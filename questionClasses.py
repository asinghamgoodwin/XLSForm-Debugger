# questionClasses -- each question type gets its own class, all have check methods


questionTypeList = ['integer', 'decimal', 'text', 'select_one', 'select_multiple',
        'note', 'geopoint', 'geotrace', 'geoshape', 'date', 'time', 'dateTime',
        'image', 'audio', 'video', 'barcode', 'calculate', 'acknowledge']

metadataTypeList = ['start', 'end', 'today', 'deviceid', 'subscriberid',
        'simserial', 'phonenumber']



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



##########################################################
def checkQuestions(questionsList):
    return True
