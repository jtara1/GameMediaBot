from src.utility.tweet_classifier import TweetClassifier
from src.data_scripts.manual_classification import ManualClassification
from src.utility.await_new_tweet import AwaitNewTweet


if __name__ == "__main__":
    # ManualClassification(twitter_screen_name="SmiteGame", search_keywords=["FWOTD"])

    clf = TweetClassifier(data_file_name="SmiteGame_classified_data.json")
    awaiter = AwaitNewTweet(classifier=clf,
                            trigger_targets=['fwotd', 'bonus_points'],
                            twitter_screen_name="SmiteGame",
                            last_id_file="last_ids.json")
    awaiter.await()  # blocks, waiting for new tweet, classifies/predicts it, retweets if it's in trigger_targets