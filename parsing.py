# parsing -- turning the choices sheet into a dictionary, survey sheet into Question objects

from xlrd import open_workbook

from helperFunctions import *
from questionClasses import *


def parseChoices(workbook, errorMessageList):
    """ parsing the choices sheet
    returns a dictionary containing all of the choice list names and their choices
    """

    choicesSheet = workbook.sheet_by_name('choices')
    choicesDict = {} # all multiple choice lists stored here, in the format 'key' --> [list, of, values]

    list_nameNumber = findColumnWithHeading('list name', choicesSheet)
    nameNumber = findColumnWithHeading('name', choicesSheet)

    for row, cell in enumerate(choicesSheet.col(list_nameNumber)):
        value = cell.value
        correspondingChoiceName = choicesSheet.col(nameNumber)[row].value
        if value not in choicesDict.keys():
            choicesDict[value] = [correspondingChoiceName]
        else:
            # if the value is already in the list, warn about it
            if correspondingChoiceName in choicesDict[value]:
                errorMessageList.append("ERROR: CHOICES  --  "+str(correspondingChoiceName)+" listed twice as a choice for the list "+value)
            else:
                choicesDict[value].append(correspondingChoiceName)

    return choicesDict


def parseQuestions(workbook):
    """ making the Question objects and populating them """

    surveySheet = getSheet(workbook, 'survey')
    questionsList = []

    # figure out which columns are used in the survey sheet
    # make sure the question objects get those attributes added properly
    columnList = []

    questionTypeNumber = findColumnWithHeading('type', surveySheet)
    nameNumber = findColumnWithHeading('name', surveySheet)
    labelNumber = findColumnWithHeading('label', surveySheet)

    # starts at 1 because the 0th row is full of headings
    for r in range(1,surveySheet.nrows): 
        row = surveySheet.row(r) #row is a list with all of the cells in that row
        questionsList.append(Question(
            row=r, 
            questionType=row[questionTypeNumber].value, 
            name=row[nameNumber].value, 
            label=row[labelNumber].value))
    return questionsList





