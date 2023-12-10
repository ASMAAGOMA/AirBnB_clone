#!/usr/bin/python3
from models.base_model import BaseModel
"""Defines the place class"""


class Place(BaseModel):
    """represents the place
    Attributes:
    city_id(str): the city id
    user_id(string): the user id
    name(string): the place name
    description(string): the description of the place
    number_rooms(int): the number of rooms
    number_bathrooms(int): the number of bathrooms
    max_guest(int): maximum num of guests
    price_by_night(int): price by night
    latitude(float): latitude of the place
    longitude(float): longitude of the place
    amenity_ids(list): amenity ids
    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
