# this allows us to pass in files as arguments
import sys 
# for reading from an excel spreadsheet
from xlrd import open_workbook
# wow! a debugger!
import pudb


#workbook = open_workbook(sys.argv[1], on_demand=True)
#errorMessageList = [] # <-- will get filled with helpful error messages as we go along

########## helper functions ##########

def getSheet(workbook, name):
    return workbook.sheet_by_name(name)

def findColumnWithHeading(heading, whichSheet):
    """ returns the index of the column with the specified heading """

    for c in range(whichSheet.ncols):
        if whichSheet.row(0)[c].value == heading:
            return c
    return None

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


##################################### FILL THESE IN SOON #####################################
def choicesSheetHasCorrectSetup(workbook, errorMessageList):
    errorMessageList.append("ERROR:  --  Choices sheet setup error message here")
    return True

def surveySheetHasCorrectSetup(workbook, errorMessageList):
    errorMessageList.append("ERROR:  --  Survey sheet setup error message here")
    return True

def settingsSheetHasCorrectSetup(workbook, errorMessageList):
    errorMessageList.append("ERROR:  --  Settings sheet setup error message here")
    return True
##############################################################################################


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


class Question():
    def __init__(self, row, questionType, name, label):
        self.row = row
        self.questionType = questionType
        self.name = name
        self.label = label
        self.checked = False
        self.hasError = False
        self.errorMessage = None
        self.mandatoryColumns = None


class IntegerQuestion(Question):
    def check(self):
        pass


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

############################### FILL THIS IN SOON #####################################
questionTypeList = ['integer', 'decimal', 'text', 'select_one', 'select_multiple', 'note',
        'geopoint', 'geotrace', 'geoshape', 'date', 'time', 'dateTime', 'image', 'audio',
        'video', 'barcode', 'calculate', 'acknowledge']

metadataTypeList = ['start', 'end', 'today', 'deviceid', 'subscriberid', 'simserial', 'phonenumber']

# other lists and regex rules here to help with checking


def checkQuestions(questionsList):
    return True
#####################################################################################


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

