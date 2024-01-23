#!/usr/bin/python3

import uuid
from datetime import datetime


class BaseModel:
    """BaseModel class representing the base model for other classes."""

    def __init__(self, *args, **kwargs):
        """Initialize a new instance of BaseModel.

        Args:
            args: Variable-length argument list.
            kwargs: Variable-length keyword argument list.
        """
        from models import storage
        if kwargs:
            for key, value in kwargs.items():
                date_form = "%Y-%m-%dT%H:%M:%S.%f"
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.strptime(value, date_form))
                elif key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Return a string representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Save the BaseModel instance and update the
        'updated_at' attribute."""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert the BaseModel instance to
        a dictionary format for serialization.

        Returns:
            dict: Dictionary representation of the BaseModel instance.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
