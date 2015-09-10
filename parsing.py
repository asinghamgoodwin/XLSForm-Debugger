# parsing -- turning the choices sheet into a dictionary, survey sheet into Question objects

#from xlrd import open_workbook

from helperFunctions import getSheet, findColumnWithHeading
from questionClasses import *


def parseChoices(workbook, errorMessageList):
    """ parsing the choices sheet
    returns a dictionary containing all of the choice list names and their choices
    """

    choicesSheet = getSheet(workbook, 'choices')
    choicesDict = {} # all multiple choice lists stored here, in the format 'key' --> [list, of, values]

    list_nameNumber = findColumnWithHeading('list name', choicesSheet)
    nameNumber = findColumnWithHeading('name', choicesSheet)

    # makes a list that represents the list_name column, taking that element from ever row except for the 0th one (the one with the heading in it)
    list_nameColumn = [row[list_nameNumber] for row in choicesSheet[1:]]
    nameColumn = [row[nameNumber] for row in choicesSheet[1:]]

#######MAKE NEW HELPER FUNCTION######
    emptyRows = []
    for row, cell in enumerate(list_nameColumn):
        if cell == "":
            if nameColumn[row] == "":
                emptyRows.append(row)
            else:
                errorMessageList.append("ERROR: CHOICES  --  'list name' is blank in row "+str(row+2))
    emptyRows.sort()
    emptyRows.reverse()

    for row in emptyRows:
        list_nameColumn.pop(row)
        nameColumn.pop(row)

    for row, cell in enumerate(nameColumn):
        if cell == "":
            errorMessageList.append("ERROR: CHOICES  --  'name' is blank in row "+str(row+2))
#####END HELPER FUNCTION###

   # print "list_nameColumn is this long: "+str(len(list_nameColumn))
   # print list_nameColumn

    for row, list_name in enumerate(list_nameColumn):
        correspondingChoiceName = nameColumn[row]

        if list_name == "" or correspondingChoiceName == "":
            continue

        if list_name not in choicesDict.keys():
            choicesDict[list_name] = [correspondingChoiceName]
        else:
            # if the value is already in the list, warn about it
            if correspondingChoiceName in choicesDict[list_name]:
                errorMessageList.append("ERROR: CHOICES  --  "+str(correspondingChoiceName)+" listed twice as a choice for the list "+list_name)
            else:
                choicesDict[list_name].append(correspondingChoiceName)

    return choicesDict



#     for row, cell in enumerate(choicesSheet.col(list_nameNumber)):
#         value = cell.value
#         correspondingChoiceName = choicesSheet.col(nameNumber)[row].value
#         if value not in choicesDict.keys():
#             choicesDict[value] = [correspondingChoiceName]
#         else:
#             # if the value is already in the list, warn about it
#             if correspondingChoiceName in choicesDict[value]:
#                 errorMessageList.append("ERROR: CHOICES  --  "+str(correspondingChoiceName)+" listed twice as a choice for the list "+value)
#             else:
#                 choicesDict[value].append(correspondingChoiceName)
# 
#     return choicesDict
# 

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
    for r, row in enumerate(surveySheet):
        if r == 0:
            continue

        questionsList.append(Question(
            row=r, 
            questionType=row[questionTypeNumber], 
            name=row[nameNumber], 
            label=row[labelNumber]))
    return questionsList



#     for r in range(1,len(surveySheet)): 
#         row = surveySheet.row(r) #row is a list with all of the cells in that row
#         questionsList.append(Question(
#             row=r, 
#             questionType=row[questionTypeNumber].value, 
#             name=row[nameNumber].value, 
#             label=row[labelNumber].value))
#     return questionsList





