#!/usr/bin/python3
#
# table.py
#
# Definition for an ORM database table and its metaclass
#

# metaclass of table
# Implement me or change me. (e.g. use class decorator instead)

from .field import Integer, Float, String, Foreign, DateTime, Coordinate
import collections
from .easydb.packet import operator
from datetime import datetime

tableNames = []
colNames = []

class MetaTable(type):
    # print("Enter metatable init")
    def __init__(cls, name, bases, attrs):

        tableCols = []
        
        if name in tableNames:
            raise AttributeError("Table with duplicate definition.")
        else:
            tableNames.append(name)
        # print("TableNames are ", tableNames)

        # loop throught the keys of attrs
        for elem in attrs.keys():

            # if the element the key accesses is an object of any of the field classes declared in field.py ...
            if isinstance(attrs.get(elem), Integer) or isinstance(attrs.get(elem), Float) \
                or isinstance(attrs.get(elem), String) or isinstance(attrs.get(elem), Foreign) \
                or isinstance(attrs.get(elem), DateTime) or isinstance(attrs.get(elem), Coordinate):  
                # error checking for underscores
                if '_' in elem:
                    raise AttributeError("Field name has underscore.")
                # error checking for key words
                if elem == "pk" or elem == "version" or elem == "save" or elem == "delete":
                    raise AttributeError("Field name uses reserved word.")
                # the following elif statements check for individual field classes and appends the key and field type to a list
                elif isinstance(attrs.get(elem), Integer):
                    tableCols.append((elem, int))
                elif isinstance(attrs.get(elem), Float):
                    tableCols.append((elem, float))
                elif isinstance(attrs.get(elem), String):
                    tableCols.append((elem, str))
                # THIS IS WHAT I CANNOT FIGURE OUT
                elif isinstance(attrs.get(elem), Foreign):
                    # print("Elem is foreign")
                    field = attrs.get(elem)
                    tableCols.append((elem, field.table.__name__))
                elif isinstance(attrs.get(elem), Coordinate):
                    # print("elem is elem", elem)
                    tableCols.append((elem + '_lat', float))
                    tableCols.append((elem + '_lon', float))
                elif isinstance(attrs.get(elem), DateTime):
                    tableCols.append((elem, float))
        # appends to another list that includes the table name
        colNames.append(tableCols)
        
        for col, val in attrs.items():
            if isinstance(val, Integer):
                val.setname(col)                    
            elif isinstance(val, String):
                # print("In String setname")
                # print("Col is: ", col, ". Val is ", val)
                val.setname(col) 
            elif isinstance(val, Float):
                val.setname(col) 
            elif isinstance(val, Foreign):
                val.setname(col) 
            elif isinstance(val, Coordinate):
              #print("In Coordinate setname")
                # col = col + "LatLon"
              #print("Col is: ", col, ". Val is ", val)
                val.setname(col)
                # val.setname(col + '_lat') 
                # val.setname(col + '_lon') 
            elif isinstance(val, DateTime):
              #print("In datetime setname")
              #print("Col is: ", col, ". Val is ", val)
                val.setname(col) 

    tables = tableNames
    cols = colNames
    # print("Exit matetable init")
    # Returns an existing object from the table, if it exists.
    #   db: database object, the database to get the object from
    #   pk: int, primary key (ID)

    # def __getattribute__(self, name):
    #     val = super().__getattribute__(name)
    #     if name != "__dict__" and name.startswith("_"):
    #         # print (name + "is a private member")
    #         pass
    #     return val
    def __iter__(cls):
        for attr in dir(cls):
            if not attr.startswith("__"):
                yield attr

    def __getattribute__(self, name):

        keyWords = 'save', 'delete'
        if name in keyWords:
            # Not a data member
            pass
        else:
            return object.__getattribute__(self, name)

    # def __repr__(self):
    #     return("This a a Metatable repr")



    def get(cls, db, pk):
        # print("ENTERED GET")
        # print("db is :", db)
        # print("pk is :", pk)
        # print("cls is :", cls)

        # print("Class bases are: ", cls.__bases__)
        # print(db.tables)

        # help(cls)


        tableName = cls.__name__
        # print("Table Name is :", tableName)
        # print("Class items: ", cls.__dict__.items())

        values, versionID = db.get(tableName, pk)
        # print("Values: ", values)
        # print("version: ", versionID)

        objFromTable = cls(db)


        columns = {}
        columns.clear()
        i = 0
        for column in cls.__dict__.items():
            if not column[0].startswith("_"):


              #print("Column is ", column)
                # print("Type of column is", type(cls.__getattribute__(column[0])))
                field = cls.__getattribute__(column[0])
                

                if isinstance(field, (int, Integer)):
                    # print("This is an Integer column")
                    # print("Field name is ", column[0])
                    # print("Value is ", values[i])
                    columns[column[0]] = values[i]

                elif isinstance(field, (float, Float)):
                    # print("This is an Float column")
                    # print("Field name is", column[0])
                    # print("Value is ", values[i])
                    columns[column[0]] = values[i]
                
                elif isinstance(field, (str, String)):
                    # print("This is an String column") 
                    # print("Field name is", column[0])
                    # print("Value is ", values[i])
                    columns[column[0]] = values[i]

                elif isinstance(field, DateTime):
                    # print("This is an DateTime column")
                    # print("Field name is", column[0])
                    # print("Value is ", values[i])

                    valueProcessed = datetime.fromtimestamp(values[i])
                  #print(valueProcessed)


                    columns[column[0]] = valueProcessed

                    
                elif isinstance(field, Coordinate):
                    # print("This is an Coordinate column") 
                    # print("Field name is", column[0])
                    # print("Value is ", values[i], " and ", values[i+1])
                    fullCoordinate = (float(values[i]), float(values[i+1]))
                    # print(fullCoordinate)
                    columns[column[0]] = fullCoordinate    
                    i = i+1              
                                
                elif isinstance(field, Foreign):
                    # print("This is an Foreign column")
                    # print("User ID is ", values[i])

                    # print("Field is ", field)
                    # print(cls.user.table)

                    innerTableID = values[i]
                    innerTableName = field.table.__name__
                    # print("Inner table name", innerTableName)
                    innerObject = MetaTable.get(field.table, db, innerTableID)

                    # print("Inner object is ", innerObject.__dict__)

                    if (innerTableName.lower()) == 'user':
                        setattr(objFromTable, innerTableName.lower(), innerObject)
                    elif (innerTableName.lower()) == 'city':
                        setattr(objFromTable, 'location', innerObject)

                    # print("Object after foreign ", objFromTable.__dict__)
                
                else: #elif isinstance(field, user class)
                    # print("This is an User column") 
                    # print("User ID is ", values[i])
                    # print("Field is ", field)
                    # print(cls.user.table)

                    innerTableID = values[i]
                    innerObject = MetaTable.get(field, db, innerTableID)

                    innerTableName = field.__name__
                    # print(innerTableName)
                    # print(innerObject)
                    setattr(objFromTable, innerTableName.lower(), innerObject)
                    # cls.user = innerObject

                i = i + 1
            # else:
            #     print(column[0])
        # print(columns)

        for key in columns:
            setattr(objFromTable, key, columns[key])

        objFromTable.pk = pk
        objFromTable.version = versionID
        # print("Leaving get with: ", objFromTable.__dict__)
        # print("EXITING GET")
        return objFromTable

    # Returns a list of objects that matches the query. If no argument is given,
    # returns all objects in the table.
    # db: database object, the database to get the object from
    # kwarg: the query argument for comparing
    def filter(cls, db, **kwarg):
        # print("ENTERED FILTER")
        # help(cls)
        # print(cls.__getattribute__(cls.__name__))

        # print(type(db))

        tableName = cls.__name__
        # print("Table Name is :", tableName)

        # print("Args are: ", kwarg)
        if not bool(kwarg):
            # print("No arguments")
            rowIDs = db.scan(tableName, operator.AL)
        else:
            rawQuery = list(kwarg.keys())[0]
            # print(rawQuery)

            value = list(kwarg.values())[0]
            # print(value)
            

            if "__" in rawQuery:
                # print("Has an op")
                columnName, opString = rawQuery.split("__")
            else:
                # print("No op so use eq")
                columnName = rawQuery
                opString = 'eq'

            # print(columnName, opString)


            if opString == 'eq':
                op = operator.EQ
            elif opString == 'ne':
                op = operator.NE
            elif opString == 'lt':
                op = operator.LT
            elif opString == 'gt':
                op = operator.GT
            else:
                raise AttributeError("Operation not supported")

            validColumnNames = []
            for table in cls.cols:
                # print(table)
                for column in table:
                    # print(column[0])
                    validColumnNames.append(column[0])

            validColumnNames.append('id')
            # print(validColumnNames)

            formattedTableNames = []
            for name in tableNames:
                formattedTableNames.append(name.lower())

            # print("table names is ", formattedTableNames)

            if columnName in formattedTableNames:
                # print("Its a table name")
                # if not isinstance(value, type(columnName)):
                #     columnName = 'id'
                if isinstance(value, int):
                    columnName = 'id'
                elif isinstance(value, (float, str)):
                    pass
                else:
                    columnName = 'id'

            # print(value)
            if isinstance(value, (int, Integer)):
                # print("This is an Integer value")
                # print("columnName in is", columnName)
                # print("tableName in is", tableName)
                # print("value in is", value)
                rowIDs = db.scan(tableName, op, columnName, value)               
                pass

            elif isinstance(value, (float, Float)):
                # print("This is an Float value")
                # print("columnName in is", columnName)
                # print("tableName in is", tableName)
                # print("value in is", value)
                rowIDs = db.scan(tableName, op, columnName, value)                  
                pass
            
            elif isinstance(value, (str, String)):
                # print("This is an String value")
                # print("columnName in is", columnName)
                # print("tableName in is", tableName)
                # print("value in is", value)
                rowIDs = db.scan(tableName, op, columnName, value)               #  
                pass

            elif isinstance(value, datetime):
                # print("This is an DateTime value")
                # print("columnName in is", columnName)
                # print("tableName in is", tableName)
                # print("value in is", value)
                posixValue = value.timestamp()
                # print(posixValue)


                rowIDs = db.scan(tableName, op, columnName, posixValue)    
                # print(rowIDs)               
                pass

            elif isinstance(value, tuple):
                # print("This is an Coordinate value") 
                columnName = 'location_lat'  
                latVal = value[0]
                if (latVal < 0 ):
                    if op == operator.GT :
                        op = operator.LT
                    elif op == operator.LT:
                        op = operator.GT

                # print("columnName in is", columnName)
                # print("tableName in is", tableName)
                # print("value in is", value)
                latRowIDs = db.scan(tableName, op, columnName, latVal)
                # print("Lat row IDS", latRowIDs)

                columnName = 'location_lon'  
                lonVal = value[1]
                if (lonVal < 0 ):
                    if op == operator.GT :
                        op = operator.LT
                    elif op == operator.LT:
                        op = operator.GT                

                # print("columnName in is", columnName)
                # print("tableName in is", tableName)
                # print("value in is", value)
                lonRowIDs = db.scan(tableName, op, columnName, lonVal)
                # print("lon rowIDs ", lonRowIDs)

                if op == operator.EQ:
                    rowIDs = []
                    for id in lonRowIDs:
                        if id in latRowIDs:
                            rowIDs.append(id)
                    rowIDs = list(set(rowIDs))                            
                else:
                    rowIDs = set(latRowIDs + lonRowIDs)
                    rowIDs = list(rowIDs)
                
                
                # print(rowIDs)


                pass                 
                            
            elif isinstance(value, Foreign):
                # print("This is an Foreign value")
                # print("columnName in is", columnName)
                # print("tableName in is", tableName)
                # print("value in is", value)
                rowIDs = db.scan(tableName, op, columnName, value)

                pass
            
            else: 
                # print("Value goes into else")
                # help(value)
                # print(value.pk)
                # objectInForeign = MetaTable.get(cls, db, value.pk)
                # print(objectInForeign.id)
                value = value.pk
                # print("columnName in is", columnName)
                # print("tableName in is", tableName)
                # print("value in is", value)
                rowIDs = db.scan(tableName, op, columnName, value)                
                


            # print("Type of column is ", type(columnName))
            # print("Type of value is ", type(value))

            # # print("Testing type is ", type(Foreign))
            # # if isinstance(value, Foreign):
            # #     print("Valus is a Foreign")
            # # else:
            # #     print("NOPEEEE")


            # # if columnName not in validColumnNames:
            # #     raise AttributeError("Unknown Field")

            # # print("Operator in is", op)
            # print("columnName in is", columnName)
            # print("tableName in is", tableName)
            # print("value in is", value)
            # rowIDs = db.scan(tableName, op, columnName, value)
  
        # print("rowIDs are ", rowIDs)
        objectsFromQuery = []
        for id in rowIDs:
            # print("id is ", id)
            currentObj = MetaTable.get(cls, db, id)

            # currentObj = db.get(tableName, id)
            # print("Obj from get ", currentObj)
            # print(type(currentObj))

            # inst = cls(db)

            # print(inst)
            # help(currentObj)
            # print(currentObj.__name__)
            # print(type(currentObj))

            # print(dir(currentObj))
            # print(cls.__getattribute__(currentObj.__name__))
            
            # print(currentObj.__dict__)
            # print(type(currentObj))
            # help(currentObj)

            # currentObj = db.get(tableName, id)
            # print(currentObj)
            # print(currentObj.__name__)
            # print(cls.__getattribute__(tableName))
            
            # help(currentObj)
            # objectsFromQuery.append(inst)
            objectsFromQuery.append(currentObj)
            # print(objectsFromQuery)

        # print("EXITED FILTER")
        return objectsFromQuery

    # Returns the number of matches given the query. If no argument is given, 
    # return the number of rows in the table.
    # db: database object, the database to get the object from
    # kwarg: the query argument for comparing
    def count(cls, db, **kwarg):
        # print("ENTERED COUNT")

        tableName = cls.__name__
        # print("Table Name is :", tableName)

        # print("Args are: ", kwarg)
        if not bool(kwarg):
            # print("No arguments")
            rowIDs = db.scan(tableName, operator.AL)
            return len(rowIDs)

        rawQuery = list(kwarg.keys())[0]
        # print(rawQuery)

        value = list(kwarg.values())[0]
        # print(value)

        if "__" in rawQuery:
            # print("Has an op")
            columnName, opString = rawQuery.split("__")
        else:
            # print("No op so use eq")
            columnName = rawQuery
            opString = 'eq'

        # print(columnName, opString)

        if opString == 'al':
            op = operator.AL
        elif opString == 'eq':
            op = operator.EQ
        elif opString == 'ne':
            op = operator.NE
        elif opString == 'lt':
            op = operator.LT
        elif opString == 'gt':
            op = operator.GT
        elif opString == 'le':
            op = operator.LE
        elif opString == 'ge':
            op = operator.GE
        else:
            raise AttributeError("Operation not supported")
        
        # print(dir(cls))

        # help(cls)

        # print(cls.cols)
        validColumnNames = []
        for table in cls.cols:
            # print(table)
            for column in table:
                # print(column[0])
                validColumnNames.append(column[0])

        validColumnNames.append('id')
        # print(validColumnNames)

        if columnName not in validColumnNames:
            raise AttributeError("Unknown Field")

        rowIDs = db.scan(tableName, op, columnName, value)



        # rowIDs = db.scan(tableName, operator.EQ, )
        # scan(self, table_name, op, column_name=None, value=None):
        # print("EXITED COUNT")
        return len(rowIDs)

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return collections.OrderedDict()

# table class
# Implement me.
class Table(object, metaclass=MetaTable):

    def __init__(self, db, **kwargs):
        # print("Entered table init")
        self._tableName = self.__class__.__name__
        # print("In init, self._name is ", self._tableName)
        self._db = db

        # CHECK FOR REQUIRED ARGUMENTS        
        tableClass = vars(self.__class__)
        requiredArguments = []
        
        for attr in tableClass: 
            val = tableClass.get(attr)
            # print("Val is ", val)
            if self.isField(val) == True:
                if val.blank == False: # if the value cannot be blank it's a required argument
                    requiredArguments.append(attr)
                if val.blank == True and attr not in kwargs.keys(): # set default value if argument is not specified
                    # print("Attr is ", attr)
                    setattr(self, attr, val.default)

        if (bool(kwargs)):
            for arg in requiredArguments:
                if arg not in kwargs.keys():
                    raise AttributeError("Missing required argument")

        # SET COLUMNS AND VALUES FOR ARGUMENTS PASSED IN
        for col, val in kwargs.items():
            # print("Col and val to populate are ", col , ", ", val)
            setattr(self, col, val)


        self.pk = None      # id (primary key)
        self.version = None # version
        # print("Dict in init ", self.__dict__)
        # print("Exit table init")

        # FINISH ME

    # Save the row by calling insert or update commands.
    # atomic: bool, True for atomic update or False for non-atomic update
    def save(self, atomic=True):
        # print("Entered save")

        insertCol = []
        insertColVals = []


        for tableName, columns in self._db.tables: # store columns of table into list
            # print("Self._name is ", self._tableName)
            # print("Self is ", self)
            # print(self.__dict__)
            # print("tableName is ", tableName)
            # print("columns is ", columns)
            if self._tableName == tableName:
                insertCol = columns

        # print("Insert col is", insertCol)

        for col, val in insertCol: # get the values of the columns from the object and store them into a list
            if self.checkForeign(col, val) == True:
                obj = getattr(self, col)
                if obj.pk is None:
                    obj.save()  # cascade save it first
                insertColVals.append(obj.pk)
            
            else:
                # print("Get col ", col)
                # Coordinate
                if col == 'location_lat':
                    col = 'location'
                    latValue = getattr(self, col)
                    # print(latValue[0])
                    insertColVals.append(latValue[0])
                elif col == 'location_lon':
                    col = 'location'
                    latValue = getattr(self, col)
                    # print(latValue[1])
                    insertColVals.append(latValue[1])

                # Datetime
                elif col == 'start':
                    value = getattr(self, col)
                    # print("Start value: ", value)
                    valueToStore = value.timestamp()
                    # print(valueToStore)
                    insertColVals.append(valueToStore)
                elif col == 'end':
                    value = getattr(self, col)
                    # print("End value: ", value)
                    valueToStore = value.timestamp()
                    # print(valueToStore)
                    insertColVals.append(valueToStore)

                # Other Fields                
                else:
                    insertColVals.append(getattr(self, col))

        if self.pk == None: # print out the values I'm sending into insert
            # print("Inserting: ", self._tableName, insertColVals)
            self.pk, self.version = self._db.insert(str(self._tableName), insertColVals)

        elif self.pk != None and atomic == True:
            self.version = self._db.update(str(self._tableName), self.pk, insertColVals, self.version)

        elif self.pk != None and atomic == False:
            self.version = self._db.update(str(self._tableName), self.pk, insertColVals)
        
        # print("Exit save")
    # Delete the row from the database.
    def delete(self):
        self._db.drop(str(self._tableName), self.pk)   
        self.pk = None
        self.version = None     


    def isField(self, val):
        if isinstance(val, Integer) or isinstance(val, String) or isinstance(val, Float) or isinstance(val, Foreign) \
        or isinstance(val, DateTime) or isinstance(val, Coordinate):
            return True
        else:
            return False

    def checkForeign(self, col, val):
        table = self.__class__
        field = table.__dict__.get(col)
        # print(field)
        if isinstance(field, Foreign):
          # print(str(col) + " " + str(val) + " is Foreign")
            return True
        