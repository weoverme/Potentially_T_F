from nltk import *
import numpy as np
import datetime

# to retrieve latest training data file
import glob
import os

class TrainingData:

    def __init__(self, flag=False):
        self.features = self.get_support_vector_features()
        self.data = []
        self.target = []
        self.text_list = []
        self.n_samples = 0

        if flag:
            # default False,
            self.retrieve()

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
        self.data.append(sample)
        self.determine_and_add_target_bin(sample)
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

    def determine_and_add_target_bin(self, sample):
        # check curr_sv if VER or NVER
        t_sum = 0
        for v in sample:
            if v < 0:
                # if there exists a "?" in the sample text (only reason why there'd be a -ve value in curr_sv)
                #self.target.append(-1)
                t_sum = -1
                break
            t_sum += v

        if t_sum > 0:
            self.target.append(1)
        else:
            self.target.append(-1)
        print("t_sum:\t",t_sum)

    def save(self):
        timestamp = '{:%Y_%m_%d_%H_%M_%S}'.format(datetime.datetime.now())
        f = open("datasets/training_data_"+ timestamp+".txt", "w+")
        f.write("TrainingData, " + str(self.n_samples) + "\n")

        for i in range(self.n_samples):
            data_ = "".join(str(self.data[i].tolist()))
            line = data_ + "%\t%" + str(self.target[i]) + "%\t%" + self.text_list[i] + "\n"
            f.write(line)

        f.close()

    def retrieve(self):
        # Can only run this if upon initialisation
        if self.n_samples != 0:
            pass
        else:
            list_of_files = glob.glob("datasets/*")
            latest_file = max(list_of_files, key=os.path.getctime)
            f = open(latest_file, "r")
            first_line = f.readline()
            if first_line.split(",")[0] == "TrainingData":
                # get td.n_samples
                self.n_samples = int(first_line.split(",")[1])

            line_check = 0 # checking the number of lines doesn't exceed our said n_samples count
            for line in f:
                if line_check >= self.n_samples:
                    break
                l_split = line.split("%\t%")
                t_data, t_target, t_text = l_split[0], l_split[1], l_split[2]

                # arrange t_data into a int list form
                t_data = t_data.replace("[", "")
                t_data = t_data.replace("]", "")
                t_data = t_data.split(",")
                t_data = [int(i) for i in t_data]

                # add t_data and t_target as they should be
                #self.data.append(np.array(t_data))
                self.data.append(t_data)
                self.target.append(int(t_target))
                self.text_list.append(t_text)
                line_check += 1
        #self.data = np.array(self.data)
        #self.target = np.array(self.target)

#########################################################

def get_sample_feature_vectors(postag_tokens_of_tweet, td_features):

    curr_sv = [0] * len(td_features)  # list of n_features of 0s ex. [0, 0, 0, ..]

    for token in postag_tokens_of_tweet: # for each feature
        t_text, t_feature = token[0], token[1]
        # find the index of the feature in td_features, if it exists
        index = 9999 # default value

        try:
            for i in range(len(td_features)):
                if t_feature == td_features[i]:
                    # when found, increment/decrement sample vector's  value

                    if td_features[i] == td_features[-1]:
                        # checking if there is a "?" in the text
                        if token[0] == "?":
                            # decrement
                            curr_sv[i] -= 1
                            break
                    else:
                        curr_sv[i] += 1
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


        if (td.data[i][-1] < 0):
            print("Data:", td.data[i], " - ", td.text_list[i])
            print("Label:", td.target[i])
        """
        print("Data:", td.data[i].tolist(), " - ", td.text_list[i])
        print("Label:", td.target[i])
        """

    td.save()

if __name__ == "__main__":
    main()