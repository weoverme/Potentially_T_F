import json
import tweepy
import traceback

# My user is  @ray_cho94
access_token = "837846446376271872-PrPyDNixKM7dxCtNrHJ9C73w7XKWzmC"
access_token_secret = "pNEJZv0tFlPFjrvdg08HEFyPTFv2WmbKmDuFlIS8qQOK9"
consumer_key = "KOAjR7P0c01Jt8Bs3jAJguXe8"
consumer_secret = "cG9V3cJPXNogyH7AbvUTZY0aPVhwDkgTUOYk8qsaZ61apYj10L"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def get_tweets_for(username, n):
    try:
        user = api.get_user(username)
        for tweet in user.timeline().items(n):
            print(tweet)
            print(tweet.text)

        print("done")
    except Exception:
        traceback.print_exc()

    except TypeError:
        try:
            get_tweets_for(username, int(n))
        except TypeError:
            print("Second argument must be a positive integer value!")


# get_tweets_for("@BarackObama", 10)

#for tweet in tweepy.Cursor(api.home_timeline).items(10):
#    print(json.dumps(tweet._json))

for status in tweepy.Cursor(api.home_timeline).items(5):
    print(status.text)