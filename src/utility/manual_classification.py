import twitter
from src.settings import *
import keyboard
import json


def main(twitter_screen_name = "SmiteGame"):
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)

    statuses = api.GetUserTimeline(screen_name=twitter_screen_name, exclude_replies=True)

    # all the tweets that have been classified
    tweets = []
    classification = []

    def add_to_end(l):
        classification.extend(l)

    def write_data_and_exit():
        with open(twitter_screen_name + "_classified_data.json", "w") as f:
            json.dump(tweets, f)
        exit(0)

    keyboard.add_hotkey(hotkey='1', callback=add_to_end, args=([["fwotd"]]))
    keyboard.add_hotkey(hotkey='2', callback=add_to_end, args=([["bonus_points"]]))
    keyboard.add_hotkey(hotkey='3', callback=add_to_end, args=([["fwotd", "bonus_points"]]))
    keyboard.add_hotkey(hotkey='esc', callback=write_data_and_exit)

    for s in statuses:
        classification = []
        print(s.text)
        print("[1] First win of the day event\n[2] Bonus points (exp, gold, etc.) event\n"
              "[3] Both FWOTD & bonus points\n[Esc] Save Previous to file\n[Enter] Continue\n"
              "[Ctrl+c] Exit")

        keyboard.wait('enter')
        print("-" * 10)
        tweets.append({'id': s.id,
                       'text': s.text,
                       'category': classification})
