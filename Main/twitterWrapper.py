import tweepy
import traceback
import datetime
import re as re


class TwitterWrapper:

    """

    One Twitter Wrapper for one username.
    Instantiating a TwitterWrapper gathers N number of tweets and saves it to
    the dictionary self.all_tweets.

    """

    def __init__(self, username, n):
        # My user is  @ray_cho94
        self.access_token = "837846446376271872-PrPyDNixKM7dxCtNrHJ9C73w7XKWzmC"
        self.access_token_secret = "pNEJZv0tFlPFjrvdg08HEFyPTFv2WmbKmDuFlIS8qQOK9"
        self.consumer_key = "KOAjR7P0c01Jt8Bs3jAJguXe8"
        self.consumer_secret = "cG9V3cJPXNogyH7AbvUTZY0aPVhwDkgTUOYk8qsaZ61apYj10L"
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)

        # My copy of the API
        self.api = tweepy.API(self.auth)

        # dictionary of tweets initialised
        self.username = username

        # dictionary 'all_tweets' will be in the form of    "id" : "tweet_text"
        self.all_tweets = {}

        self.get_tweets_for(n)

    def get_tweets_for(self, n):
        """
        Get the tweets for a object's username, in order of most recent --> least recent
        :param n: limited integer value
        :return: None
        """
        try:
            # for each tweet, add it to the object's dictionary
            for status in tweepy.Cursor(self.api.user_timeline, id=self.username).items(n):
                self.add_tweet_to_dic(status.id, status.text)
            # save the tweets, for future reference
            self.write_tweets_to_file()
        except TypeError:
            try:
                self.get_tweets_for(int(n))
            except TypeError:
                print("Second argument must be a positive integer value!")

        except tweepy.error.TweepError:
            #.print_exc()
            print("Invalid Username")
            self.username = ""

    def add_tweet_to_dic(self, t_id, tweet):
        """
        # if id already exists in the dictionary
        if self.all_tweets[t_id] is not None:
            # dont screw up my dictionary
            return False
        else:
            # add entry to the dictionary
            self.all_tweets[t_id] = tweet
            return True
        """

        self.all_tweets[t_id] = tweet

    def write_tweets_to_file(self):
        """
        replace file with text file containing the new dictionary, in order of tweet_id.
        """

        # create/overwrite @username.txt
        f = open("datasets_twitter/"+self.username+".txt", "w+", encoding="UTF-8")

        # get all tweet ids in ascending order
        tweet_ids = sorted(self.all_tweets.keys())

        # for each tweet
        for tw_id in tweet_ids:
            self.all_tweets[tw_id] = " ".join(self.all_tweets[tw_id].split("\n"))

            tw_text = self.all_tweets[tw_id]

            f.write(str(tw_id)+" :: "+tw_text+"\n")

        # end function
        f.close()

    def get_all_tweets_from_file(self):
        """
        get all tweets from the object's designated dictionary. This dictionary may exist prior to the instantiation of
        this object, most likely because there has been an instance of this object being used previously.
        :return: None
        """
        # open file with only READ ACCESS, since we don't want to change anything to the file here
        try:
            f = open(self.username+".txt", "r")

            # replace the dictionary with whatever we have in our file.
            # Essentially, if the dictionary file doesn't have the id/Tweet combo, then it shouldn't exist in the
            # dictionary.
            self.all_tweets = {}

            # Unpack the (hopefully) unique string
            for line in f:
                l_split = line.split(" :: ")
                self.all_tweets[int(l_split[0])] = l_split[1]

            # finished using file
            f.close()
        except FileNotFoundError:
            print("File not found. Write to file first!")

    def get_most_recent_tweets(self, n):
        """
        get the n most recent tweets
        :param n:
        :return:
        """
        tweets_sorted = sorted(self.all_tweets.keys())
        most_recent = []
        t_len = len(tweets_sorted)
        for i in range(t_len-1, t_len-n-1, -1):
            most_recent.append(self.all_tweets[tweets_sorted[i]])
        print(most_recent)


if __name__ == "__main__":
    timestamp = '{:%Y_%m_%d_%H_%M_%S}'.format(datetime.datetime.now())
    w_file = open("datasets_twitter/twitter_training_data_raw" + timestamp + ".txt", "w+", encoding="UTF-8")

    # make training data made up of twitter feed
    tw_users = ["@realDonaldTrump", "BarackObama", "@HillaryClinton",
                 "@SenSanders", "@AdamBandt", "@TurnbullMalcolm",
                 "@TonyAbbottMHR", "@MrKRudd", "@billshortenmp",
                 "@JuliaGillard", "@JoeHockey", "@JulieBishopMP", "@POTUS"]

    # write twitter feed to file
    for i in tw_users:
        # get 50 tweets for each user
        tw = TwitterWrapper(i, 20)
        # write the tweets to the training data file
        all_t = tw.all_tweets
        ks = all_t.keys()
        for k in ks:

            text = all_t[k].replace("\n", " ")
            try:
                to_write = text + "%\t%" + str(k) + "\n"
                w_file.write(to_write)

            except UnicodeEncodeError:
                pass

    w_file.close()
