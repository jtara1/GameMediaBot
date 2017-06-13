import asyncio
import twitter
from src.settings import *
import json


class AwaitNewTweet:
    def __init__(self, classifier, trigger_targets, twitter_screen_name, data_file=None):
        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token_key,
                               access_token_secret=access_token_secret)
        self.twitter_screen_name = twitter_screen_name
        data_file = twitter_screen_name + "_classified_data.json" if data_file is None else data_file
        self.most_recent_tweet_id = json.load(open(data_file, 'r'))[0]['id']
        self.clf = classifier
        self.trigger_targets = trigger_targets

    def await(self):
        async def wait_for_new_tweet():
            while True:
                statuses = self.api.GetUserTimeline(
                    screen_name=self.twitter_screen_name,
                    since_id=self.most_recent_tweet_id)
                if len(statuses) > 0:
                    self._process_new_tweets(statuses)
                await asyncio.sleep(10)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(wait_for_new_tweet())

    def _process_new_tweets(self, statuses):
        for s in statuses:
            # if classification of tweet text is in trigger_targets
            if self.clf.classify(s.text)[0] in self.trigger_targets:
                print("Retweeting: " + s.text[:10] + " ...")
                self.api.PostRetweet(s.id)  # retweet this tweet
                self.most_recent_tweet_id = s.id
