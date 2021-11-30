import Object2d
from ObjectConnector import ObjectConnector
from ObjectInstance import ObjectInstance

import math

from ground.base import get_context, set_context, Mode
# plain mode tells underlying operations to use plain geometric operations & predicates
set_context(get_context().replace(mode=Mode.PLAIN,sqrt=math.sqrt))
# importing from gon module should go after setting context for changes to take effect
from gon.base import Polygon, Contour, Point, Orientation


class Object3d:
    def __init__(self,name):
        self.vertices = []  # list of 3d points of shape
        self.edges = []     # list of lines between points (not used)
        self.faces = []     # list of faces from vertices
        self.connectors2 = []
        self.thickness = 18 # how thicj is the sheet
        self.centroid = (0,0) # where is the centroid
        self.volume = 0     # volume of object
        self.name = name
        
    def from_Object2d(self,obj2d):

        def _points2mesh(points,clockwise = False):
            # add a list of 2d-points to 3d mesh with quad faces
            # lst is list of 2d points
            # clockwise or anti clockwise (border vs holes)
            # the thickness of sheet
            #start_point_nr = len(self.vertices) + 1       # make it 0 to start at 0 (for unity) ???
            start_point_nr = len(self.vertices)
            pointnr = start_point_nr
            first = True
            for point in points.vertices:
                if not first:
                    #self.edges.append([pointnr - 2,pointnr])
                    #self.edges.append([pointnr - 1,pointnr + 1])
                    if clockwise:
                        self.faces.append([pointnr - 2,pointnr - 1, pointnr + 1,pointnr])
                    else:
                        self.faces.append([pointnr - 2,pointnr, pointnr + 1,pointnr - 1])
                self.vertices.append([point.x,point.y,0])
                self.vertices.append([point.x,point.y,self.thickness])
                #self.edges.append([pointnr,pointnr + 1])
                pointnr += 2
                first = False
            if clockwise:
                self.faces.append([pointnr - 2,pointnr - 1, start_point_nr + 1,start_point_nr])
            else:
                self.faces.append([pointnr - 2,start_point_nr, start_point_nr + 1,pointnr - 1])
            #self.edges.append([pointnr - 2,start_point_nr])
            #self.edges.append([pointnr - 1,start_point_nr + 1])

        borderpoints = []
        for point in obj2d.border:
            borderpoints.append(Point(point[0],point[1]))
        holespoints = []
        for hole in obj2d.holes:
            hpoints = []
            for point in hole:
                hpoints.append(Point(point[0],point[1]))
            contour = Contour(hpoints)
            if contour.orientation == Orientation.CLOCKWISE:
                holespoints.append(contour)
            else:
                holespoints.append(contour.reverse())
        contour = Contour(borderpoints)
        if contour.orientation == Orientation.CLOCKWISE:
            p = Polygon(contour,holespoints)
        else:
            p = Polygon(contour.reverse(),holespoints)
        _points2mesh(p.border,True)
        for hole in p.holes:
            _points2mesh(hole,False)
        #print(p.border.orientation)
        #for hole in p.holes:
        #    print(hole.orientation)
        # te following centroid and volume are not used (yet)
        # maybe in future a point to rotate object around
        centerpoint = p.centroid
        self.centroid = [centerpoint.x,centerpoint.y,self.thickness / 2]
        # volume is equal to area(border - holes) * thickness
        self.volume = float(p.area) * self.thickness
        # triangalation
        # because we just have the contour of the shape, fill it in with triangles
        # Use triangles on top and bottom face
        triangles = p.triangulate().triangles()
        #print(triangles)
        for triangle in triangles:
            raw = triangle.vertices # we get coordinates of triangles
            a = [raw[0].x,raw[0].y]        # we need vertices index nr's
            b = [raw[1].x,raw[1].y]
            c = [raw[2].x,raw[2].y]
            a.append(0.0)
            b.append(0.0)
            c.append(0.0)
            a_nr = self.vertices.index(a)
            b_nr = self.vertices.index(b)
            c_nr = self.vertices.index(c)
            # vertices number index is the point at z-axis 0
            # the +1 vertices is the one at z-axis self.thickness (usual 18)
            self.faces.append([c_nr, b_nr, a_nr])
            self.faces.append([a_nr+1, b_nr+1, c_nr+1])
        
        # make connectors into 8 3d points to make it like a box
        for connectorNR in range(len(obj2d.connectors)):
            connector = obj2d.connectors[connectorNR]
            newconnector = []
            for point in connector:
                newconnector.append([point[0],point[1],0])
                newconnector.append([point[0],point[1],self.thickness])
            objConnector = ObjectConnector()
            objConnector.init_from_points(newconnector)
            obj2d.connectors2[connectorNR].init_from_points(newconnector)
            #self.connector.append(objConnector)
        self.connectors2 = obj2d.connectors2
        

    def to_dict(self):
        # convert object to a dict, so we can save it as a json object in a library
        connectorsdict = []
        for connector in self.connectors2:
            connectorsdict.append(connector.to_dict())
        data = {"vertices":self.vertices,
                "edges":self.edges,
                "faces":self.faces,
                #"border":self.border,
                #"connectors":self.connectors,
                "connectors2":connectorsdict,
                #"holes":self.holes,
                "name":self.name,
                "volume":self.volume,
                "centroid":self.centroid,
                "thickness":self.thickness}
        return data
    
    def from_dict(self,data):
        # convert dict to an object, so we can load it from a json object in a library
        # data is the dict containg the object
        self.vertices = data["vertices"]
        self.edges = data["edges"]
        self.faces = data["faces"]
        #self.border = data["border"]
        #self.connectors = data["connectors"]
        self.connectors2 = []
        for connector in data["connectors2"]:
            objConnector = ObjectConnector()
            objConnector.from_dict(connector)
            self.connectors2.append(objConnector)
        #self.holes = data["holes"]
        self.name = data["name"]
        self.volume = data["volume"]
        self.centroid = data["centroid"]
        self.thickness = data["thickness"]
    
    # op termijn export2obj(fp,startpointnr)
    # add materials
    def export2obj(self,filename,scale = 1,add_connectors = False):
        # export object as obj file
        # write it to filename
        # scale, set it to 10 for 3d print files
        # if you want to see the connectors, set it to True
        fp = open(filename + ".obj","w")
        fp.write("mtllib polygon.mtl\n")    # use this material library
        fp.write("usemtl objectcolour\n")   # the colour of the object
        obj = ObjectInstance(self).write_to_objfile(fp,1,scale)
        fp.close()
