"""
Retrieved from: adilmoujahid.com/posts/2014/07/twitter-analytics/
Author: Adil Moujahid
Modified: 4 March 2017
"""


#Import the necessary methods from tweepy library
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
#My user is  @ray_cho94
access_token = "837846446376271872-PrPyDNixKM7dxCtNrHJ9C73w7XKWzmC"
access_token_secret = "pNEJZv0tFlPFjrvdg08HEFyPTFv2WmbKmDuFlIS8qQOK9"
consumer_key = "KOAjR7P0c01Jt8Bs3jAJguXe8"
consumer_secret = "cG9V3cJPXNogyH7AbvUTZY0aPVhwDkgTUOYk8qsaZ61apYj10L"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
        print(status.text)
        print('done')
