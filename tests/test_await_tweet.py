import pytest
from src.utility.await_new_tweet import AwaitNewTweet
from src.utility.tweet_classifier import TweetClassifier
from src.settings import *
import twitter
import time
import threading
import logging


class TestAwaitTweet:
    logging.basicConfig(level=logging.DEBUG)

    # @pytest.fixture(scope="module", params=["status_id"])
    # def on_exit(self):
    #     yield
    #     api = twitter.Api(consumer_key=consumer_key,
    #                        consumer_secret=consumer_secret,
    #                        access_token_key=access_token_key,
    #                        access_token_secret=access_token_secret)
    #     api.DestroyStatus(status_id=)

    def test(self):
        log = logging.getLogger("test_1")

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
                                last_id_file="SmiteGame_classified_data.json")
        thread = threading.Thread(target=awaiter.await, name="awaiter")

        # create new tweet
        doc1 = "Earn 3 Fantasy Point Boosters for completing 1 First Win of the Day!\n\
                http://www.smitegame.com/team-booster-weekend-june-9-11 ..."
        new_tweet_status = api.PostUpdate(status=doc1)

        log.debug("waiting before we check user timeline most recent tweet")
        print()
        time.sleep(awaiter.poll_rate + 1)
        print("checking ...")
        recheck_statuses = api.GetHomeTimeline(count=1)
        print(recheck_statuses[0].retweeted)
        print(recheck_statuses[0].AsDict())

        assert(new_tweet_status.id == recheck_statuses[0].id)
        api.DestroyStatus(status_id=recheck_statuses[0].id)
