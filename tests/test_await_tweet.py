import pytest
from src.utility.await_new_tweet import AwaitNewTweet
from src.utility.tweet_classifier import TweetClassifier
from src.settings import *
import twitter
import time


class TestAwaitTweet:
    def test(self):
        api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token_key,
                               access_token_secret=access_token_secret)
        clf = TweetClassifier(data_file_name="SmiteGame_classified_data.json")

        # monitor (parameter) twitter_screen_name for new tweets
        # classify/predict the new tweet using my classifier fitted/trained by the SmiteGame....json dataset
        # retweets if classification is in trigger targets
        awaiter = AwaitNewTweet(classifier=clf,
                                trigger_targets=['fwotd', 'bonus_points'],
                                twitter_screen_name=my_twitter_screen_name,
                                data_file="SmiteGame_classified_data.json")

        # create new tweet
        tweet = twitter.Status(text="""Earn 3 Fantasy Point Boosters for completing 1 First Win of the Day!\n
                                          http://www.smitegame.com/team-booster-weekend-june-9-11 …""")
        new_tweet_status = api.PostUpdate(tweet)
        time.sleep(11)  # TODO: make the amount of time between polling for new tweets an attribute
        recheck_status = api.GetHomeTimeline(count=1)
        print(recheck_status['retweeted'])
        assert(new_tweet_status.id == recheck_status.id)
        

