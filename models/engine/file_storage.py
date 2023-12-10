#!/usr/bin/python3
# models/engine/file_storage.py


import json
from models.base_model import BaseModel
from os.path import exists


class FileStorage:
    __file_path = "file.json"
    __objects = {}
    MyClasses = {"BaseModel": BaseModel}

    def all(self):
        return FileStorage.__objects

    def new(self, obj):
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        serialized_objects = {}
        for key, obj in FileStorage.__objects.items():
            serialized_objects[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as jsonF:
            json.dump(serialized_objects, jsonF)

    def reload(self):
        try:
            with open(FileStorage.__file_path, encoding="utf-8") as jsonStr:
                deserialized = json.load(jsonStr)
                for obj_values in deserialized.values():
                    MyCls = obj_values["__class__"]
                    if isinstance(MyCls, str) and type(eval(MyCls)) == type:
                        self.new(eval(MyCls)(**obj_values))
        except FileNotFoundError:
            pass
