import twitter
from src.settings import *
import keyboard
import json
import os
import colorama
colorama.init()


class ManualClassification:
    def __init__(self, twitter_screen_name="SmiteGame"):
        self.classification = []
        self.twitter_screen_name = twitter_screen_name
        self.file_name = "{0}_classified_data.json".format(twitter_screen_name)
        self.last_id = None
        self.tweets = []

        self.load_last_id()
        self.main()

    def load_last_id(self):
        if os.path.isfile(self.file_name):
            with open(self.file_name, 'r') as f:
                self.tweets = json.load(f)
            self.last_id = self.tweets[-1]['id']

    def main(self):
        """
        Iterates from most recent to oldest tweets asking the user to classify which type it is 
        Script requires su privilege if running on Linux because of the keyboard library
        e.g.: $ sudo manual_classification.py
        Args:
            twitter_screen_name (str): 
                Name seen when visiting the twitter profile. Tweets will be pulled from this profile
        Returns:
            None. Output can be a .json file containing data of tweets with classification when user commands it
        """
        api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token_key,
                          access_token_secret=access_token_secret)

        statuses = api.GetUserTimeline(screen_name=self.twitter_screen_name,
                                       max_id=self.last_id,
                                       exclude_replies=True)

        def classify_as(src):
            self.classification = src

        def save():
            with open(self.file_name, "w") as f:
                json.dump(self.tweets, f)
            print("\nDone, safe to exit")

        keyboard.add_hotkey(hotkey='1', callback=classify_as, args=([["fwotd"]]))
        keyboard.add_hotkey(hotkey='2', callback=classify_as, args=([["bonus_points"]]))
        # keyboard.add_hotkey(hotkey='3', callback=classify_as, args=([["fwotd", "bonus_points"]]))
        # keyboard.add_hotkey(hotkey='esc', callback=save)

        for s in statuses:
            self.classification = ["dont_care"]
            print(colorama.Fore.RED + s.text + colorama.Style.RESET_ALL)
            print("[1] First win of the day event\n[2] Bonus points (exp, gold, etc.) event\n"
                  "[Enter] Continue\n"
                  "[Ctrl+c] Save PREVIOUS & Exit")

            try:
                keyboard.wait('enter')
            except KeyboardInterrupt as e:
                save()
                break

            print("-" * 10)
            self.tweets.append({'id': s.id,
                                'text': s.text,
                                'category': self.classification})
