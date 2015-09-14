# sheetSetupChecking -- checking the workbook for correct sheets, & sheets for correct columns

# from xlrd import open_workbook

from helperFunctions import getSheet, findColumnWithHeading

def check4correctSheets(workbook, errorMessageList):
    """ making sure that there is one sheet named 'survey' and one named 'choices'
    if there isn't, this function returns false
    (which will halt the whole checking process)
    """

    check4survey = False
    check4choices = False
    
    for sheet_name in workbook.keys():
        if sheet_name == 'choices': check4choices = True
        if sheet_name == 'survey': check4survey = True
    
    if not check4survey:
        errorMessageList.append("ERROR: SHEET NAMES  --  need one sheet named 'survey'")
    if not check4choices:
        errorMessageList.append("ERROR: SHEET NAMES  --  need one sheet named 'choices'")
    if not check4survey or not check4choices:
        return False
    else:
        return True


def choicesSheetHasCorrectSetup(workbook, errorMessageList):
    errorMessageList.append("ERROR: SETUP  --  Choices sheet error message")
    return True


def surveySheetHasCorrectSetup(workbook, errorMessageList):
    errorMessageList.append("ERROR: SETUP  --  Survey sheet error message")

    #for heading in surveySheet[0]:
    #    if heading not in possibleColumns:
    #        errorMessageList.append("ERROR
    return True


def settingsSheetHasCorrectSetup(workbook, errorMessageList):
    errorMessageList.append("ERROR: SETUP  --  settings sheet error message")
    return True
