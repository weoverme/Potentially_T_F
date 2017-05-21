from nltk import *
from nltk.classify import SklearnClassifier
from sklearn.svm import SVC
from sklearn.externals import joblib
import glob, os


##############################################################


class MyClassifier:
    def __init__(self, load=False):
        self.features = self.__get_support_vector_features()
        self.training_data = []
        self.n_samples = 0
        self.tweets_from_file = self.__get_tweets_from_file()
        if load:
            self.load_clf()
        else:
            self.clf = SklearnClassifier(SVC(), sparse=False)

    def __get_tweets_from_file(self):
        # open latest file
        list_of_files = glob.glob("datasets_twitter/twitter_training_data_set*.txt")
        latest_file = max(list_of_files, key=os.path.getctime)
        f = open(latest_file, "r")

        tweet_list = []
        for line in f:
            line = line.split("%\t%")
            tweet_text, tweet_id = line[0], line[1]
            tweet_list.append(tweet_text, tweet_id)

        return tweet_list

    def __get_support_vector_features(self):
        feature_f = open("verifiability_features.txt", "r")

        # get all features
        support_vector_features = []
        for line_f in feature_f:
            support_vector_features.append(line_f.replace("\n", ""))

        feature_f.close()

        return support_vector_features

    def __get_sample(self, text_str):
        """
        Changes the text_str into a sample of data in the form of [0, 0, 0, ...]
        This is to be used by the classifier, when
            1) Assembling Training Data, and
            2) Testing data.
        It returns a list of int, which is basically a count of how many of each feature existed in text_str.

        :param text_str: a string of text which is to be verified
        :return: curr_sample, a list of int, sort of mapped to self.features
        """
        tokens = pos_tag(word_tokenize(text_str))

        curr_sample = [0] * len(self.features)  # list of n_features of 0s ex. [0, 0, 0, ..]

        for token in tokens:  # for each feature
            t_text, t_feature = token[0], token[1]
            try:
                for index in range(len(self.features)):
                    if t_feature == self.features[index]:
                        # when found, increment/decrement sample vector's  value

                        if self.features[index] == self.features[-1]:
                            # checking if there is a "?" in the text
                            if token[0] == "?":
                                # decrement
                                curr_sample[index] -= 1
                                break
                        else:
                            curr_sample[index] += 1
                            break

            except IndexError:
                # if the feature isn't in the sv_features list
                pass

        return curr_sample

    def __get_training_target(self, sample):
        """
        Returns the label depending on the sample given.

        :param sample: int[] from self.__get_sample()
        :return: "VER" or "NVER", representing the two labels Verifiable and Non-Verifiable
        """
        # check sample if VER or NVER
        t_sum = 0
        for v in sample:
            if v < 0:
                # if there exists a "?" in the sample text
                # (this is the only reason why there'd be a -ve value in curr_sv)
                t_sum = -1
                break

            t_sum += v

        if t_sum > 0:
            return "VER"
        else:
            return "NVER"

    def assemble_training_data(self):
        """
        Construct the training data using the twitter training data set.

        To be used directly prior to training the Classifier

        :return:
        """

        for tweet in self.tweets_from_file:
            # get the sample and target for each tweet
            tweet_text, tweet_id = tweet[0], tweet[1]
            curr_sample = self.__get_sample(tweet_text)
            curr_target = self.__get_training_target(curr_sample)

            # change the above into training data
            tr_dict = {}
            for i in range(len(self.features)):
                tr_dict[self.features[i]] = curr_sample[i]

            tup = (tr_dict, curr_target)

            # add to self.training_data
            self.training_data.append(tup)

        # repeat

    def train_with_SVC(self):
        self.assemble_training_data()
        self.clf.train(self.training_data)

    def predict_single(self, test_text):
        """
        Predict a single sample. Then based on user's input, add the sample to the training data with the correct label.

        :param test_text:
        :return:
        """

        test_sample = self.__get_sample(test_text)
        test_dict = {}
        for index in range(self.features):
            test_dict[self.features[index]] = test_sample[index]

        pred = self.clf.predict([test_dict])
        print("Prediction:", pred)
        feedback = input("Is this prediction correct? Y/N")

        # Make data + target into a tuple
        if feedback == "Y" or feedback == "y":
            tup = (test_dict, pred)
        else:
            # correct the target and make into a tuple
            if pred == "VER":
                tup = (test_dict, "NVER")
            else:
                tup = (test_dict, "VER")

        # add to self.training_data
        self.training_data.append(tup)

    def predict_multiple(self, test_list):
        """
        Predict more than one sample at a time.

        :param test_list:
        :return:
        """
        test_data = []
        for i in test_list:
            curr_test_sample = self.__get_sample(i)
            test_dict = {}
            for index in range(self.features):
                test_dict[self.features[index]] = curr_test_sample[index]

            test_data.append(test_dict)

        pred = self.clf.predict([test_data])
        print("Prediction:", pred)

        feedback = input("Are these predictions correct? Y/N")

        # Make data + target into a tuple
        if feedback == "Y" or feedback == "y":
            # get individual tuples
            for i in range(len(test_data)):
                tup = (test_data[i], pred[i])

                # add to self.training_data
                self.training_data.append(tup)

        else:
            # must correct test data manually before adding into training data
            print("Please predict each separately to add samples into training dataset.")

    def load_clf(self):
        """
        Load a previously trained and saved classifier.
        :return:
        """
        self.clf = joblib.load("twitterClassifier.pkl")

    def save_clf(self):
        """
        Save the current classifier to file
        :return:
        """
        joblib.dump(self.clf, "twitterClassifier.pkl")

"""
DATASET EXAMPLE
    train_data = [({"a": 4, "b": 1, "c": 0}, "ham"),
               ({"a": 5, "b": 2, "c": 1}, "ham"),
               ({"a": 0, "b": 3, "c": 4}, "spam"),
               ({"a": 5, "b": 1, "c": 1}, "ham"),
               ({"a": 1, "b": 4, "c": 3}, "spam")]



def prepare_sample(text_str, features):

    tokens = pos_tag(word_tokenize(text_str))

    curr_sv = [0] * len(features)  # list of n_features of 0s ex. [0, 0, 0, ..]

    for token in tokens:  # for each feature
        t_text, t_feature = token[0], token[1]
        try:
            for index in range(len(features)):
                if t_feature == features[index]:
                    # when found, increment/decrement sample vector's  value

                    if features[index] == features[-1]:
                        # checking if there is a "?" in the text
                        if token[0] == "?":
                            # decrement
                            curr_sv[index] -= 1
                            break
                    else:
                        curr_sv[index] += 1
                        break

        except IndexError:
            # if the feature isn't in the sv_features list
            pass

    return curr_sv



FEATURES

POS_TAG     Explanation
=======     ===========
CD          cardinal digit
VBD         verb - Past tense
VBG         verb - present participle
VBN         verb - past participle
VBP         verb - singular present
VBZ         verb - 3rd person singular present
JJ          adjective
JJR         adjective - comparative
JJS         adjective - superlative
RBR         adjective - comparative
RBS         adjective - superlative
?           non pos_tag, just looking for a ? in the text


"""

