
import json

import Object3d

class ObjectLibrary:
    def __init__(self):
        # all objects in library
        self.objects = []

    def add_object(self,obj3d):
        obj3d.name = obj3d.name.upper()
        # add an object to library
        foundnr = -1
        for objnr in range(len(self.objects)):
            if obj3d.name == self.objects[objnr].name:
                foundnr = objnr
                break
        if foundnr == -1:
            self.objects.append(obj3d)
            #print("Library add",obj3d.name)
        else:
            self.objects[foundnr] = obj3d
            #print("Library replace",obj3d.name)
            #for c in obj3d.connectors2:
            #    print(c.widthX,c.heightY,c.depthZ)
    

    def save(self,filename):
        data = []
        for obj in self.objects:
            data.append(obj.to_dict())
        #print(data)
        with open(filename,"w") as fp:
            json.dump(data,fp, indent = 4)

    def load(self,filename):
        with open(filename,"r") as fp:
            data = json.load(fp)
        for obj in data:
            obj3d = Object3d.Object3d("")
            obj3d.from_dict(obj)
            #obj3d.name = obj3d.name.upper()
            self.add_object(obj3d)

    def get_object(self,name):
        foundnr = -1
        for objnr in range(len(self.objects)):
            if name == self.objects[objnr].name:
                foundnr = objnr
                break
        #print(foundnr,self.objects[objnr].name)
        msg = "object {} not found in library".format(name)
        assert foundnr != -1,msg
        return self.objects[foundnr]
