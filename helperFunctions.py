# helperFunctions -- little things to make XLS debugging easier
from xlrd import open_workbook


def getSheet(workbook, name):
    return workbook.sheet_by_name(name)

def findColumnWithHeading(heading, whichSheet):
    """ returns the index of the column with the specified heading """

    for c in range(whichSheet.ncols):
        if whichSheet.row(0)[c].value == heading:
            return c
    return None
