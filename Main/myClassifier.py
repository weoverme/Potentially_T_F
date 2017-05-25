from nltk import *
from nltk.classify import SklearnClassifier
from sklearn.svm import SVC
from sklearn.externals import joblib  # saving the clf
import glob
import os
import datetime  # for new file
import json  # to save training_data to file


class MyClassifier:
    def __init__(self, load_clf=False, load_tr_data=False):
        self.features = self.__load_support_vector_features()
        self.training_data = []
        self.n_samples = 0
        self.all_tweets = self.__load_tweets_from_file()  # list not dict

        # Classifier loading
        if load_clf:
            self.load_clf()
        else:
            self.clf = SklearnClassifier(SVC(), sparse=False)

        # Training Data loading
        if load_tr_data:
            self.__load_training_data()

    def __load_tweets_from_file(self):
        # open latest file
        list_of_files = glob.glob("datasets_twitter/twitter_training_data_raw*.txt")
        latest_file = max(list_of_files, key=os.path.getctime)
        f = open(latest_file, "r", encoding="UTF-8")

        tweet_list = []
        for line in f:
            line = line.split("%\t%")
            tweet_text, tweet_id = line[0], line[1]
            tweet_list.append((tweet_text, tweet_id))

        return tweet_list

    def __load_support_vector_features(self):
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

    def __assemble_training_data(self):
        """
        Construct the training data using the twitter training data set.

        To be used directly prior to training the Classifier

        :return:
        """

        for tweet in self.all_tweets:
            # get the sample and target for each tweet
            tweet_text = tweet[0]
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

    def __save_training_data(self):
        timestamp = '{:%Y_%m_%d_%H_%M_%S}'.format(datetime.datetime.now())
        f = open("datasets_twitter/twitter_training_dataset"+timestamp+".json", "w+")
        json_data = json.dumps(self.training_data)
        f.write(json_data)
        f.close()

    def __load_training_data(self):
        list_of_files = glob.glob("datasets_twitter/twitter_training_dataset*.json")
        latest_file = max(list_of_files, key=os.path.getctime)
        f = open(latest_file, "r")
        s = f.readline()
        js = json.loads(s)
        for i in js:
            tup = (i[0], i[1])  # sample, target
            self.training_data.append(tup)

    def train_with_svc(self):
        # make the training data
        self.__assemble_training_data()

        # Train the classifier
        self.clf.train(self.training_data)

        # save classifier as soon as it is trained
        self.save_clf()

    def predict_single(self, test_text):
        """
        Predict a single sample. Then based on user's input, add the sample to the training data with the correct label.

        :param test_text:
        :return:
        """

        test_sample = self.__get_sample(test_text)
        test_dict = {}
        for index in range(len(self.features)):
            test_dict[self.features[index]] = test_sample[index]

        pred = self.clf.classify_many([test_dict])
        return (pred[0], test_sample)

    def predict_multiple(self, test_list):
        """
        Predict more than one sample at a time.

        :param test_list:
        :return:
        """
        # translate test_list into clf passable data format
        test_data = []
        for i in test_list:
            curr_test_sample = self.__get_sample(i)
            test_dict = {}
            for index in range(len(self.features)):
                test_dict[self.features[index]] = curr_test_sample[index]

            test_data.append(test_dict)

        # predict
        pred = self.clf.classify_many(test_data)
        return pred

    def update_pred_into_training(self, test_tweet, pred_val):
        """
        Adds predicted ( {feat:sample}, target ) to training data
        then saves the training data

        if test_text already exists in the training data
            update the target value instead
            then save the training data


        :param test_tweet: a tweet in the form of (tweet_text, tweet_id)
        :param pred_val: the value of the prediction made by the classifier
        :return:
        """
        # a flag to make sure only one part of the code is run
        updated = False

        # localise
        test_tweet_text = test_tweet[0]

        # if text exists in training data already, update the target for this tweet
        for i in range(len(self.all_tweets)):
            tweet = self.all_tweets[i]

            if test_tweet_text == tweet[0]:   # if found
                test_sample = self.__get_sample(test_tweet_text)

                # make into trainable data format
                test_dict = {}
                for j in range(len(self.features)):
                    test_dict[self.features[j]] = test_sample[j]
                test_target = pred_val

                tup = (test_dict, test_target)

                # get the current tup for the test_text and replace
                self.training_data[i] = tup

                # there should only be one tweet with the same text
                updated = True
                break

        # if test_text is not in the training data already
        if not updated:
            # make into trainable data format
            test_sample = self.__get_sample(test_tweet_text)
            test_dict = {}
            for j in range(len(self.features)):
                test_dict[self.features[j]] = test_sample[j]
            test_target = pred_val

            tup = (test_dict, test_target)

            # add tweet to all_tweets and training data
            # get tweet_id
            self.all_tweets.append(test_tweet)
            self.training_data.append(tup)

            # consistency
            updated = True

        # save the training data to file
        self.__save_training_data()
        # train the classifier again
        self.train_with_svc()

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
JJR         adjective - comparative
JJS         adjective - superlative
RBR         adjective - comparative
RBS         adjective - superlative
?           non pos_tag, just looking for a ? in the text


"""

if __name__ == "__main__":
    clf = MyClassifier(True, True)
    clf.train_with_svc()




