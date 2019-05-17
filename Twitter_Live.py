import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import unicodedata
import os


class TwitterClient(object):

    def __init__(self):

        # keys and tokens from the Twitter Dev Console
        consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        """Utility function to clean tweet text by removing links, special characters using simple regex statements."""

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        """Utility function to classify sentiment of passed tweetusing textblob's sentiment method"""

        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
            # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=100):
        # empty list to store parsed tweets
        tweets = []
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                # saving text of tweet
                parsed_tweet['text'] = unicodedata.normalize('NFKD', tweet.text).encode('ascii', 'ignore')
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                        print (parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            if tweets != "":
                print ("got tweets")
                # return parsed tweets
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
        global ptweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # percentage of positive tweets
        global posper
        posper = format(100 * len(ptweets) / len(tweets))
        print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
        # picking negative tweets from tweets
        global ntweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        # percentage of negative tweets
        global negper
        negper = format(100 * len(ntweets) / len(tweets))
        print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
        # percentage of neutral tweets
        print("Neutral tweets percentage: {} % \ ".format(100 * (len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

        # printing first 5 positive tweets

        try:
            print("\n\nPositive tweets:")
            for tweet in ptweets[:10]:
                print(tweet['text'])
            # printing first 5 negative tweets
            print("\n\nNegative tweets:")
            for tweet in ntweets[:10]:
                print(tweet['text'])
        except UnicodeEncodeError:
            pass
        return

def main(rev):
    print (rev + "topic goes here")
    q = rev
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query=q, count=200)
    if tweets != "":
        print ("no tweets")
    return posper, negper, ptweets, ntweets
