#!/usr/bin/python3
"""Defines the HBNB"""
from shlex import split
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


def parsing(arg):
    curly_braces = find_curly_braces(arg)
    square_brackets = find_square_brackets(arg)

    if curly_braces is None:
        if square_brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            x = split(arg[:arg.find(square_brackets)])
            r = [i.strip(",") for i in x]
            r.append(square_brackets)
            return r
        else:
            x = split(arg[:arg.find(curly_braces)])
            r = [i.strip(",") for i in x]
            r.append(curly_braces)
            return r


def find_curly_braces(string):
    opening_brace = '{'
    closing_brace = '}'

    start_index = string.find(opening_brace)
    end_index = string.find(closing_brace, start_index + 1)

    if start_index != -1 and end_index != -1:
        return string[start_index:end_index + 1]
    else:
        return None


def find_square_brackets(string):
    opening_bracket = '['
    closing_bracket = ']'

    start_index = string.find(opening_bracket)
    end_index = string.find(closing_bracket, start_index + 1)

    if start_index != -1 and end_index != -1:
        return string[start_index:end_index + 1]
    else:
        return None


class HBNBCommand(cmd.Cmd):
    """Defines Hbnb cmd
    Attributes:
    prompt (str): The prompt.
    """

    prompt = "(hbnb) "
    __classes = {
            "BaseModel",
            "User",
            "Place",
            "City",
            "Amenity",
            "State",
            "Review"
    }


def default(self, arg):
    """Default for cmd"""
    ardic = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
    }
    matching = re.search(r"\.", arg)
    if matching is not None:
        ar = [arg[:matching.span()[0]], arg[matching.span()[1]:]]
        matching = re.search(r"\((.*?)\)", ar[1])
        if matching is not None:
            co = [ar[1][:matching.span()[0]], matching.group()[1:-1]]
            if co[0] in ardic.keys():
                ca = "{} {}".format(ar[0], co[1])
                return ardic[co[0]](ca)
            print("*** Unknown syntax: {}".format(arg))
            return False


def do_quit(self, arg):
    """command to exit the program"""
    return True


def do_EOF(self, arg):
    """exit the program."""
    print("")
    return True


def do_creat(self, arg):
    """Create a new class and print the id."""
    ar = parsing(arg)
    if len(ar) == 0:
        print("** class name missing **")
    elif ar[0] not in HBNBCommand.__classes:
        print("** class doesn't exist **")
    else:
        print(eval(ar[0])().id)
        storage.save()


def do_show(self, arg):
    """ Prints the string representation of an instance
    based on the class name and id"""
    ar = parsing(arg)
    serialized_objects = storage.all()
    if len(ar) == 0:
        print("** class name missing **")
    elif ar[0] not in HBNBCommand.__classes:
        print("** class doesn't exist **")
    elif len(ar) == 1:
        print("** instance id missing **")
    elif "{}.{}".format(ar[0], ar[1]) not in serialized_objects:
        print("** no instance found **")
    else:
        print(serialized_objects["{}.{}".format(ar[0], ar[1])])


def do_destroy(self, arg):
    """Deletes an instance based on the class name and id"""
    ar = parsing(arg)
    serialized_objects = storage.all()
    if len(ar) == 0:
        print("** class name missing **")
    elif ar[0] not in HBNBCommand.__classes:
        print("** class doesn't exist **")
    elif len(ar) == 1:
        print("** instance id missing **")
    elif "{}.{}".format(ar[0], ar[1]) not in serialized_objects.keys():
        print("** no instance found **")
    else:
        del serialized_objects["{}.{}".format(ar[0], ar[1])]
        storage.save()


def do_all(self, arg):
    """Prints all string representation of all instances
    based or not on the class name"""
    ar = parsing(arg)
    if len(ar) > 0 and ar[0] not in HBNBCommand.__classes:
        print("** class doesn't exist **")
    else:
        ob = []
        for j in storage.all().values():
            if len(ar) > 0 and ar[0] == j.__class__.__name__:
                ob.append(j.__str__())
            elif len(ar) == 0:
                ob.append(j.__str__())
        print(ob)


def do_count(self, arg):
    """gives the number of users thst have the same user name"""
    ar = parsing(arg)
    c = 0
    for ob in storage.all().values():
        if ar[0] == ob.__class__.__name__:
            c += 1
    print(c)


def do_update(self, arg):
    """Updates an instance based on the class name and id """
    ar = parsing(arg)
    serialized_objects = storage.all()

    if len(ar) == 0:
        print("** class name missing **")
        return False
    if ar[0] not in HBNBCommand.__classes:
        print("** class doesn't exist **")
        return False
    if len(ar) == 1:
        print("** instance id missing **")
        return False
    if "{}.{}".format(ar[0], ar[1]) not in serialized_objects.keys():
        print("** no instance found **")
        return False
    if len(ar) == 2:
        print("** attribute name missing **")
        return False
    if len(ar) == 3:
        try:
            type(eval(ar[2])) != dict
        except NameError:
            print("** value missing **")
            return False
    if len(ar) == 4:
        ob = serialized_objects["{}.{}".format(ar[0], ar[1])]
        if ar[2] in ob.__class__.__dict__.keys():
            vt = type(ob.__class__.__dict__[ar[2]])
            ob.__dict__[ar[2]] = vt(ar[3])
        else:
            ob.__dict__[ar[2]] = ar[3]
    elif type(eval(ar[2])) == dict:
        ob = serialized_objects["{}.{}".format(ar[0], ar[1])]
        for k, v in eval(ar[2]).items():
            if (k in ob.__class__.__dict__.keys() and
                    type(ob.__class__.__dict__[k]) in {str, int, float}):
                vt = type(ob.__class__.__dict__[k])
                ob.__dict__[k] = vt(v)
            else:
                ob.__dict__[k] = v
                storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
