#!/usr/bin/python3
from models.base_model import BaseModel
"""deines the User class"""


class User(BaseModel):
    """represents the user
    Attributes:
    email(str): the email of the user
    password(str): the password of the user
    first_name(str): the first name of the user
    last_name(str): the last name of the user
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
