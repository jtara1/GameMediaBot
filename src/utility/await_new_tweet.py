import asyncio
import twitter
import json
import logging
from src.settings import *
from src.utility.general import get_first_x_words


class AwaitNewTweet:
    def __init__(self,
                 classifier,
                 trigger_targets,
                 twitter_screen_name,
                 last_id_file="last_ids.json",
                 poll_rate=10):
        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token_key,
                               access_token_secret=access_token_secret)
        self.twitter_screen_name = twitter_screen_name
        self.last_ids_file = last_id_file
        self.last_ids = json.load(open(last_id_file, 'r'))
        self.most_recent_tweet_id = self.last_ids[twitter_screen_name.lower()]
        self.clf = classifier
        self.trigger_targets = trigger_targets
        self.poll_rate = poll_rate
        self.loop = None
        self.log = logging.getLogger("AwaitNewTweet")

    def await(self):
        async def wait_for_new_tweet():
            while True:
                statuses = self.api.GetUserTimeline(
                    screen_name=self.twitter_screen_name,
                    since_id=self.most_recent_tweet_id)
                if len(statuses) > 0:
                    self._process_new_tweets(statuses)
                await asyncio.sleep(self.poll_rate)

        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(wait_for_new_tweet())

    def stop(self):
        if self.loop is not None:
            self.loop.stop()
            self.loop.close()

    def _process_new_tweets(self, statuses):
        for s in statuses:
            # if classification of tweet text is in trigger_targets
            if self.clf.classify(s.text)[0] in self.trigger_targets:
                print("Retweeting: " + get_first_x_words(s.text, 10) + " ...")
                self.api.PostRetweet(s.id)  # retweet this tweet
            else:
                self.log.debug("Not retweeting: {} ...".format(get_first_x_words(s.text, 10)))

        # update dict and json file with most recent twitter id processed
        self.most_recent_tweet_id = statuses[-1].id
        self.last_ids[self.twitter_screen_name.lower()] = self.most_recent_tweet_id
        json.dump(self.last_ids, open(self.last_ids_file, 'w'))
