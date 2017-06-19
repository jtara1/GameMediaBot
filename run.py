from GameMediaBot.tweet_classifier import TweetClassifier
from GameMediaBot.await_new_tweet import AwaitNewTweet
from GameMediaBot.utility.file_writer import FileWriter
import os


if __name__ == "__main__":
    # ManualClassification(twitter_screen_name="SmiteGame", search_keywords=["FWOTD"])

    last_ids_file = os.path.join(os.getcwd(), 'last_ids.json')
    file_writer = [FileWriter(file_name=last_ids_file)]

    smite_classifier = TweetClassifier(data_file_name="SmiteGame_classified_data.json")
    smite_awaiter = AwaitNewTweet(classifier=smite_classifier,
                                  trigger_targets=['fwotd', 'bonus_points'],
                                  twitter_screen_name="SmiteGame",
                                  last_id_file="last_ids.json",
                                  file_writer=file_writer)
    smite_awaiter.await()  # blocks, waiting for new tweet, classifies/predicts it, retweets if it's in trigger_targets
