import sys 
#from xlrd import open_workbook
from pyexcel_ods import get_data
import json
import ast
import pudb


from helperFunctions import getSheet, findColumnWithHeading
from parsing import parseChoices, parseQuestions
from sheetSetupChecking import (check4correctSheets, settingsSheetHasCorrectSetup,
        surveySheetHasCorrectSetup, choicesSheetHasCorrectSetup)
from questionClasses import *



def main():
    """ overall function, checks the spreadsheet and outputs the errors """

    #workbook = open_workbook(sys.argv[1], on_demand=True)
    data = get_data(sys.argv[1])
    workbookString = json.dumps(data)
    workbookDict = ast.literal_eval(workbookString)

    errorMessageList_setup = []
    errorMessageList_questions = []
    errorMessageList_choices = []

    print ""

    if not check4correctSheets(workbookDict, errorMessageList_setup):
        for error in errorMessageList_setup:
            print error
        print "FATAL ERROR  --  incorrect sheets in workbook"
        return False
    print "checking for correct worksheets.......................................OK!"

    # I wonder if it's ok to only have user input questions, and then no choices sheet or a blank one?
    # This definitely has to get checked and parsed before the survey questions can get checked
    if not choicesSheetHasCorrectSetup(workbookDict, errorMessageList_setup):
        for error in errorMessageList_setup:
            print error
        print "FATAL ERROR  --  choices could not be parsed"
        return False

    choicesDict = parseChoices(workbookDict, errorMessageList_choices)
    print "checking choices sheet setup..........................................OK!"

    if not surveySheetHasCorrectSetup(workbookDict, errorMessageList_setup):
        for error in errorMessageList_setup:
            print error
        print "FATAL ERROR  --  survey could not be parsed"
        return False
    questionsList = parseQuestions(workbookDict)
    print "checking survey sheet setup...........................................OK!"

    checkQuestions(questionsList, errorMessageList_questions)


    # This matters less so I put it below the other two so that they could still get checked if this fails
    if not settingsSheetHasCorrectSetup(workbookDict, errorMessageList_setup):
        for error in errorMessageList_setup:
            print error
        print "FATAL ERROR  --  survey could not be parsed"
        return False
    print "checking settings sheet setup.........................................N/A"

    print ""

    if len(errorMessageList_choices) > 0:
        for error in errorMessageList_choices:
            print error
            print ""

    if len(errorMessageList_questions) > 0:
        for error in errorMessageList_questions:
            print error
            print ""

    print "Enjoy your survey!....................................................OK!"
    print ""
    return True

##    # just for making sure it works right now:
##    print ""
##    print "there are "+str(len(questionsList))+" question objects in your list"
##    someKey = choicesDict.keys()[17]
##    print ""
##    print "here is a sample key-value pair from your choices dictionary: "+someKey+" -->"
##    print ""
##    print choicesDict[someKey]
##    print ""
##    print "the question on line 7 is of type "+questionsList[5].questionType+", has variable name "+questionsList[5].name+" and label "+questionsList[5].label
##    print ""
##    print errorMessageList
##    print ""
##    return errorMessageList


main()

