
import math
from PIL import Image, ImageDraw
from gon.shaped import Polygon         # https://github.com/lycantropos/gon/

def Connector(self):
    def __init__(self,name):
        self.name = name
        self.polygoon = []
        
# eigenlijk een module, maar dat wil niet.

class DrawPolygon:
    def __init__(self,name,startx = 0.0,starty = 0.0,direction = 0):
        self.name = name
        self.x = startx    # "turtle" x and y
        self.y = starty
        self.direction = direction   # of deltaX,deltaY ?
        self.points = [(self.x,self.y)]
        #self.points2 = Multipoint()
        self.commands = []    # array to hold commands for this polygon

    def _forward(self,length,width = 0):
        self.x += math.cos(math.radians(self.direction)) * length
        self.y += math.sin(math.radians(self.direction)) * length
        if width:
            self.x += math.cos(math.radians(self.direction + 90)) * -width
            self.y += math.sin(math.radians(self.direction + 90)) * -width
        self.points.append((self.x,self.y))

    def forward(self,length,width = 0):
        if width:
            self.commands.append("Forward {},{}".format(length,width))
        else:
            self.commands.append("Forward {}".format(length))
        self._forward(length,width)

    def left(self,length,width = 0):
        if width:
            self.commands.append("Left {},{}".format(length,width))
        else:
            self.commands.append("Left {}".format(length))
        self.direction += 90
        self._forward(length,width)

    def right(self,length,width = 0):
        if width:
            self.commands.append("Right {},{}".format(length,width))
        else:
            self.commands.append("Right {}".format(length))
        self.direction -= 90
        self._forward(length,width)
        
    def draw(self,img,offsetx,offsety):
        draw = ImageDraw.Draw(img)
        first = True
        for point in self.points:
            if not first:
                draw.line((x,y,point[0] - offsetx,point[1] - offsety))
            x = point[0] - offsetx
            y = point[1] - offsety
            first = False
        draw.line((x,y,self.points[0][0] - offsetx,self.points[0][1] - offsety))

    def minmaxXY(self):
        minx = self.points[0][0]
        miny = self.points[0][1]
        maxx = minx
        maxy = miny
        for point in self.points:
            minx = min(minx,point[0])
            maxx = max(maxx,point[0])
            miny = min(miny,point[1])
            maxy = max(maxy,point[1])
        return (minx,miny,maxx,maxy)

    def copy(self,deltax,deltay):     # eigenlijk een instancie maken
        ret = DrawPolygon(self.name)
        ret.points = []     #moet anders
        for point in self.points:
            ret.points.append((point[0] + deltax,point[1] + deltay))
        return ret

    def tomesh(self,start_point_nr,clockwise = False,thickness = 0.018):
        # start_point_nr is om door te nummer per shape
        # points is in mm ipv meter, dus delen door 1000
        # faces wordt nog niet gemaakt, alleen wireframe
        #    nog parameter nodig of het inclusief polygon is, of niet, wegens de draairichting volgorde van punten van een face
        # clockwise = true als een zijkant clockwise (border zijkant) of anti clockwise (hole zijkant)
        vertices = []
        edges = []
        faces = []
        pointnr = start_point_nr
        first = True
        for point in self.points:
            if not first:
                #edges.append([pointnr - 2,pointnr])    # edged hebben we niet meer
                #edges.append([pointnr - 1,pointnr + 1])    # edged hebben we niet meer
                if clockwise:
                    faces.append([pointnr - 2,pointnr - 1, pointnr + 1,pointnr])
                else:
                    faces.append([pointnr - 2,pointnr, pointnr + 1,pointnr - 1])
            #print(point)
            vertices.append([point[0]/1000,point[1]/1000,0])
            vertices.append([point[0]/1000,point[1]/1000,thickness])
            #edges.append([pointnr,pointnr + 1])
            pointnr += 2
            first = False
        if clockwise:
            faces.append([pointnr - 2,pointnr - 1, start_point_nr + 1,start_point_nr])
        else:
            faces.append([pointnr - 2,start_point_nr, start_point_nr + 1,pointnr - 1])
        #edges.append([pointnr - 2,start_point_nr])
        #edges.append([pointnr - 1,start_point_nr + 1])
        return vertices,edges,faces
"""
    def push(self):
        self.stack.append((self.x,self.y,self.direction))

    def pull(self):
        if self.stack:
            self.x, self.y, self.direction = self.stack.pop()
        else:
            print("ERROR stack empty")

    def close(self):
        self.x, self.y = self.points[0]
        self.points.append((self.x,self.y))
"""
    

class shape:
    def __init__(self,outer,name = ""):
        self.included = outer
        self.excluded = []
        #self.holes = []
        #self.border = []
        #self.connectors = []
        self.name = name
        self.commands = []    # array to hold commands for this shape

    def add_exclude(self,exclude_poly,x,y):
        self.commands.append("Hole {} at {},{}".format(exclude_poly.name,x,y))
        copy_exclude_poly = exclude_poly.copy(x,y)
        self.excluded.append(copy_exclude_poly)

    def make_image(self):
        # herschijf met minmax namen
        size = self.included.minmaxXY()

        img = Image.new("RGB",(int(size[2] - size[0]) + 1,int(size[3] - size[1]) + 1))
        self.included.draw(img,size[0],size[1])
        for exclude in self.excluded:
            exclude.draw(img,size[0],size[1])
        return img.transpose(Image.FLIP_TOP_BOTTOM)

    def export2mesh(self,startpointnr = 1,thickness = 0.018):
        #border = s.included.points
        all_points = []     # contains all points, so x,y points of triangle can be translated to pointnr's
        all_points += self.included.points
        holes = []
        for poly in self.excluded:
            holes.append(poly.points)
            all_points += poly.points
        #print(len(all_points))
        vertices, edges, faces = self.included.tomesh(startpointnr,False,thickness)    

        p = Polygon.from_raw([self.included.points,holes])
        triangles = p.triangulate()         # make triangles of polygon with holes

        for triangle in triangles:
            raw = triangle.raw()[0]
            a = raw[0]
            b = raw[1]
            c = raw[2]
            a_nr = all_points.index(a)
            b_nr = all_points.index(b)
            c_nr = all_points.index(c)
            faces.append([c_nr * 2+1,b_nr *2+1,a_nr *2 +1])
            faces.append([a_nr * 2+2,b_nr *2+2,c_nr *2 +2])
        for excluded_poly in self.excluded:
            v,e,f = excluded_poly.tomesh(len(vertices) + 1,True,thickness)    # the +1 is because obj files start counting vertices with 1
            vertices += v
            edges += e
            faces += f
        return vertices, edges, faces
    
trap = []

c1 = DrawPolygon("c60")
# c.addconnector("c1-female")
c1.forward(28)
c1.left(10)
c1.left(5)
c1.right(40)
c1.right(5)
c1.left(10)
c1.left(28)
c1.left(10)
c1.left(5)
c1.right(40)
c1.right(5)
#c1.left(10)

def tredegat(poly,delta):
    poly.left(58.5 - delta)
    poly.left(5)
    poly.right(10)
    poly.right(28)
    poly.right(10)
    poly.right(5)
    poly.left(58 + delta)
    
a = DrawPolygon("a")
a.forward(152)
a.left(318,56)
a.right(289)
a.right(318,-56)
a.left(152)
a.left(318,-56)
tredegat(a,-1.5)
a.left(242,-43)
tredegat(a,-1.5)
a.left(242,-43)
tredegat(a,-1.5)
a.left(242,-43)
tredegat(a,-1.5)
a.left(242,-43)
tredegat(a,-1.5)
a.left(246,-43)
a.left(30)
a.left(23)
a.right(10)
a.right(5)
a.left(53)
a.left(5)
a.right(10)
a.right(23)
a.left(30)
a.left(246,43)
tredegat(a,1.5)
a.left(242,43)
tredegat(a,1.5)
a.left(242,43)
tredegat(a,1.5)
a.left(242,43)
tredegat(a,1.5)
a.left(242,43)
tredegat(a,1.5)
#a.left(318,56)

    
ahole = DrawPolygon("ahole")
ahole.forward(253)
ahole.left(512,-90)
ahole.left(73)

trede = DrawPolygon("trede")
trede.forward(20)

trede.left(20)
trede.left(5)
trede.right(10)
trede.right(28)
trede.right(10)
trede.right(5)
trede.left(20)

trede.left(382)

trede.left(20)
trede.left(5)
trede.right(10)
trede.right(28)
trede.right(10)
trede.right(5)
trede.left(20)

trede.left(20)
trede.left(100)
trede.left(458)
trede_shape = shape(trede,"Trede")

bredetrede = DrawPolygon("brede trede")
bredetrede.forward(458)
bredetrede.left(100)
bredetrede.left(20)

bredetrede.left(20)
bredetrede.left(5)
bredetrede.right(10)
bredetrede.right(28)
bredetrede.right(10)
bredetrede.right(5)
bredetrede.left(88)

bredetrede.left(141)
bredetrede.left(18)
bredetrede.right(241)

bredetrede.left(70)
bredetrede.left(5)
bredetrede.right(10)
bredetrede.right(28)
bredetrede.right(10)
bredetrede.right(5)
bredetrede.left(20)

bredetrede.left(20)

bredetrede_shape = shape(bredetrede,"Brede Trede")

topplank = DrawPolygon("topplank")
topplank.forward(382)
topplank.left(20)
topplank.left(5)
topplank.right(10)
topplank.right(23)
topplank.left(73)
topplank.left(23)
topplank.right(10)
topplank.right(5)
topplank.left(20)

topplank.left(382)
topplank.left(20)
topplank.left(5)
topplank.right(10)
topplank.right(23)
topplank.left(73)
topplank.left(23)
topplank.right(10)
topplank.right(5)
#left(20)

topplankhole = DrawPolygon("topplank hole")
topplankhole.forward(10)
topplankhole.left(5)
topplankhole.right(80)
topplankhole.right(5)
topplankhole.left(10)
topplankhole.left(28)

topplankhole.left(10)
topplankhole.left(5)
topplankhole.right(80)
topplankhole.right(5)
topplankhole.left(10)
#topplankhole.left(28)

topplank_shape = shape(topplank,"Topplank")
topplank_shape.add_exclude(topplankhole,141,52)

topsteun = DrawPolygon("topsteun")
topsteun.forward(60)
topsteun.left(73)
topsteun.right(10)
topsteun.right(5)
topsteun.left(20)
topsteun.left(382)
topsteun.left(20)
topsteun.left(5)
topsteun.right(10)
topsteun.right(73)

topsteun.left(60)
topsteun.left(73)
topsteun.right(10)
topsteun.right(5)
topsteun.left(20)
topsteun.left(141)
topsteun.right(18)
topsteun.left(100)
topsteun.left(18)
topsteun.right(141)
topsteun.left(20)
topsteun.left(5)
topsteun.right(10)
#topsteun.right(73)

c73 = DrawPolygon("c73")
c73.forward(28)
c73.left(10)
c73.left(5)
c73.right(73 - 20)
c73.right(5)
c73.left(10)
c73.left(28)
c73.left(10)
c73.left(5)
c73.right(73 - 20)
c73.right(5)
#c73.left(10)

topsteun_shape = shape(topsteun,"Topsteun")
topsteun_shape.add_exclude(c73,16,20)
topsteun_shape.add_exclude(c73,16,425)

midsteun = DrawPolygon("midsteun")
midsteun.forward(60)
midsteun.left(73)
midsteun.right(10)
midsteun.right(5)
midsteun.left(44)
midsteun.left(382)
midsteun.left(44)
midsteun.left(5)
midsteun.right(10)
midsteun.right(73)

midsteun.left(60)
midsteun.left(73)
midsteun.right(10)
midsteun.right(5)
midsteun.left(44)
midsteun.left(141)
midsteun.right(18)
midsteun.left(100)
midsteun.left(18)
midsteun.right(141)
midsteun.left(44)
midsteun.left(5)
midsteun.right(10)
#midsteun.right(73)

midsteun_shape = shape(midsteun,"Midden steun")
midsteun_shape.add_exclude(c73,16,20)
midsteun_shape.add_exclude(c73,16,425)

lowsteun = DrawPolygon("lowsteun")
lowsteun.forward(60)
lowsteun.left(73)
lowsteun.right(10)
lowsteun.right(5)
lowsteun.left(10)
lowsteun.left(382)
lowsteun.left(10)
lowsteun.left(5)
lowsteun.right(10)
lowsteun.right(73)

lowsteun.left(60)
lowsteun.left(73)
lowsteun.right(10)
lowsteun.right(5)
lowsteun.left(10)
lowsteun.left(382)
lowsteun.left(10)
lowsteun.left(5)
lowsteun.right(10)
#right(73)

lowsteun_shape = shape(lowsteun,"Lower steun")
lowsteun_shape.add_exclude(c73,16,20)
lowsteun_shape.add_exclude(c73,16,425)

peg = DrawPolygon("peg")
peg.forward(97)
peg.left(29)
peg.left(81,2)
peg.right(9)
peg.right(5)
peg.left(9)
peg.left(21)

peg_shape = shape(peg,"Peg")

a_shape = shape(a,"A")
a_shape.add_exclude(ahole,226,418)
a_shape.add_exclude(c1,339,338)
a_shape.add_exclude(c1,339,985)
a_shape.add_exclude(c1,339,1509)
#size = a.minmaxXY()

#i = Image.new("RGB",(int(size[2]) + 1,int(size[3]) + 1))
i = a_shape.make_image()
#i.show()
i.save("a-shape.png")
#img = a.makeImage()
#img.show()

"""
to_blender = {}
for lib_shape in (a_shape,peg_shape,lowsteun_shape,midsteun_shape,topsteun_shape,trede_shape,bredetrede_shape,topplank_shape):
    vertices,edges,faces = lib_shape.export2mesh(0,0.018)
    to_blender[lib_shape.name] = { "vertices" : vertices,"edges" : edges,"faces" : faces }

import json

fp = open("toblender.json","w")
json.dump(to_blender,fp,indent=2)
fp.close()
"""
"""
############ delaunay_triangulation test ###########################

from delaunay_triangulation.triangulate import delaunay
from delaunay_triangulation.typing import Vertex, Triangle, Coordinate, Edge
from typing import List, NoReturn


vertices: List[Vertex] = []
for i in a_shape.included.points:
    vertices.append(Vertex(x=i[0],y=i[1]))
vv = []
for poly in a_shape.excluded:
    for e in poly.points:
        aap = Vertex(x=e[0],y=e[1])
        vertices.append(aap)
        vv.append(aap)

# delete_super_shared is True by default but can be turned off if you need to fill a plane completely
triangles = delaunay(
    vertices=vertices,
    delete_super_shared=True
)

from PIL import Image, ImageDraw
i = a_shape.make_image().transpose(Image.FLIP_TOP_BOTTOM)
draw = ImageDraw.Draw(i)
for v in vertices:
    draw.ellipse((v.x-5,v.y-5,v.x +5,v.y+5),fill=(255,255,255))
for t in triangles:
    #if t.a in vv and t.b in vv and t.c in vv:
    #    continue
    draw.line((t.a.x,t.a.y,t.b.x,t.b.y),fill=(155,0,0))
    draw.line((t.a.x,t.a.y,t.c.x,t.c.y),fill=(155,0,0))
    draw.line((t.c.x,t.c.y,t.b.x,t.b.y),fill=(155,0,0))

#i.show()

tel = 0
for t in triangles:
    if t.a in vv and t.b in vv and t.c in vv:
       tel += 1
print(tel)

#i.save("a-shape.png")
"""
######################### gon test ##########

from gon.shaped import Polygon

s=a_shape
border = s.included.points
holes = []
#for i in a_shape.included.points:
#    vertices.append(Vertex(x=i[0],y=i[1]))

"""
for poly in s.excluded:
    vv = []
    for e in poly.points:
        aap = (e[0],e[1])
        vv.append(aap)
    holes.append(vv)
"""
for poly in s.excluded:
    holes.append(poly.points)



p = Polygon.from_raw([border,holes])
triangles = p.triangulate()

from PIL import Image, ImageDraw
i = s.make_image().transpose(Image.FLIP_TOP_BOTTOM)
draw = ImageDraw.Draw(i)
for point in border:
    draw.ellipse((point[0]-5,point[1]-5,point[0] +5,point[1]+5),fill=(255,255,255))

for poly in s.excluded:
    for e in poly.points:
        draw.ellipse((e[0]-5,e[1]-5,e[0]+5,e[1]+5),fill=(255,255,255))

for t in triangles:
    #if t.a in vv and t.b in vv and t.c in vv:
    #    continue
    raw = t.raw()[0]
    draw.line((raw[0][0],raw[0][1],raw[1][0],raw[1][1]),fill=(155,0,0))
    draw.line((raw[0][0],raw[0][1],raw[2][0],raw[2][1]),fill=(155,0,0))
    draw.line((raw[1][0],raw[1][1],raw[2][0],raw[2][1]),fill=(155,0,0))

#i.show()

#print(len(a_shape.included.points))
for lib_shape in (a_shape,peg_shape,lowsteun_shape,midsteun_shape,topsteun_shape,trede_shape,bredetrede_shape,topplank_shape):
    
    v,e,f = lib_shape.export2mesh()

    fp=open(lib_shape.name + ".obj","w")
    for point in v:
        fp.write("v {} {} {}\n".format(point[0],point[1],point[2]))
    for face in f:
        if len(face) == 3:
            fp.write("f {} {} {}\n".format(face[0],face[1],face[2]))
            
        elif len(face) == 4:
            fp.write("f {} {} {} {}\n".format(face[0],face[1],face[2],face[3]))
            
        else:
            print("error length face")

    fp.close()




import math 

def q_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)

def qv_mult(q1, v1):
    q2 = [0.0,] + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z

def euler_to_quaternion(phi, theta, psi):
 
        qw = math.cos(phi/2) * math.cos(theta/2) * math.cos(psi/2) + math.sin(phi/2) * math.sin(theta/2) * math.sin(psi/2)
        qx = math.sin(phi/2) * math.cos(theta/2) * math.cos(psi/2) - math.cos(phi/2) * math.sin(theta/2) * math.sin(psi/2)
        qy = math.cos(phi/2) * math.sin(theta/2) * math.cos(psi/2) + math.sin(phi/2) * math.cos(theta/2) * math.sin(psi/2)
        qz = math.cos(phi/2) * math.cos(theta/2) * math.sin(psi/2) - math.sin(phi/2) * math.sin(theta/2) * math.cos(psi/2)
 
        return [qw, qx, qy, qz]

def quaternion_to_euler(w, x, y, z):
 
        t0 = 2 * (w * x + y * z)
        t1 = 1 - 2 * (x * x + y * y)
        X = math.atan2(t0, t1)
 
        t2 = 2 * (w * y - z * x)
        t2 = 1 if t2 > 1 else t2
        t2 = -1 if t2 < -1 else t2
        Y = math.asin(t2)
         
        t3 = 2 * (w * z + x * y)
        t4 = 1 - 2 * (y * y + z * z)
        Z = math.atan2(t3, t4)
 
        return X, Y, Z
    
def normalize(v, tolerance=0.00001):
    mag2 = sum(n * n for n in v)
    if abs(mag2 - 1.0) > tolerance:
        mag = math.sqrt(mag2)
        v = tuple(n / mag for n in v)
    return v

lib_shape = a_shape
for angle in range(0,360,15):
    
    v,e,f = lib_shape.export2mesh()
    phi = math.radians(0)
    theta = math.radians(0)
    psi = math.radians(angle)
    q = euler_to_quaternion(phi, theta, psi)

    fp=open(lib_shape.name + "-" + str(angle) + ".obj","w")
    for point in v:
        rotated_point = qv_mult(q,point)
        
        fp.write("v {} {} {}\n".format(rotated_point[0],rotated_point[1],rotated_point[2]))
    for face in f:
        if len(face) == 3:
            fp.write("f {} {} {}\n".format(face[0],face[1],face[2]))
            
        elif len(face) == 4:
            fp.write("f {} {} {} {}\n".format(face[0],face[1],face[2],face[3]))
            
        else:
            print("error length face")

    fp.close()

