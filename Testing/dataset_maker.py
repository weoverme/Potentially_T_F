from nltk import *
import numpy as np
import datetime

class TrainingData:

    def __init__(self):
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
        if sample[-1] != 0:
            # if there exists a "?" in the sample text
            self.target.append("NVER")
        else:
            # check if features exist in the sample text
            t_sum = 0
            for v in sample:

                t_sum += v

            if t_sum > 0:
                self.target.append("VER")
            else:
                self.target.append("NVER")


    def save(self):
        timestamp = '{:%Y_%m_%d_%H_%M_%S}'.format(datetime.datetime.now())
        f = open("datasets/training_data_"+ timestamp+".txt", "w+")
        f.write("TrainingData, " + str(self.n_samples) + "\n")

        for i in range(self.n_samples):
            data_ = "".join(str(self.data[i].tolist()))
            line = data_ + "%\t%" + self.target[i] + "%\t%" + self.text_list[i] + "\n"
            f.write(line)

        f.close()

#########################################################

def get_sample_feature_vectors(postag_tokens_of_tweet, training_data_object):

    td_features = training_data_object.features
    curr_sv = [0] * len(td_features)  # list of n_features of 0s ex. [0, 0, 0, ..]

    for token in postag_tokens_of_tweet: # for each feature
        text, feature = token[0], token[1]
        # find the index of the feature in td_features, if it exists
        index = 9999 # default value

        try:
            for i in range(len(td_features)):
                #print("Feature:", feature, "\tTD Feature:", td_features[i])
                if feature == td_features[i]:
                    # when found, increment sample vector's  value

                    if td_features[i] == td_features[-1]:
                        # checking if there is a "?" in the text
                        if token[0] == "?":
                            curr_sv[i] -= 1
                            break
                    else:
                        curr_sv[i] += 1
                        #print('incremented:', td_features[i], "-", curr_sv)

                        break


        except IndexError:
            # if the feature isn't in the sv_features list
            pass

    return curr_sv


def main():
    td = TrainingData()

    twitter_f = open("twitter_training_data_set.txt", "r")

    # set up support vector item

    for line in twitter_f:
        attr = line.split("%\t%")
        # for each line, get the classification value, text and url/tweet_id
        c_val, text_string, text_id = attr[0], attr[1], int(attr[2])

        # get all features from the current tweet
        pos = pos_tag(word_tokenize(text_string))

        # save all features into featureList
        postag_tokens_of_tweet = []
        for token in pos:
            feat = token[1]
            if feat not in postag_tokens_of_tweet:
                postag_tokens_of_tweet.append(token)

        # See if there are features in the list, which matches whats in the list of features of the TD
        sample_item = get_sample_feature_vectors(postag_tokens_of_tweet, td)
        td.add_sample(sample_item, text_string)




    for i in range(td.n_samples):

        """
        if (td.data[i][-1] != 0):
            print("Data:", td.data[i], " - ", td.text_list[i])
            print("Label:", td.target[i])
        """
        print("Data:", td.data[i].tolist(), " - ", td.text_list[i])
        print("Label:", td.target[i])


    td.save()

if __name__ == "__main__":
    main()