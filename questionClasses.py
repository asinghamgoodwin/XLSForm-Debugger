# questionClasses -- each question type gets its own class, all have check methods


questionTypeList = ['integer', 'decimal', 'text', 'select_one', 'select_multiple',
        'note', 'geopoint', 'geotrace', 'geoshape', 'date', 'time', 'dateTime',
        'image', 'audio', 'video', 'barcode', 'calculate', 'acknowledge']

metadataTypeList = ['start', 'end', 'today', 'deviceid', 'subscriberid',
        'simserial', 'phonenumber']


possibleColumns = ['appearance', 'type', 'name', 'label', 'constraint', 
    'constraint_message', 'required', 'relevant', 'repeat_count', 'calculation', 'hint']

class Question():
    def __init__(self, row, appearance, questionType, name, label, constraint,
            constraint_message, required, relevant, repeat_count, calculation, hint):
        self.row = row

        self.appearance = appearance
        self.questionType = questionType
        self.name = name
        self.label = label
        self.constraint = constraint
        self.constraint_message = constraint_message
        self.required = required
        self.relevant = relevant
        self.repeat_count = repeat_count
        self.calculation = calculation
        self.hint = hint

        self.checked = False
        self.hasError = False
        self.errorMessages = []
        self.mandatoryColumns = None

    def check(self, priorQuestionsList, choicesDict):
        # check that type makes sense
        # meaning: (appropriate type) __ (from choice list) __ (or_other)
        if self.questionType == "":
            self.errorMessages.append("ERROR: QUESTION "+str(self.row)+"  --  blank type not allowed")
            self.hasError = True
            return False

        splitType = self.questionType.split()
        if splitType[0] == "begin" or splitType[0] == "end" or splitType[0] == "note":
            return True

        if splitType[0] not in questionTypeList and splitType[0] not in metadataTypeList:
            self.errorMessages.append("ERROR: QUESTION "+str(self.row)+"  --  invalid type")
            self.hasError = True
            return False

        if len(splitType) > 1:
            if splitType[0] != "select_one" and splitType[0] != "select_multiple":
                self.errorMessages.append("ERROR: QUESTION "+str(self.row)+"  --  "+splitType[0]+" takes no choice list")
            else:
                if splitType[1] not in choicesDict:
                    self.errorMessages.append("ERROR: QUESTION "+str(self.row)+"  -- nonexistent choices list")

        if len(splitType) > 2 and splitType[1] != "select_one" and splitType[1] != "select_multiple" and splitType[2] != "or_other":
            self.errorMessages.append("ERROR: QUESTION "+str(self.row)+"  -- too many arguments for type")


        # check that name is ok, unique 
        if self.name == "":
            self.errorMessages.append("ERROR: QUESTION "+str(self.row)+"  --  blank name not allowed")

        if " " in self.name: # TO DO!!! check on rules like starting with a number
            self.errorMessages.append("ERROR: QUESTION "+str(self.row)+"  --  no space allowed in name")

        for question in priorQuestionsList:
            if question.name == self.name:
                self.errorMessages.append("ERROR: QUESTION "+str(self.row)+"  --  same name as question "+str(question.row))
                break

        # check that label isn't empty
        if self.questionType not in metadataTypeList and self.questionType != "calculate":
            if self.label == "":
                self.errorMessages.append("ERROR: QUESTION "+str(self.row)+"  --  blank label not allowed")

        # setting self.hasError if applicable
        if len(self.errorMessages) > 0:
            self.hasError = True

class IntegerQuestion(Question):
    def check(self):
        pass



##########################################################
def checkQuestions(questionsList, errorMessageList, choicesDict):
    for num, question in enumerate(questionsList):
        question.check(questionsList[:num], choicesDict)

    for question in questionsList:
        if question.hasError:
            errorMessageList += question.errorMessages
    return True


