import json, _json
import tweepy
import sys
from tweepy import OAuthHandler


#My user is  @ray_cho94
access_token = "837846446376271872-PrPyDNixKM7dxCtNrHJ9C73w7XKWzmC"
access_token_secret = "pNEJZv0tFlPFjrvdg08HEFyPTFv2WmbKmDuFlIS8qQOK9"
consumer_key = "KOAjR7P0c01Jt8Bs3jAJguXe8"
consumer_secret = "cG9V3cJPXNogyH7AbvUTZY0aPVhwDkgTUOYk8qsaZ61apYj10L"


def function1():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    for friend in tweepy.Cursor(api.friends).items(10):
        process_or_store(friend._json)
        # print(status.text)
        store_name(friend._json)

def store_name(tweet):
    name = tweet["name"]
    f = open(name+".txt", "w+")
    for i in tweet:
       f.write(i+" : "+str(tweet[i])+"\n")
    f.close()


def process_or_store(tweet):
    print(json.dumps(tweet))
    print(tweet["name"])



function1()