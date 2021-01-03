#!/usr/bin/python3
#
# fields.py
#
# Definitions for all the fields in ORM layer
#

from collections.abc import Iterable
from datetime import datetime

class Integer:   
    def __init__(self, blank=False, default=None, choices=None):

        self.baseDefault = 0
        self.blank = blank
        self.choices = choices

        if default != None:
            self.blank = True
            self.default = default
        else:
            self.default = self.baseDefault      

        if (default != None) and (isinstance(default, int) == False):
            raise TypeError("Default value is not the correct type.")

        if (choices != None):
            for choice in choices:
                if (isinstance(choice, int) == False):
                    raise TypeError("Choices value is not the correct type.")

        if (default != None) and (choices != None) and (default not in choices):
            raise TypeError("Default value is not found in choices")

    def setname(self, name):
        self.name = "_" + name

    def __set__(self, inst, value):
        if isinstance(value, int) == False:
            raise TypeError("Cannot set a non-int to Integer value")
        if self.choices != None and value not in self.choices:
            raise ValueError("Value not in choices")
        else:
            setattr(inst, self.name, value)

    def __get__(self, inst, cls):
        return getattr(inst, self.name)



class Float: 
    def __init__(self, blank=False, default=None, choices=None):

        self.baseDefault = 0
        self.blank = blank
        self.choices = choices

        if default != None:
            self.blank = True
            self.default = default
        else:
            self.default = self.baseDefault      

        if (default != None) and (isinstance(default, float) == False):
            raise TypeError("Default value is not the correct type.")

        if (choices != None):
            for choice in choices:
                if (isinstance(choice, float) == False):
                    raise TypeError("Choices value is not the correct type.")

        if (default != None) and (choices != None) and (default not in choices):
            raise TypeError("Default value is not found in choices")

    def setname(self, name):
        # print("Float setname: ", self.__dict__)
        self.name = "_" + name
        # print(self.name)

    def __set__(self, inst, value):
        if isinstance(value, float) == False and isinstance(value, int) == False:
            raise TypeError("Cannot set a non-int or non-float to Float value")
        if self.choices != None and value not in self.choices:
            raise ValueError("Value not in choices")
        else:
            # print("Float set: ", self.__dict__)
            setattr(inst, self.name, float(value))

    def __get__(self, inst, cls):
        return getattr(inst, self.name)


class String:
    def __init__(self, blank=False, default=None, choices=None):
        self.baseDefault = ""
        self.blank = blank
        self.choices = choices

        if default != None:
            self.blank = True
            self.default = default
        else:
            self.default = self.baseDefault        

        if (default != None) and (isinstance(default, str) == False):
            raise TypeError("Default value is not the correct type.")

        if (choices != None):
            for choice in choices:
                if (isinstance(choice, str) == False):
                    raise TypeError("Choices value is not the correct type.")

        if (default != None) and (choices != None) and (default not in choices):
            raise TypeError("Default value is not found in choices")


    def setname(self, name):
        # print("String setname: ", self.__dict__)
        self.name = "_" + name

    def __set__(self, inst, value):
        # print("String set: ", self.__dict__)
        if self.choices != None and value not in self.choices:
            raise ValueError("Value not in choices")
        else:
            setattr(inst, self.name, value)

    def __get__(self, inst, cls):
        return getattr(inst, self.name)


class Foreign:
    def __init__(self, table, blank=False):
        self.table = table
        self.blank = blank

    def setname(self, name):
        self.name = "_" + name

    def __set__(self, inst, value):
        if isinstance(value, self.table) == False and value != None:
            raise TypeError("Not setting valid table")
        else:
            setattr(inst, self.name, value)
        
    def __get__(self, inst, cls):
        # print("In foreign get attr")
        return getattr(inst, self.name)


class DateTime:
    # print("In field.DateTime")
    implemented = True #Change to True if doing custom

    def __init__(self, blank=False, default=None, choices=None):
        # print("ENTERED DATETIME INIT")
        # print(datetime.fromtimestamp(0))
        # deafultDatetime = datetime.fromtimestamp(0)
        self.baseDefault = datetime.fromtimestamp(0)
        self.blank = blank
        self.choices = choices

        if default != None:
          # print("Using provided default")
            self.blank = True
            if default.__name__ == 'now':
                self.default = datetime.now()
            # self.default = default
        else:
          # print("Using my default")
            self.default = self.baseDefault  
    

      # print("type of default is ", type(self.default))
        # print(isinstance(self.default, datetime))
        # if (default != None) and (isinstance(default, datetime) == False):
        #     raise TypeError("Default value is not the correct type.")

        if (choices != None):
            for choice in choices:
                if (isinstance(choice, datetime) == False):
                    raise TypeError("Choices value is not the correct type.")

        if (default != None) and (choices != None) and (default not in choices):
            raise TypeError("Default value is not found in choices")

    def setname(self, name):
        self.name = "_" + name

    def __set__(self, inst, value):
      # print("Values is ", value, "of type ", self.name)

        if not isinstance(value, datetime):
            raise TypeError("Must be of datetime type")


        if self.choices != None and value not in self.choices:
            raise ValueError("Value not in choices")
        else:
            # print("In set trying to set ", value)
            # print("inst is ", inst)
            setattr(inst, self.name, value)
            # print("Exit my sett")

    def __get__(self, inst, cls):
        return getattr(inst, self.name)


class Coordinate:
    # print("In field.Coordinate")
    implemented = True #Change to True if doing custom

    def __init__(self, blank=False, default=None, choices=None):
        # print("ENTERED COORDINATE INIT")
        # print("Self is ", self)
        # print("blank is ", blank)
        # print("default is ", default)
        # print("choices is ", choices)

        self.baseDefault = (0, 0)
        self.blank = blank
        self.choices = choices

        if default != None:
            self.blank = True
            self.default = default
        else:
            self.default = self.baseDefault        

        if (default != None) and (isinstance(default, tuple) == False):
            raise TypeError("Default value is not the correct type.")

        if (choices != None):
            for choice in choices:
                if (isinstance(choice, tuple) == False):
                    raise TypeError("Choices value is not the correct type.")

        if (default != None) and (choices != None) and (default not in choices):
            raise TypeError("Default value is not found in choices")

    def setname(self, name):
        # print("Name in setname is", name)
        self.name = "_" + name
        # if name == 'name':
        #     self.name = "_" + name
        # else:
        #     self.location_lat = "_" + name + "_lat"
        #     self.location_lon = "_" + name + "_lon"

    def __set__(self, inst, value):
        # help(self)
        # print(self.__dict__)
        # print("Value is", value)
        if (value[0] < -90 or value [0] > 90):
            raise ValueError("Not a valid coordinate")
        if (value[1] < -180 or value [1] > 180):
            raise ValueError("Not a valid coordinate")
        if not isinstance(value, tuple):
            raise TypeError("Coordinate must be 2-tuple")
        if self.choices != None and value not in self.choices:
            raise ValueError("Value not in choices")
        else:
            # print("In set trying to set ", value)
            # print("inst is ", inst)

            # print(type(value[0]))

            # print("----------Name is ", self.name)
            # print("----------Value is ", value)
            setattr(inst, self.name, value)


    def __get__(self, inst, cls):
        return getattr(inst, self.name)
