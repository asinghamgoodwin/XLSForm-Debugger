# this allows us to pass in files as arguments
import sys 
# allowing us to open an excel spreadsheet
from xlrd import open_workbook
import pudb

#print sys.argv[1] # <- just checking we got the right sheet

workbook = open_workbook(sys.argv[1], on_demand=True)
errorMessageList = []

# making sure that there is one sheet named 'survey' and one named 'choices'
def check4correctSheets():
    check4survey = False
    check4choices = False
    
    for sheet_name in workbook.sheet_names():
        if sheet_name == 'choices': check4choices = True
        if sheet_name == 'survey': check4survey = True
    
    if not check4survey or not check4choices:
        errorMessageList.append("Oops! You need to have one sheet named 'choices' and one sheet named 'survey'. Check to make sure that you have spelled both of those names correctly and that neither are capitalized.")
        return False
    else:
        print "You have the correct sheets and are good to go! Let's keep checking."
        return True

def findColumnWithHeading(heading, whichSheet):
    for c in range(whichSheet.ncols):
        if whichSheet.row(0)[c].value == heading:
            return c
    return None

# parsing the choices sheet
def parseChoices():
    choicesSheet = workbook.sheet_by_name('choices')
    choicesDict = {}
    #pu.db
    list_nameNumber = findColumnWithHeading('list name', choicesSheet)
    nameNumber = findColumnWithHeading('name', choicesSheet)
    #firstRow = choicesSheet.row(0)
    #for i in range(choicesSheet.ncols):
#        if firstRow[i] == 'list name':
#            list_nameNumber = i 
#
#        if firstRow[i].value == 'name':
#            nameNumber = i 
#
    #print list_nameNumber
    #print nameNumber
    
    for r, cell in enumerate(choicesSheet.col(list_nameNumber)):
        if cell.value not in choicesDict.keys():
            choicesDict[cell.value] = [choicesSheet.col(nameNumber)[r].value]
        else:
            # if the value is already in the list, warn about it
            if choicesSheet.col(nameNumber)[r].value in choicesDict[cell.value]:
                errorMessageList.append("Oops, it looks like you have the same choices listed twice for the list "+cell.value)
            else:
                choicesDict[cell.value].append(choicesSheet.col(nameNumber)[r].value)

    print choicesDict


class Question():
    def __init__(self, row, questionType, name, label):
        self.row = row
        self.questionType = questionType
        self.name = name
        self.label = label
        self.checked = False
        self.hasError = False
        self.errorMessage = None

    def check(self):
        pass

def getSheet(name):
    return workbook.sheet_by_name(name)

# making the Question objects and populating them
def parseQuestions():
    surveySheet = getSheet('survey')
    questionsList = []

    questionTypeNumber = findColumnWithHeading('type', surveySheet)
    nameNumber = findColumnWithHeading('name', surveySheet)
    labelNumber = findColumnWithHeading('label', surveySheet)
    for r in range(1,surveySheet.nrows): 
        row = surveySheet.row(r) #row is a list with all of the cells in that row
        questionsList.append(Question(
            row=r, 
            questionType=row[questionTypeNumber], 
            name=row[nameNumber], 
            label=row[labelNumber]))
    return questionsList
#pu.db
questionListForChecking = parseQuestions()
print len(questionListForChecking)
#parseChoices()







