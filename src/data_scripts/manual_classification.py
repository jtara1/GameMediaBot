import twitter
from src.settings import *
import keyboard
import json
import os
import colorama
import datetime
colorama.init()


class ManualClassification:
    def __init__(self, twitter_screen_name="SmiteGame", search_keywords=()):
        """
        
        Args:
            twitter_screen_name (str): 
                Name seen when visiting the twitter profile. Tweets will be pulled from this profile 
        """
        self.classification = []
        self.twitter_screen_name = twitter_screen_name
        self.file_name = "{0}_classified_data.json".format(twitter_screen_name)
        self.last_id = None
        self.tweets = []
        self.statuses = None

        # begin
        self._load_last_id()
        self._get_statuses(search_keywords)
        self._iterate_over_statuses()

    def _load_last_id(self):
        if os.path.isfile(self.file_name):
            with open(self.file_name, 'r') as f:
                self.tweets = json.load(f)
            self.last_id = self.tweets[-1]['id']

    def _get_date(self):
        today = datetime.datetime.utcnow()
        return "{0}-{1}-{2}".format(today.year, today.month, today.day)

    def _get_statuses(self, keywords):
        """ 
        Script requires su privilege if running on Linux because of the keyboard library
        e.g.: $ sudo manual_classification.py
        Returns:
            None. Output can be a .json file containing data of tweets with classification when user commands it
        """
        api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token_key,
                          access_token_secret=access_token_secret)

        # build twitter search query
        raw_query = "q=from%3A{acc}".format(acc=self.twitter_screen_name)
        for w in keywords:
            raw_query += "+{word}".format(word=w)

        self.statuses = api.GetUserTimeline(screen_name=self.twitter_screen_name,
                                            count=40,
                                            max_id=self.last_id,
                                            include_rts=False,
                                            exclude_replies=True)

    def _iterate_over_statuses(self):
        def abbreviate(text):
            return " ".join(text.split(" ")[:10])

        def classify_as(src):
            self.classification = src

        def save():
            with open(self.file_name, "w") as f:
                json.dump(self.tweets, f)
            print("\nSave completed, safe to exit")

        keyboard.add_hotkey(hotkey='1', callback=classify_as, args=([["fwotd"]]))
        keyboard.add_hotkey(hotkey='2', callback=classify_as, args=([["bonus_points"]]))

        # O(n^n) (worse because it'll block, waiting for user input)
        for s in self.statuses:
            duplicate = False
            # adds terrible runtime, but I don't want redundant or ambiguous data
            # if this tweet has already been processed, skip to next iteration
            # O(n)
            for i in self.tweets:
                if i['id'] == s.id:
                    print("duplicate: " + abbreviate(s.text) + " ...")
                    duplicate = True
                    break
            if duplicate:
                continue

            self.classification = ["dont_care"]
            print(colorama.Fore.RED + s.text + colorama.Style.RESET_ALL)
            print("[1] First win of the day event\n"
                  "[2] Bonus points (exp, gold, etc.) event\n"
                  "[Enter] Continue\n"
                  "[Ctrl+c] Save PREVIOUS & Exit")

            try:
                keyboard.wait('enter')
            except KeyboardInterrupt as e:
                break

            print("-" * 10)

            self.tweets.append({"id": s.id,
                                "text": s.text,
                                "category": self.classification})

        self.tweets.sort(key=lambda d: d['id'], reverse=True)  # sort tweets from newest to oldest
        save()
