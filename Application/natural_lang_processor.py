from nltk import *


class NatLangProcessor:

    def __init__(self, username):
        self.username = username
        self.all_tweets = []
        self.features = []

    def get_tweets(self):
        f = open(self.username+".txt", "r")

        # [(int:id, str:tweet), bool:verifiable] per index
        for line in f:
            l_split = line.split(" :: ")
            self.all_tweets.append([(l_split[0], l_split[1]), None])

        f.close()

    def tokenize_tweets_by_word(self):
        """
        Tokenize all words, for each sentence (regardless of which tweet it came from.)
        The purpose of this method is to help the machine recognise the different
        features in a statement.

        :return: all_tok_list - a list of all tokenized words made up by all the tweets.
        """
        sent_tok_list = []
        all_tok_list = []

        for t in range(len(self.all_tweets) - 1):
            sent_list = sent_tokenize(self.all_tweets[t][0][1]) # all_tweets[tweet][look at tuple][look at text]
            all_tok_list.append([])
            for s in sent_list:  # for each sentence
                word_tok_list = word_tokenize(s)
                pos_tag_list = pos_tag(word_tok_list)
                all_tok_list[t].append(pos_tag_list)
                print(pos_tag_list)

        return all_tok_list

    def tokenize_tweets_by_tweets(self):

        verifiable_tweets = []

        for t in range(len(self.all_tweets) - 1):
            word_tok_list = word_tokenize(self.all_tweets[t])
            pos_tag_list = pos_tag(word_tok_list)

            for feature in self.features:
                if self.return_flag_on_feature(feature, pos_tag_list):
                    verifiable_tweets.append(self.all_tweets[t])
                    break

        return verifiable_tweets

    def return_flag_on_feature(self, feature, pos_tag_list):
        """
        Flags a statement true if a feature is present.
        :param feature:
        :param pos_tag_list:
        :return:
        """
        for i in pos_tag_list:
            if i[1] == feature:
                return True
        return False

    def add_features(self, feature):
        self.features.append(feature)

    def save_features_to_file(self):
        """
        Save the list of features to the file: verifiability_features.txt

        :return: None
        """
        f = open("verifiability_features.txt", "w+")
        for feat in self.features:
            f.write(feat+"/n")
        f.close()

    def get_features_from_file(self):
        """
        Get a list of features from a saved file of features.

        :return:
        """
        f_list = []
        f = open("verifiability_features.txt", "r")
        for line in f:
            f_list.append(line)
        self.features = f_list





