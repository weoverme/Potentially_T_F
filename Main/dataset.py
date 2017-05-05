from Main.PolitiFactWrapper import *
from Main.twitter_observer import *

"""
    data set is made up of a list of two things:
    the data, and
    the classified value.

    For the Training set, this will be a tuple, as it the training set mustn't have the data modified.

    Whenever classification is being done during Training, the classification value
    (1 for Verifiable, -1 for Not-Verifiable), with a default value of 0)
    this value will be checked against the actual value of the data.

    For the Testing set, the classified value will not have a value at first; the classifier will be giving it a value.
    However, to validate the testing set, human-checking will be required.

    """

class TrainingSet:

    def __init__(self):
        self.set_ = []

    def add_to_set(self, dataObj):
        self.set_.append(dataObj)
        return

    def get_training_data_set(self):
        return self.set_

class TestingSet:
    def __init__(self):
        self.set_ = []

    def add_to_set(self, dataObj):
        self.set_.append(dataObj)

    def get_testing_data_set(self):
        return self.set_

    def classify_data(self, dataObj, value=0):
        try:
            if value != 1 or value != -1:
                raise Exception InvalidClassificationValue
            dataObj.set_classification(value)

        except InvalidClassificationValue:
            message = "Enter a valid classification value 1 or -1"

        return message


class AbstractData:
    def __init__(self, statement):
        self.__statement = statement
        self.__classification = 0

    def set_classification(self, value):
        pass

class TrainingData(AbstractData):
    def __init__(self, statement):
        super.__init__(statement)
        self.__classified = False

    def set_classification(self, value):
        #cannot classify again
        if not self.classified:
            self.classification = value
            self.classified = True


class TestingData(AbstractData):
    def __init__(self, statement):
        super.__init__(statement)

    def set_classification(self, value):
        self.classification = value

