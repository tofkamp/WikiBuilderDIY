
import math

class ObjectConnector:
                   
    def __init__(self):
        #self.faces = []
        #self.vertices = []
        #self.edges = []
        self.type = "?x?x?"
        self.centroid = [0,0,0]
        self.widthX = 0     # size in x axis
        self.heightY = 0    # size in y axis
        self.depthZ = 0     # size in z axis (== thickness)
        self.rotateZ = 0    # rotation around z axis
        #self.points = []
        
    def _init_from_points(self,points):
        # init connector from 8 points of cube
        #self.points = points
        #self.allowed_vectors = []   # future
        # find the centre of the box by averaging all points
        x = 0.0
        y = 0.0
        z = 0.0
        for point in points:
            x += point[0]
            y += point[1]
            z += point[2]
        x /= len(points)
        y /= len(points)
        z /= len(points)
        # kan eruit ?
        self.centroid = [x,y,z]
        #print(self.centroid,[x,y,z])
        # find type name of connector by sorting the length,height and width
        # get max size of box per axis (hardcoded, not good)
        maxx = abs(points[0][0] - points[5][0])
        maxy = abs(points[0][1] - points[5][1])
        maxz = abs(points[0][2] - points[5][2])
        # sort length of box sides, small to big
        if maxx > maxy:
            t = maxx
            maxx = maxy
            maxy = t
        if maxy > maxz:
            t = maxy
            maxy = maxz
            maxz = t
        if maxx > maxy:
            t = maxx
            maxx = maxy
            maxy = t
        # set the kind of connector eg 18x18x70
        # kan eruit ?
        self.type = "{}x{}x{}".format(round(maxx),round(maxy),round(maxz))
        # prepare the 3d object to display or write to objfile
        #self.faces = []
        #self.vertices = points
        #self.edges = [] # not used, maybe in future
        # set faces of sidebox
        # hardcoded len(points) == 8, other length should be possible, but not now
        #for vnr in range(2, len(self.vertices), 2):
        #    self.faces.append([vnr - 2,vnr - 1,vnr + 1,vnr])
        #self.faces.append([1, 0, len(self.vertices) - 2, len(self.vertices) - 1])
        ## write faces top and bottom quad
        #self.faces.append([0 ,2, 4, 6])
        #self.faces.append([7 ,5, 3, 1])
        
    def init2(self,centroid,widthX,heightY,direction):
        self.widthX = widthX   # size in x axis
        self.heightY = heightY   # size in y axis
        self.depthZ = 18                    # size in z axis
        self.rotateZ = direction        
        #print(self.centroid,centroid)
        self.centroid = centroid
        self.type = "{}x{}x{}".format(self.depthZ,min(round(self.widthX),round(self.heightY)),max(round(self.widthX),round(self.heightY)))
        
    def to_dict(self):
        # convert object to a dict, so we can save it as a json object in a library
        data = {#"vertices":self.vertices,
            #"edges":self.edges,
            #"faces":self.faces,
            "type":self.type,
            "widthX":self.widthX,
            "heightY":self.heightY,
            "depthZ":self.depthZ,
            "rotateZ":self.rotateZ,
            "centroid":self.centroid}
        return data

    def moveorigin(self,dx,dy,dz = 0):
        self.centroid[0] += dx
        self.centroid[1] += dy
        self.centroid[2] += dz
            
    def from_dict(self,data):
        # convert dict to an object, so we can load it from a json object in a library
        # data is the dict containg the object
        def _get_value(index):
            if index in data:
                return data[index]
            return ""
        #self.vertices = _get_value("vertices")
        #self.edges = _get_value("edges")
        #self.faces = _get_value("faces")
        self.type = _get_value("type")
        self.centroid = _get_value("centroid")
        self.widthX = _get_value("widthX")
        self.heightY = _get_value("heightY")
        self.depthZ = _get_value("depthZ")
        self.rotateZ = _get_value("rotateZ")
        #print("from_dict",self.widthX,self.heightY,self.depthZ)

    # wrong place ?????? should be in ObjectInstance
    def get_translation(self,dest_connector):
        # move this connector to the destination connector position
        # should also handle rotation
        return dest_connector.centroid[0] - self.centroid[0], dest_connector.centroid[1] - self.centroid[1], dest_connector.centroid[2] - self.centroid[2]

    def get_box(self):
        def _rotated_point_around(x,y,direction,centroid):
            cd = math.cos(math.radians(direction))
            sd = math.sin(math.radians(direction))
            return (centroid[0] + x * sd + y *cd, centroid[1] - x * cd + y * sd)
        return [_rotated_point_around(-self.widthX / 2,-self.heightY / 2,self.rotateZ,self.centroid),
                _rotated_point_around( self.widthX / 2,-self.heightY / 2,self.rotateZ,self.centroid),
                _rotated_point_around( self.widthX / 2, self.heightY / 2,self.rotateZ,self.centroid),
                _rotated_point_around(-self.widthX / 2, self.heightY / 2,self.rotateZ,self.centroid)]
