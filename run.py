from GameMediaBot.tweet_classifier import TweetClassifier
from GameMediaBot.await_new_tweet import AwaitNewTweet
from GameMediaBot.utility.file_writer import FileWriter
import os
import click


@click.command()
@click.option(
    '--retrain', default=False, is_flag=True, help="Train the classifier again instead of deserializing.")
@click.option(
    '--print-metrics', default=False, is_flag=True, help="""Print the accuracy of the training data classified with 
                                                         the classifier that was trained on it.""")
def main(retrain=False, print_metrics=False):
    # ManualClassification(twitter_screen_name="SmiteGame", search_keywords=["FWOTD"])

    last_ids_file = os.path.join(os.getcwd(), 'last_ids.json')
    file_writer = [FileWriter(file_name=last_ids_file)]

    smite_classifier = TweetClassifier(data_file_name="SmiteGame_classified_data.json",
                                       retrain=retrain,
                                       print_metrics=print_metrics)
    smite_awaiter = AwaitNewTweet(classifier=smite_classifier,
                                  trigger_targets=['fwotd', 'bonus_points'],
                                  twitter_screen_name="SmiteGame",
                                  last_id_file="last_ids.json",
                                  file_writer=file_writer)
    smite_awaiter.await()  # blocks, waiting for new tweet, classifies/predicts it, retweets if it's in trigger_targets


if __name__ == "__main__":
    main()
