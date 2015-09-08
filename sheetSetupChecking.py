# sheetSetupChecking -- checking the workbook for correct sheets, & sheets for correct columns

from xlrd import open_workbook

from helperFunctions import *

def check4correctSheets(workbook, errorMessageList):
    """ making sure that there is one sheet named 'survey' and one named 'choices'
    if there isn't, this function returns false
    (which will halt the whole checking process)
    """

    check4survey = False
    check4choices = False
    
    for sheet_name in workbook.sheet_names():
        if sheet_name == 'choices': check4choices = True
        if sheet_name == 'survey': check4survey = True
    
    if not check4survey or not check4choices:
        errorMessageList.append("ERROR: SHEET NAMES  -- you must have one sheet named 'choices' and one sheet named 'survey'")
        return False
    else:
        return True


def choicesSheetHasCorrectSetup(workbook, errorMessageList):
    errorMessageList.append("ERROR:  --  Choices sheet setup error message here")
    return True


def surveySheetHasCorrectSetup(workbook, errorMessageList):
    errorMessageList.append("ERROR:  --  Survey sheet setup error message here")
    return True


def settingsSheetHasCorrectSetup(workbook, errorMessageList):
    errorMessageList.append("ERROR:  --  Settings sheet setup error message here")
    return True
