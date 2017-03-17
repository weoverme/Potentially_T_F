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
        try:
            for status in tweepy.Cursor(self.api.user_timeline, id=self.username).items(n):
                #print(json.dumps(status._json))
                self.add_tweet_to_dic(status.id, status.text)
            #print(self.all_tweets)
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
            print(str(i))
            print(self.all_tweets[i])
            self.all_tweets[i] = " ".join(self.all_tweets[i].split("\n"))
            f.write(str(i)+" :: "+self.all_tweets[i]+"\n")

        # end function
        f.close()

    def get_all_tweets(self):
        f = open(self.username+".txt", "r")
        self.all_tweets = {}
        for line in f:
            print(line)
            lsplit = line.split(" :: ")
            self.all_tweets[int(lsplit[0])] = lsplit[1]

        print(sorted(self.all_tweets))
        f.close()


    def get_most_recent_tweets(self, n):
        """
        get the n most recent tweets
        :param n:
        :return:
        """
        pass


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
print("done")
t.get_all_tweets()
print("done2")
#TwitterObserver().get_most_recent_tweets("@realDonaldTrump",10)