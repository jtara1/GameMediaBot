import logging
import threading
import time
import twitter
from GameMediaBot.tweet_classifier import TweetClassifier
from GameMediaBot.await_new_tweet import AwaitNewTweet
from GameMediaBot.settings import *


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
                                last_id_file="last_ids.json")
        thread = threading.Thread(target=awaiter.await, name="awaiter")

        # create new tweet
        doc1 = "Earn 3 Fantasy Point Boosters for completing 1 First Win of the Day!\n\
                http://www.smitegame.com/team-booster-weekend-june-9-11 ..."
        doc2 = "Junk tweet for test case, please ignore, this should be deleted shortly..."
        new_tweet_status = api.PostUpdate(status=doc1)
        api.PostUpdate(status=doc2)

        time.sleep(awaiter.poll_rate + 1)
        print("checking statuses/tweets ...")
        recheck_statuses = api.GetHomeTimeline(count=2)
        print(recheck_statuses[1].retweeted)
        print(recheck_statuses[1].AsDict())

        assert(new_tweet_status.id == recheck_statuses[1].id)
        api.DestroyStatus(status_id=recheck_statuses[1].id)
        api.DestroyStatus(status_id=recheck_statuses[0].id)
