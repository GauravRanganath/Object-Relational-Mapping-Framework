#!/usr/bin/python3
#
# orm.py
#
# Definition for setup and export function
#

from .table import MetaTable
from .easydb import Database

"""
tb = (
    ("User", (                  # table_name
        ("firstName", str),     # (column_name, type)
        ("lastName", str),
        ("height", float),
        ("age", int),
    )),
    
    ("Account", (
        ("user", "User"),       # (column_name, table_reference)
        ("type", str),
        ("balance", float),
    )),
)
"""

MetaTable.tables.pop(0)
MetaTable.cols.pop(0)

# Return a database object that is initialized, but not yet connected.
#   database_name: str, database name
#   module: module, the module that contains the schema
def setup(database_name, module):

    # Check if the database name is "easydb".
    if database_name != "easydb":
        raise NotImplementedError("Support for %s has not implemented"%(
            str(database_name)))

    tableNames = (MetaTable.tables)

    colNames = MetaTable.cols
    tuple(colNames)

    tableList = tuple(zip(tableNames, colNames))
        
    newData = Database(tableList)
    
    return newData

# Return a string which can be read by the underlying database to create the 
# corresponding database tables.
#   database_name: str, database name
#   module: module, the module that contains the schema
def export(database_name, module): 

    # Check if the database name is "easydb".
    if database_name != "easydb":
        raise NotImplementedError("Support for %s has not implemented"%(
            str(database_name)))

    tableNames = (MetaTable.tables)

    colNames = MetaTable.cols
    tuple(colNames)

    tableList = tuple(zip(tableNames, colNames))

    exportStr = ""
    
    for elem in tableList:
        columnKeys = []
        columnVals = []
        columnDict = {}
        tableStr = ""

        tableStr = tableStr + (str(elem[0])) + " {" # table name

        for column in elem[1]: # cycle through columns in table
            columnKeys.append(column[0])
            tableStr = tableStr + " " + str(column[0])
            if column[1] == str:
                columnVals.append("string")
                tableStr = tableStr + " : string ;"
            elif column[1] == int:
                columnVals.append("integer")
                tableStr = tableStr + " : integer ;"
            elif column[1] == float:
                columnVals.append("float")
                tableStr = tableStr + " : float ;"
            else:
                columnVals.append(column[1])
                tableStr = tableStr + " : " + str(column[1]) + " ;"

        columnDict = dict(zip(columnKeys, columnVals))
        
        tableStr = tableStr + " } "

        exportStr = exportStr + tableStr

        #print(str(columnDict))
        #print(tableStr)
    # print(exportStr)

    # IMPLEMENT ME
    return exportStr

