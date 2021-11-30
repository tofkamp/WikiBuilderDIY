
import math

import ObjectLibrary
import Object3d

from ObjectConnector import ObjectConnector
from transform import Transform

class ObjectInstance:
    # an instance of a object in a world
    def __init__(self,obj3d):
        self.obj3d = obj3d
        self.transform = Transform()

    def move(self,dx,dy,dz):
        self.transform.Move(dx,dy,dz)
        
    def rotate(self,phi,theta,psi):
        self.transform.Rotate(phi,theta,psi)
    """    
    #def ConnectTo(self,dest_connector):
        # move this instance to the destination connector position
    
    def get_connector_centroid(self,indexnr):
        # return the centroid of the connector with index in world coordinates
        return self.transform.Point(self.connectors[indexnr].centroid)
    """
    def write_to_objfile(self,fp, next_point_nr, scale=1):
        # write an object to a file in .obj file format
        # next_point_nr is the next free vertices number, usual for obj files it starts with 1, for unity it is 0
        # scale is for scaling it down, so it could be 3d printed (scale = 10)
        # points are in mm
        # put group name for every shape (optional)
        fp.write("g {}\n".format(self.obj3d.name))
        for point in self.obj3d.vertices:
            rotated_point = self.transform.Point(point)
            fp.write("v {} {} {}\n".format((rotated_point[0])/scale, (rotated_point[1])/scale, (rotated_point[2])/scale))
        for face in self.obj3d.faces:
            if len(face) == 3:
                fp.write("f {} {} {}\n".format(face[0] + next_point_nr,face[1] + next_point_nr,face[2] + next_point_nr))
            elif len(face) == 4:
                fp.write("f {} {} {} {}\n".format(face[0] + next_point_nr,face[1] + next_point_nr,face[2] + next_point_nr,face[3] + next_point_nr))
            else:
                print("error length face")
        return next_point_nr + len(self.obj3d.vertices)
    
class ObjectWorld:
    def __init__(self):
        # create a new world for object definitions and instances
        # if we only could do this to the real world...
        self.objects = []
        self.library = ObjectLibrary.ObjectLibrary()

    def addLibrary(self,filename):
        # add a library with object definitions
        # filename is without .json and in subfolder library
        self.library.load("library/"+ filename + ".json")

    def addObject(self,name):
        # add an objectinstance to the world
        # name = name of object from library
        obj3d = self.library.get_object(name)
        obj = ObjectInstance(obj3d)
        self.objects.append(obj)
        return obj

    def save_as_objfile(self,filename,scale = 1):
        # save the world as one obj file
        fp = open(filename,"w")
        next_point_nr = 1       # obj files start with point nr 1
        for instance in self.objects:
            next_point_nr = instance.write_to_objfile(fp, next_point_nr,scale)
        fp.close()

    def debug_print_connectors(self):
        for i in self.objects:
            for connector in i.obj3d.connectors2:
                centroid = i.transform.Point(connector.centroid)
                print(i.obj3d.name,connector.type,centroid[0], centroid[1], centroid[2])

    def debug_print_objects(self):
        quaternion2euler = {(1.0, 0.0, 0.0, 0.0): (0, 0, 0), (0.5000000000000001, -0.5000000000000001, -0.5000000000000001, -0.5000000000000001): (0, -90, -90), (0.5000000000000001, 0.5000000000000001, -0.5000000000000001, 0.5000000000000001): (90, -90, 0), (0.5000000000000001, 0.5000000000000001, 0.5000000000000001, -0.5000000000000001): (90, 90, 0), (0.5000000000000001, -0.5000000000000001, 0.5000000000000001, -0.5000000000000001): (-90, 0, -90), (0.7071067811865476, -0.7071067811865476, 0.0, 0.0): (-90, 0, 0), (0.7071067811865476, 0.7071067811865476, 0.0, 0.0): (90, 0, 0), (0.5000000000000001, -0.5000000000000001, 0.5000000000000001, 0.5000000000000001): (0, 90, 90)}
        for i in self.objects:
            if i.transform.quaternion in quaternion2euler:
                print('    ["{}", ({}, {}, {}), {}],'.format(i.obj3d.name,round(i.transform.originX,3),round(i.transform.originY,3),round(i.transform.originZ,3),quaternion2euler[i.transform.quaternion]))
            else:
                print('    ["{}", ({}, {}, {}), {}],'.format(i.obj3d.name,round(i.transform.originX,3),round(i.transform.originY,3),round(i.transform.originZ,3),i.transform.quaternion))

if __name__ == '__main__':

    ladder = [
        ["a", (0, 0, 0), (0, 0, 0)],
        ["topplank", (286.0, 1606.0, 18.0), (0, -90, -90)],
        ["a", (0.0, 0.0, 400.0), (0, 0, 0)],
        ["trede", (156.0, 336.0, -20.0), (90, -90, 0)],
        ["trede", (549.0, 318.0, -20.0), (0, -90, -90)],
        ["trede", (202.0, 597.0, -20.0), (90, -90, 0)],
        ["trede", (503.0, 579.0, -20.0), (0, -90, -90)],
        ["trede", (248.0, 858.0, -20.0), (90, -90, 0)],
        ["trede", (457.0, 840.0, -20.0), (0, -90, -90)],
        ["trede", (340.0, 1380.0, -20.0), (90, -90, 0)],
        ["trede", (365.0, 1362.0, -20.0), (0, -90, -90)],
        ["bredetrede", (511.0, 1119.0, -20.0), (90, -90, 0)],
        ["bredetrede", (194.0, 1119.0, 438.0), (90, 90, 0)],
        ["lowsteun", (344.0, 398.0, 468.0), (-90, 0, -90)],
        ["peg", (287.5, 359.0, 0.0), (-90, 0, 0)],
        ["peg", (287.5, 377.0, 418.0), (90, 0, 0)],
        ["midsteun", (344.0, 1047.0, 468.0), (-90, 0, -90)],
        ["peg", (287.5, 1008.0, 0.0), (-90, 0, 0)],
        ["peg", (287.5, 1026.0, 418.0), (90, 0, 0)],
        ["topsteun", (344.0, 1569.0, 468.0), (-90, 0, -90)],
        ["peg", (287.5, 1530.0, 0.0), (-90, 0, 0)],
        ["peg", (287.5, 1548.0, 418.0), (90, 0, 0)]]
    ladderdiy = [
        ["a", (0, 0, 0), (0, -90, -90)],
        ["a", (1624, 18, 439), (90, -90, 0)],
        ["lowsteun", (1040, 18, 100), (90, 90, 0)],
        ["peg", (0, 0, 300), (-90, 0, 0)],
        ["peg", (140, 0, 335), (-90, 0, 0)],
        ["peg", (0, 0, 370), (-90, 0, 0)],
        ["peg", (140, 0, 405), (-90, 0, 0)],
        ["peg", (0, 0, 440), (-90, 0, 0)],
        ["peg", (140, 0, 475), (-90, 0, 0)],
        ["trede", (1650, 0, 0), (0, -90, -90)],
        ["trede", (1770, 0, 0), (0, -90, -90)],
        ["trede", (1890, 0, 0), (0, -90, -90)],
        ["trede", (2010, 0, 0), (0, -90, -90)],
        ["trede", (2130, 0, 0), (0, -90, -90)],
        ["trede", (2250, 0, 0), (0, -90, -90)],
        ["trede", (1650, 0, 500), (0, -90, -90)],
        ["trede", (1770, 0, 500), (0, -90, -90)],
        ["bredetrede", (1890, 0, 500), (0, -90, -90)],
        ["bredetrede", (2230, 0, 960), (0, 90, 90)],
        ["topplank", (2250, 0, 500), (0, -90, -90)],
        ["midsteun", (0, 0, 1050), (0, -90, -90)],
        ["topsteun", (550, 0, 1100), (0, -90, -90)]]

    world = ObjectWorld()
    world.addLibrary("ladder")
    for line in ladder:
        obj = world.addObject(line[0])
        obj.rotate(line[2][0], line[2][1], line[2][2])
        #obj.transform.quaternion = line[2]
        obj.move(line[1][0],line[1][1],line[1][2])

    world.save_as_objfile("ladder.obj",1000)

    #world.debug_print_objects()

    world = ObjectWorld()
    world.addLibrary("ladder")
    for line in ladderdiy:
        obj = world.addObject(line[0])
        obj.rotate(line[2][0], line[2][1], line[2][2])
        #obj.transform.quaternion = line[2]
        obj.move(line[1][0],line[1][1],line[1][2])

    world.save_as_objfile("ladderdiy.obj")

    #world.debug_print_objects()
    
    #world.debug_print_connectors()
"""
    qs = []
    for line in ladder + ladderdiy:
        if line[2] not in qs:
            qs.append(line[2])
    print(qs)
    result = {}
    for q in qs:
        found = None
        for x in range(-90,91,90):
            for y in range(-90,91,90):
                for z in range(-90,91,90):
                    t = Transform()
                    t.Rotate(x,y,z)
                    #print(x,y,z,t.quaternion)
                    if t.quaternion == q:
                        found = x,y,z
        if found:
            print(found,q)
            result[q] = found
        else:
            print("not found",q)
    print(result)
"""
