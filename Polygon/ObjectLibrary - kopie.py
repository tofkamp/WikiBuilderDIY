
import json

import Object3d

class ObjectLibrary:
    def __init__(self):
        # all objects in library
        self.objects = {}

    def add_object(self,name,obj3d):
        # add an object to library
        self.objects[name] = obj3d

    def save(self,filename):
        data = {}
        for objname in self.objects:
            data[objname] = self.objects[objname].to_dict()
        with open(filename,"w") as fp:
            json.dump(data,fp, indent = 4, sort_keys=True)

    def load(self,filename):
        with open(filename,"r") as fp:
            data = json.load(fp)
        for objname in data:
            obj3d = Object3d.Object3d(objname)
            obj3d.from_dict(data[objname])
            self.add_object(objname,obj3d)

    def get_object(self,name):
        msg = f"object {name} not found in library"
        assert name in self.objects,"object with name not found"
        return self.objects[name]
