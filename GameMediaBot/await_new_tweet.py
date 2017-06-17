import asyncio
import twitter
import json
import logging
from GameMediaBot.settings import *
from GameMediaBot.utility.general import get_first_x_words


class AwaitNewTweet:
    """ Monitors an account for new tweets. Classifies the new tweets. Retweets the tweets if they're classified as
        a trigger tweet.
    
        Args:
            classifier (TweetClassifier):
                An estimator that's been trained on a dataset and ready to classify a document by calling classify(doc)
                on it
            trigger_targets (list of str):
                If classifier classifies as a str found in trigger_targets, it retweets (or triggers)
            twitter_screen_name (str):
                The username of the twitter account we're monitoring 
            last_id_file (str):
                File path pointing to file that contains a JSON dictionary containing keys of screen_names with values
                of the last id processed for the screen_name
            poll_rate (int or float):
                The time (seconds) between cycles in the event loop that checks if a new tweet was tweeted
    """
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
        self.twitter_screen_name = twitter_screen_name.lower()
        self.last_ids_file = last_id_file
        self.last_ids = json.load(open(last_id_file, 'r'))

        if self.twitter_screen_name not in self.last_ids:
            self._define_new_most_recent_tweet()
        else:
            self.most_recent_tweet_id = self.last_ids[self.twitter_screen_name]

        self.clf = classifier
        self.trigger_targets = trigger_targets
        self.poll_rate = poll_rate
        self.loop = None
        self.log = logging.getLogger("AwaitNewTweet")

    def _define_new_most_recent_tweet(self):
        """ Update the JSON file and the dictionary in case this twitter_screen_name has no defined last tweet id """
        self.most_recent_tweet_id = self.api.GetUserTimeline(screen_name=self.twitter_screen_name, count=2)[1].id
        self.last_ids[self.twitter_screen_name] = self.most_recent_tweet_id

    def await(self):
        """ Event loop that will BLOCK FOREVER checking for new tweets then sending them down if new """
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
        """ Stop the event loop """
        if self.loop is not None:
            self.loop.stop()
            self.loop.close()

    def _process_new_tweets(self, statuses):
        """ Retweet the tweets from statuses if they're classified as a trigger tweet/target 
            Args:
                statuses (list of twitter.model.Status):
                    Iterate through these, classifying each
        """
        for s in statuses:
            # if classification of tweet text is in trigger_targets
            if self.clf.classify(s.text)[0] in self.trigger_targets:
                print("Retweeting: " + get_first_x_words(s.text, 10) + " ...")
                self.api.PostRetweet(s.id)  # retweet this tweet
            else:
                self.log.debug("Not retweeting: id={}, {} ...".format(s.id, get_first_x_words(s.text, 10)))

        # update dict and json file with most recent twitter id processed
        self.most_recent_tweet_id = statuses[-1].id
        self.last_ids[self.twitter_screen_name] = self.most_recent_tweet_id
        json.dump(self.last_ids, open(self.last_ids_file, 'w'))
