import json
import tweepy


# My user is  @ray_cho94
access_token = "837846446376271872-PrPyDNixKM7dxCtNrHJ9C73w7XKWzmC"
access_token_secret = "pNEJZv0tFlPFjrvdg08HEFyPTFv2WmbKmDuFlIS8qQOK9"
consumer_key = "KOAjR7P0c01Jt8Bs3jAJguXe8"
consumer_secret = "cG9V3cJPXNogyH7AbvUTZY0aPVhwDkgTUOYk8qsaZ61apYj10L"


def main():
    """
    The main function of the twitter streaming function. For now
    the name is only a placeholding name and will be replaced
    in the near future.
    :return:
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    for friend in tweepy.Cursor(api.friends).items(10):
        process_or_store(friend._json)
        # print(status.text)
        store_metadata(friend._json)


def store_metadata(tweet):
    """
    Stores the metadata of a tweet._json file into its respective
    user's name.txt file.
    :param tweet:
    :return: None

    """
    name = tweet["name"]
    f = open(name+".txt", "w+")
    for i in tweet:
       f.write(i+" : "+str(tweet[i])+"\n")
    f.close()


def process_or_store(tweet):
    """
    Mostly used for testing purposes while getting to know more
    about the TwitterAPI.
    :param tweet:
    :return: None
    """
    print(json.dumps(tweet))
    print(tweet["name"])



main()