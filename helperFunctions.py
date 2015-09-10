# helperFunctions -- little things to make XLS debugging easier

# from xlrd import open_workbook
# from pyexcel_ods import get_data
# import json
# import sys
# import ast

def getSheet(workbook, name):
    return workbook[name]

def findColumnWithHeading(heading, whichSheet):
    """ returns the index of the column with the specified heading """

    for col, label in enumerate(whichSheet[0]):
        if label == heading:
            return col
    return None

# data = get_data(sys.argv[1])
# workbookString = json.dumps(data)
# workbookDict = ast.literal_eval(workbookString)
# 
# 
# print getSheet(workbookDict, 'choices')[0][:3]
# 
# print findColumnWithHeading('list name', getSheet(workbookDict, 'choices'))
