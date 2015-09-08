import sys 
from xlrd import open_workbook
import pudb

from helperFunctions import *
from parsing import *
from sheetSetupChecking import *
from questionClasses import *



def main():
    """ overall function, checks the spreadsheet and outputs the errors """

    workbook = open_workbook(sys.argv[1], on_demand=True)
    errorMessageList = [] # <-- will get filled with helpful error messages as we go along

    if check4correctSheets(workbook, errorMessageList) == False:
        return errorMessageList

    # I wonder if it's ok to only have user input questions, and then no choices sheet or a blank one?
    # This definitely has to get checked and parsed before the survey questions can get checked
    if choicesSheetHasCorrectSetup(workbook, errorMessageList):
        choicesDict = parseChoices(workbook, errorMessageList)
    else:
        return errorMessageList

    if surveySheetHasCorrectSetup(workbook, errorMessageList):
        questionsList = parseQuestions(workbook)
    else:
        return errorMessageList

    checkQuestions(questionsList)

    # This matters less so I put it below the other two so that they could still get checked if this fails
    if settingsSheetHasCorrectSetup(workbook, errorMessageList):
        pass # <--- make a settings parser function
    else:
        return errorMessageList

    # just for making sure it works right now:
    print ""
    print "there are "+str(len(questionsList))+" question objects in your list"
    someKey = choicesDict.keys()[17]
    print ""
    print "here is a sample key-value pair from your choices dictionary: "+someKey+" -->"
    print ""
    print choicesDict[someKey]
    print ""
    print "the question on line 7 is of type "+questionsList[5].questionType+", has variable name "+questionsList[5].name+" and label "+questionsList[5].label
    print ""
    print errorMessageList
    print ""
    return errorMessageList


main()

