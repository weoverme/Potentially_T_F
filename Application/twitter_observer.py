import tweepy
import traceback
import json

class TwitterObserver:

    """

    One Twitter Observer for one user.

    """

    def __init__(self, username):
        # dictionary of tweets initialised
        self.username = username
        # dictionary 'all_tweets' will be in the form of    "id" : "tweet_text"
        self.all_tweets = {}

        # My user is  @ray_cho94
        self.access_token = "837846446376271872-PrPyDNixKM7dxCtNrHJ9C73w7XKWzmC"
        self.access_token_secret = "pNEJZv0tFlPFjrvdg08HEFyPTFv2WmbKmDuFlIS8qQOK9"
        self.consumer_key = "KOAjR7P0c01Jt8Bs3jAJguXe8"
        self.consumer_secret = "cG9V3cJPXNogyH7AbvUTZY0aPVhwDkgTUOYk8qsaZ61apYj10L"
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)

        # My copy of the API
        self.api = tweepy.API(self.auth)

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
        except tweepy.error.TweepError as e:
            traceback.print_exc()
            print("Exception")
        except TypeError:
            try:
                self.get_tweets_for(self.username, int(n))
            except TypeError:
                print("Second argument must be a positive integer value!")

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
        f = open(self.username+".txt", "w+")

        # get all tweet ids in ascending order
        tweet_ids = sorted(self.all_tweets.keys())

        # for each tweet
        for i in tweet_ids:
            self.all_tweets[i] = " ".join(self.all_tweets[i].split("\n"))
            f.write(str(i)+" :: "+self.all_tweets[i]+"\n")

        # end function
        f.close()

    def get_all_tweets(self):
        """
        get all tweets from the object's designated dictionary. This dictionary may exist prior to the instantiation of
        this object, most likely because there has been an instance of this object being used previously.
        :return: None
        """
        # open file with only READ ACCESS, since we don't want to change anything to the file here
        f = open(self.username+".txt", "r")

        # replace the dictionary with whatever we have in our file.
        # Essentially, if the dictionary file doesn't have the id/Tweet combo, then it shouldn't exist in the
        # dictionary.
        self.all_tweets = {}

        # Unpack the (hopefully) unique string
        for line in f:
            lSplit = line.split(" :: ")
            self.all_tweets[int(lSplit[0])] = lSplit[1]

        # finished using file
        f.close()

    def get_most_recent_tweets(self, n):
        """
        get the n most recent tweets
        :param n:
        :return:
        """
        tweets_sorted = sorted(self.all_tweets.keys())
        most_recent = []
        tLen = len(tweets_sorted)
        for i in range(tLen-1, tLen-n-1, -1):
            most_recent.append(self.all_tweets[tweets_sorted[i]])
        print(most_recent)


def test_get_tweets_for():
    test_valid_user = "@ray_cho94"
    test_invalid_user = "@raydio545"
    # test for invalid n value
    testOb = TwitterObserver()
    testOb.get_tweets_for(test_valid_user, 10.1)
    print("tested invalid numerical")
    # test for str version of n value
    testOb.get_tweets_for(test_valid_user, "10")
    print("tested str(numerical)")
    # test for invalid user
    testOb.get_tweets_for(test_invalid_user, 10)
    print("tested invalid user")

t = TwitterObserver("@BarackObama")
t.get_tweets_for(15)
t.get_most_recent_tweets(10)
t.get_all_tweets()