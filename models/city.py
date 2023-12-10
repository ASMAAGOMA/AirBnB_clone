#!/usr/bin/python3
from models.base_model import BaseModel
"""Defines the city class"""


class City(BaseModel):
    """represents the city
    Attributes:
    name(str): the name of the city
    state_id(str): state id
    """
    name = ""
    state_id = ""
