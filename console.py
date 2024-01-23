#!/usr/bin/python3
"""Defines the HBNB"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parsing(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    square_brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if square_brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            x = split(arg[:square_brackets.span()[0]])
            r = [i.strip(",") for i in x]
            r.append(square_brackets.group())
            return r
    else:
        x = split(arg[:curly_braces.span()[0]])
        r = [i.strip(",") for i in x]
        r.append(curly_braces.group())
        return r


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

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

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

<<<<<<< HEAD
    def do_creat(self, arg):
=======
    def do_create(self, arg):
>>>>>>> be494269ffe5a05bde9ebb12a0cece7acc7546ba
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
<<<<<<< HEAD
        """ Prints the string representation of an instance
        based on the class name and id"""
=======
        """ Prints the string representation of
        an instance based on the class name and id"""
>>>>>>> be494269ffe5a05bde9ebb12a0cece7acc7546ba
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
<<<<<<< HEAD
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
=======
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
>>>>>>> be494269ffe5a05bde9ebb12a0cece7acc7546ba

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
