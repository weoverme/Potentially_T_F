import tweepy
import traceback

class TwitterObserver:

    def __init__(self):
        # My user is  @ray_cho94
        self.access_token = "837846446376271872-PrPyDNixKM7dxCtNrHJ9C73w7XKWzmC"
        self.access_token_secret = "pNEJZv0tFlPFjrvdg08HEFyPTFv2WmbKmDuFlIS8qQOK9"
        self.consumer_key = "KOAjR7P0c01Jt8Bs3jAJguXe8"
        self.consumer_secret = "cG9V3cJPXNogyH7AbvUTZY0aPVhwDkgTUOYk8qsaZ61apYj10L"
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)

        self.api = tweepy.API(self.auth)

    def get_tweets_for(self, username, n):
        try:
            for status in tweepy.Cursor(self.api.user_timeline, id=username).items(n):
                # process_status(status._json)
                # print(status.text)
                self.write_tweet_to_file(username, status.text)
        except tweepy.error.TweepError as e:
            traceback.print_exc()
            print("Exception")
        except TypeError:
            try:
                self.get_tweets_for(username, int(n))
            except TypeError:
                print("Second argument must be a positive integer value!")

    def write_tweet_to_file(self, username, tweet):
        f = open(username + ".txt", "w+")
        f.write(tweet + "\n")
        f.close()

    def get_most_recent_tweets(self, username, n):
        total_tweets = 0
        with open(username+".txt", "r+") as file:
            # find out how many lines are in the .txt file
            for line in file:
                total_tweets += 1
                print(total_tweets)

            # report how many lines
            print(total_tweets)

            # print out the most recent tweets
            for i in range(total_tweets, (0), -1):
                print(i)


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

TwitterObserver().get_tweets_for("@chrismorrisOrg", 10)
#TwitterObserver().get_most_recent_tweets("@realDonaldTrump",10)