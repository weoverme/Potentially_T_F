from nltk import *
import numpy as np


class TrainingData:

    def __init__(self, data_size):
        self.features = self.get_support_vector_features()
        self.data = []
        self.target = []
        self.text_list = []
        self.n_samples = 0

    def get_support_vector_features(self):
        feature_f = open("verifiability_features.txt", "r")

        # get all features
        support_vector_features = []
        for line_f in feature_f:
            support_vector_features.append(line_f.replace("\n", ""))

        feature_f.close()

        return support_vector_features

    def increment_n_samples(self):
        self.n_samples += 1

    def add_sample(self, sample, text):
        """

        :param sample: an array of integers, mapped to the sv_features
        :return: None
        """
        self.data.append(np.array(sample))
        self.determine_and_add_target(sample)
        self.text_list.append(text)
        self.increment_n_samples()

    def determine_and_add_target(self, sample):


        if sample[-1] > 0:
            # if there exists a "?" in the sample text
            self.target.append("NVER")
        else:
            # check if features exist in the sample text
            t_sum = 0
            for v in sample:
                t_sum += v

            if t_sum != 0:
                self.target.append("VER")
            else:
                self.target.append("NVER")


#########################################################

def get_sample_feature_vectors(features_of_tweet, training_data_object):

    td_features = training_data_object.features

    for feature in features_of_tweet: # for each feature
        # find the index of the feature in sv_features, if it exists
        index = 9999 # default value
        curr_sv = [0]*len(td_features) # list of n_features of 0s ex. [0, 0, 0, ..]

        try:
            for i in range(len(td_features)):
                if feature == td_features[i]:
                    index = i
                    break

            # when found, increment value
            curr_sv[index] += 1

        except IndexError:
            # if the feature isn't in the sv_features list
            pass

    return curr_sv


def main():
    td = TrainingData(10)

    twitter_f = open("twitter_training_data_set.txt", "r")

    # set up support vector item

    for line in twitter_f:
        attr = line.split("%\t%")
        # for each line, get the classification value, text and url/tweet_id
        c_val, text_string, text_id = attr[0], attr[1], int(attr[2])

        # get all features from the current tweet
        pos = pos_tag(word_tokenize(text_string))

        # save all features into featureList
        features_of_tweet = []
        for token in pos:
            feat = token[1]
            if feat not in features_of_tweet:
                features_of_tweet.append(feat)

        #print(features_of_tweet)

        # See if there are features in the list, which matches whats in the list of features of the TD
        td.add_sample(get_sample_feature_vectors(features_of_tweet, td), text_string)
    print(td.data)
    print(td.target)


if __name__ == "__main__":
    main()