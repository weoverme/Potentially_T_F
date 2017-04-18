from nltk import *
import numpy

def get_tweets(filename, all_tweets):
    f = open("@BarackObama.txt", "r")

    for line in f:
        l_split = line.split(" :: ")
        all_tweets.append(l_split[1])

    # finished using file
    f.close()

def tokenise_tweets(all_tweets):
    sent_tok_list = []
    all_tok_list = []

    for t in range(len(all_tweets)-1):
        # print(all_tweets[t])
        sent_list = sent_tokenize(all_tweets[t])
        all_tok_list.append([])
        for s in sent_list: # for each sentence
            word_tok_list = word_tokenize(s)
            pos_tag_list = pos_tag(word_tok_list)
            all_tok_list[t].append(pos_tag_list)
            if return_flag_on_feature("CD", pos_tag_list):
                print(pos_tag_list)



    return all_tok_list


def return_flag_on_feature(feature, pos_tag_list):
    for i in pos_tag_list:
        if i[1] == feature:
            return True
    return False



def main():
    all_tweets = []
    get_tweets("@BarackObama.txt", all_tweets)
    tokenise_tweets(all_tweets)

main()