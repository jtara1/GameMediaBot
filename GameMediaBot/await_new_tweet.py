import asyncio
import twitter
import json
import logging
import os
import colorama
from GameMediaBot.settings import *
from GameMediaBot.utility.general import get_first_x_words
from GameMediaBot.emailer import Emailer
colorama.init()


class AwaitNewTweet:
    """ Monitors an account for new tweets. Classifies the new tweets. Retweets the tweets if they're classified as
        a trigger tweet.
    
        Args:
            classifier (TweetClassifier):/home/j/Documents/_Github-Projects/GameMediaBot
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
                 poll_rate=121,
                 file_writer=None,
                 email='',
                 gmail_oauth2_file='',
                 email_csv=''):
        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token_key,
                               access_token_secret=access_token_secret)
        self.twitter_screen_name = twitter_screen_name.lower()
        self.last_ids_file = last_id_file
        # create if not yet created
        if not os.path.isfile(last_id_file):
            with open(last_id_file, 'w') as f:
                f.write('{}')
        self.last_ids = json.load(open(last_id_file, 'r'))

        # no record of last id for this twitter user
        if self.twitter_screen_name not in self.last_ids:
            self._define_new_most_recent_tweet()
        else:
            self.most_recent_tweet_id = self.last_ids[self.twitter_screen_name]

        self.clf = classifier
        self.trigger_targets = trigger_targets
        self.poll_rate = poll_rate
        self.loop = None
        self.log = logging.getLogger("AwaitNewTweet")
        # setup logging (imported from github.com/jtara1/turbo_palm_tree)
        logging.basicConfig(
            filename='logger.log',
            format='%(levelname)s | %(name)s | %(asctime)s | %(message)s',
            datefmt='%m/%d/%y %H:%M:%S',
            level=logging.DEBUG)

        if file_writer is not None:
            self.file_writer = file_writer[0]  # dereference
            # only need to have dictionary containing last id for this twitter acc we're monitoring
            self.last_ids = {self.twitter_screen_name: self.last_ids[self.twitter_screen_name]}
        else:
            self.file_writer = file_writer

        self.emailer = Emailer(email, gmail_oauth2_file, email_csv)

    def _define_new_most_recent_tweet(self):
        """ Update the JSON file and the dictionary in case this twitter_screen_name has no defined last tweet id """
        self.most_recent_tweet_id = self.api.GetUserTimeline(screen_name=self.twitter_screen_name, count=10)[-1].id
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
        # iterate from oldest to newest (tweet) statuses
        for s in sorted(statuses, key=lambda status: status.id):
            # if classification of tweet text is in trigger_targets
            if self.clf.classify(s.text) in self.trigger_targets:
                self._trigger_tweet_found(s)
            else:
                self._trigger_tweet_not_found(s)

        # update dict and json file with most recent twitter id processed
        self.most_recent_tweet_id = statuses[0].id
        self.last_ids[self.twitter_screen_name] = self.most_recent_tweet_id
        if self.file_writer is None:
            json.dump(self.last_ids, open(self.last_ids_file, 'w'))
        else:
            self.file_writer.write(self.last_ids)

    def _trigger_tweet_found(self, tweet):
        status_str = "Retweeting: " + get_first_x_words(tweet.text, 10) + " ..."
        print(colorama.Fore.GREEN + status_str + colorama.Style.RESET_ALL)
        self.log.debug(status_str)  # store in log
        self.api.PostRetweet(tweet.id)  # retweet this tweet
        self.emailer.send_to_all(
            '{}: New Event!'.format(self.twitter_screen_name),
            """<html>
            <body>
            <a href="{tweet_link}" />
            <p>{tweet_text}</p>
            </body>
            </html>
            """.format(
                tweet_link='https://www.twitter.com/{}/status/{}'
                    .format(self.twitter_screen_name, tweet.id),
                tweet_text=tweet.text
            )
        )

    def _trigger_tweet_not_found(self, tweet):
        status_str = "Not retweeting: id={}, {} ..."\
            .format(tweet.id, get_first_x_words(tweet.text, 10))
        print(colorama.Fore.RED + status_str + colorama.Style.RESET_ALL)
        self.log.debug(status_str)
