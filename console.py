import cmd
import sys
import re
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id"""
        if not arg:
            print("** class name missing **")
            return
        try:
            cls = eval(arg)
        except NameError:
            print("** class doesn't exist **")
            return
        new_instance = cls()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        try:
            value = storage.all()[key]
        except KeyError:
            print("** no instance found **")
            return
        print(value)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id (saves the change into the JSON file)"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        try:
            del storage.all()[key]
        except KeyError:
            print("** no instance found **")
            return
        storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances based or not on the class name"""
        if not arg:
            objects = storage.all().values()
        else:
            try:
                cls = eval(arg)
            except NameError:
                print("** class doesn't exist **")
                return
            objects = (obj for obj in storage.all().values() if isinstance(obj, cls))
        print([str(obj) for obj in objects])

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file)"""
        args = re.split(r'\s+', arg, maxsplit=3)
        if not args[0]:
            print("** class name missing **")
            return
        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        try:
            obj = storage.all()[key]
        except KeyError:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        setattr(obj, args[2], args[3])
        obj.save()

    def do_count(self, arg):
        """Counts the number of instances of a class"""
        try:
            cls = eval(arg)
        except NameError:
            print("** class doesn't exist **")
            return
        count = sum(1 for obj in storage.all().values() if isinstance(obj, cls))
        print(count)

    def default(self, line):
        """Method called on an input line when the command prefix is not recognized"""
        args = line.split('.', 1)
        if len(args) == 2:
            cls_name, method_call = args
            try:
                cls = eval(cls_name)
            except NameError:
                pass
            else:
                if method_call == "all()":
                    self.do_all(cls_name)
                elif method_call == "count()":
                    self.do_count(cls_name)
                else:
                    args = re.match(r"(\w+)\((.*)\)", method_call)
                    if args:
                        method, params = args.groups()
                        if method == "show":
                            self.do_show("{} {}".format(cls_name, params))
                        elif method == "destroy":
                            self.do_destroy("{} {}".format(cls_name, params))
                        elif method == "update":
                            params = re.split(r'\s*,\s*', params)
                            if len(params) == 3:
                                self.do_update("{} {} {} {}".format(
                                    cls_name, params[0], params[1], params[2]))
                            elif len(params) == 2:
                                self.do_update("{} {} {} {}".format(
                                    cls_name, params[0], *eval(params[1])))
    
if __name__ == '__main__':
    HBNBCommand().cmdloop()

