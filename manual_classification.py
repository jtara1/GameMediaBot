import twitter
from GameMediaBot.settings import *
from GameMediaBot.utility.general import get_first_x_words
import keyboard
import json
import os
import colorama
import datetime
colorama.init()


class ManualClassification:
    def __init__(self, twitter_screen_name, categories, start_from_most_recent=False):
        """
        
        Args:
            twitter_screen_name (str): 
                Name seen when visiting the twitter profile. Tweets will be pulled from this profile 
            categories (list of str):
                The names of the categories you wish to classify the tweets as
            start_from_most_recent (bool):
                Begins iterating over the twitter timeline from the most recent tweet to the older ones if True
        """
        self.classification = []
        self.twitter_screen_name = twitter_screen_name
        self.file_name = "{0}_classified_data.json".format(twitter_screen_name)
        self.last_id = None
        self.tweets = []
        self.statuses = None
        self.categories = categories
        self.start_from_most_recent = start_from_most_recent
        self.first_load = True

        # begin
        while True:
            self._load_last_id()
            self._get_statuses(start_from_most_recent=(self.first_load and self.start_from_most_recent))
            self._iterate_over_statuses()
            self.first_load = False

    def _load_last_id(self):
        if os.path.isfile(self.file_name):
            with open(self.file_name, 'r') as f:
                self.tweets = json.load(f)
            self.last_id = self.tweets[-1]['id']

    def _get_date(self):
        today = datetime.datetime.utcnow()
        return "{0}-{1}-{2}".format(today.year, today.month, today.day)

    def _get_statuses(self, start_from_most_recent=False):
        """ 
        Script requires root privilege if running on Linux because of the keyboard library
        Examples: $ sudo manual_classification.py
        Returns:
            None. Output can be a .json file containing data of tweets with 
            classification when user commands it
        """
        api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token_key,
                          access_token_secret=access_token_secret)

        max_id = None if start_from_most_recent else self.last_id  # if max_id is none, it starts from beginning
        self.statuses = api.GetUserTimeline(screen_name=self.twitter_screen_name,
                                            count=200,  # 200 is max amount permitted by python-twitter
                                            max_id=max_id,
                                            include_rts=False,
                                            exclude_replies=True)

    def _iterate_over_statuses(self):
        def classify_as(classification):
            self.classification = classification

        def save():
            with open(self.file_name, "w") as f:
                json.dump(self.tweets, f)
            print("\nSave completed, safe to exit")

        if len(self.categories) > 9:
            raise ValueError("Auto hotkey assignment will screw up with more than 9 categories")

        ui_str = ""
        for count, category in enumerate(self.categories):
            keyboard.add_hotkey(hotkey=str(count+1), callback=classify_as, args=([[category]]))
            ui_str += "[{count}] {category}\n".format(count=count+1, category=category)
        ui_str += "[Enter] Continue\n[Ctrl+c] Save PREVIOUS & Exit"

        # O(n^n) (worse because it'll block, waiting for user input)
        for s in self.statuses:
            duplicate = False
            # adds terrible runtime, but I don't want redundant or ambiguous data
            # if this tweet has already been processed, skip to next iteration
            # O(n)
            for i in self.tweets:
                if i['id'] == s.id:
                    print("duplicate: " + get_first_x_words(s.text, 10) + " ...")
                    duplicate = True
                    break
            if duplicate:
                continue

            self.classification = ["dont_care"]
            print(colorama.Fore.RED + s.text + colorama.Style.RESET_ALL)
            print(ui_str)

            try:
                keyboard.wait('enter')
            except KeyboardInterrupt:
                save()
                exit(0)

            print("-" * 10)

            self.tweets.append({"id": s.id,
                                "text": s.text,
                                "category": self.classification})

        self.tweets.sort(key=lambda d: d['id'], reverse=True)  # sort tweets from newest to oldest
        save()


if __name__ == "__main__":
    """ The categories I've used and what they represent:
        fwotd: First win of the day special event (often used to give free gems away in Smite)
        bonus_points: Additional experience or currency gained event
        f2p: Free to play event
        game_sale: The game is being sold at a discounted price
        promotion: In game content is being sold at a discount (or possibly free)
    """
    ManualClassification(twitter_screen_name="SmiteGame",
                         categories=["fwotd", "bonus_points"],
                         start_from_most_recent=True)
    # ManualClassification(twitter_screen_name="PlayOverwatch",
    #                      categories=["f2p", "game_sale", "promotion", "bonus_points"])
