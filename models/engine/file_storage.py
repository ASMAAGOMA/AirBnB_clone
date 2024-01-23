#!/usr/bin/python3
"""File storage"""
# models/engine/file_storage.py

import json
from os.path import exists
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """File Storage class for managing storage of BaseModel instances"""

    __file_path = "file.json"
    __objects = {}
    MyClasses = {"BaseModel": BaseModel, "User": User, "Place": Place,
                 "Amenity": Amenity, "City": City, "Review": Review,
                 "State": State}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Add a new object to the dictionary __objects."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize and save the objects to the file."""
        serialized_objects = {}
        for key, obj in FileStorage.__objects.items():
            serialized_objects[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as json_file:
            json.dump(serialized_objects, json_file)

    def reload(self):
        """Deserialize and load the objects from the file."""
        try:
            with open(FileStorage.__file_path, encoding="utf-8") as json_file:
                deserialized = json.load(json_file)
                for obj_values in deserialized.values():
                    my_cls = obj_values["__class__"]
                    if isinstance(my_cls, str) and type(eval(my_cls)) == type:
                        self.new(eval(my_cls)(**obj_values))
        except FileNotFoundError:
            pass
