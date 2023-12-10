#!/usr/bin/python3
from model.bas_model import BaseModel
"""Defines the review class"""


class Review(BaseModel):
    """represents the review
    Attributes:
    place_id(str): the place id
    user_id(str): the user id
    text(str):the review text
    """
    place_id = ""
    user_id = ""
    text = ""
