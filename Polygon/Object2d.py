
from PIL import Image, ImageDraw, ImageColor
from ObjectConnector import ObjectConnector

class Object2d:
    # object to hold a 2d shape, drawn with a geo language
    def __init__(self):
        self.holes = []     # array of array of points of holes
        self.border = [(0,0)]    # the outer points of the shape
        self.connectors = []# array of 4 points of box connector
        self.connectors2 = [] # array of dict of connectors
    def add_hole(self,hole):
        # add a hole to the shape
        # hole = array of points
        self.holes.append(hole)
    def add_border_point(self,point):
        # add a border point to the shape
        # the shape is defined by the lines between the points
        # the shape is closed by a line from the last to the first point
        self.border.append((round(point[0],3),round(point[1],3)))
    def add_connector(self,p1,p2):
        # add a connector box defined by the two oposite points
        # round the coordinates, so small deviations are removed
        p1 = (round(p1[0],3),round(p1[1],3))
        p2 = (round(p2[0],3),round(p2[1],3))
        connector_box = [p1, [p1[0],p2[1]], p2, [p2[0],p1[1]]]
        self.connectors.append(connector_box)
    def add_connector2(self,centroid,widthX,heightY,direction):
        # add a connector with a centre and width,height and direction
        objconnector = ObjectConnector()
        objconnector.init2(centroid,widthX,heightY,direction)
        self.connectors2.append(objconnector)
    def add_connector_boxes(self,connectors):
        # add a list of boxes as connectors
        for connector in connectors:
            self.connectors.append(connector)
    def add_connector2_boxes(self,connectors2):
        for connector in connectors2:
            self.connectors2.append(connector)
    def moveorigin(self,dx,dy):
        # move the origin of the shape
        # usual a shape is positioned with 0,0 at the left low corner
        # To ad a hole (also a shape) to a shape, move it first to the right position
        def _moveorigin(points,dx,dy):
            newpoints = []
            for point in points:
                newpoints.append([point[0] + dx,point[1] + dy])
            return newpoints

        self.border = _moveorigin(self.border,dx,dy)
        
        newholes = []
        for hole in self.holes:
            newholes.append(_moveorigin(hole,dx,dy))
        self.holes = newholes
        
        newconnectors = []
        for connector in self.connectors:
            newconnectors.append(_moveorigin(connector,dx,dy))
        self.connectors = newconnectors

        for connector in self.connectors2:
            connector.moveorigin(dx,dy)
    def autoAddConnectors(self):
        # add connectors for border, if there are no connectors
        # used when adding a hole to the shape
        if len(self.connectors2) != 0:
            return
        if len(self.border) != 4:
            return
        deltax = round(self.border[2][0] - self.border[0][0])
        deltay = round(self.border[2][1] - self.border[0][1])
        #print(deltax,deltay,self.border)
        if deltax == 18 or deltax == 36 or deltax == 54:
            for x in range(9,deltax,18):
                objcon = ObjectConnector()
                #objcon.init2((self.border[0][0] + x,self.border[0][1] + deltay/2),18,abs(deltay),90)
                objcon.init2([x, deltay/2, 9],18,abs(deltay),90)
                self.connectors2.append(objcon)
        elif deltax == -18 or deltax == -36 or deltax == -54:
            for x in range(-9,deltax,-18):
                objcon = ObjectConnector()
                #objcon.init2((self.border[0][0] + x,self.border[0][1] + deltay/2),18,abs(deltay),90)
                objcon.init2([x, deltay/2, 9],18,abs(deltay),90)
                self.connectors2.append(objcon)
        elif deltay == 18 or deltay == 36 or deltay == 54:
            for y in range(9,deltay,18):
                objcon = ObjectConnector()
                #objcon.init2((self.border[0][0] + deltax / 2, self.border[0][1] + y),abs(deltax),18,90)
                objcon.init2([deltax / 2, y, 9],abs(deltax),18,90)
                self.connectors2.append(objcon)
        elif deltay == -18 or deltay == -36 or deltay == -54:
            for y in range(-9,deltay,-18):
                objcon = ObjectConnector()
                #objcon.init2((self.border[0][0] + deltax / 2,self.border[0][1] + y),abs(deltax),18,90)
                objcon.init2([deltax / 2, y, 9],abs(deltax),18,90)
                self.connectors2.append(objcon)
                
        
        # for debug, to show a image of the shape
    def show_image(self):
        def _drawlines(points,draw,color):
            linecolor = ImageColor.getrgb(color)
            first = True
            for pointnr in range(len(points)):
                point = points[pointnr]
                colorshade = 1.0 - 0.5 * pointnr / len(points)      # from 100% till 50% of color
                shadedlinecolor = (int(linecolor[0] * colorshade), int(linecolor[1] * colorshade), int(linecolor[2] * colorshade))
                if not first:
                    draw.line((x + 2500,y + 2500,point[0] + 2500,point[1]+2500), fill = shadedlinecolor)
                x = point[0]
                y = point[1]
                first = False
            draw.line((x+2500,y+2500,points[0][0]+2500,points[0][1]+2500), fill = shadedlinecolor)

        img = Image.new("RGB",(5000,5000))
        draw = ImageDraw.Draw(img)
        _drawlines(self.border,draw,"WhiteSmoke")
        for hole in self.holes:
            _drawlines(hole,draw,"YellowGreen")
        for connector in self.connectors:
            _drawlines(connector,draw,"red")
        for connector2 in self.connectors2:
            linecolor = ImageColor.getrgb("Violet")
            box = connector2.get_box()
            newbox = []
            for point in box:
                newbox.append((2500 + point[0],2500 + point[1]))
            draw.polygon(newbox,outline=linecolor)
            linecolor = ImageColor.getrgb("white")
            draw.point((2500 + connector2.centroid[0], 2500 + connector2.centroid[1]),linecolor)
                           
        img = img.crop(img.getbbox()).transpose(Image.FLIP_TOP_BOTTOM)
        img.show()
        print("The height of the image is: ", img.height)
        print("The width of the image is: ", img.width)
