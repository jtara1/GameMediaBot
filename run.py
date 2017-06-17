from GameMediaBot.tweet_classifier import TweetClassifier
from GameMediaBot.await_new_tweet import AwaitNewTweet


if __name__ == "__main__":
    # ManualClassification(twitter_screen_name="SmiteGame", search_keywords=["FWOTD"])

    smite_classifier = TweetClassifier(data_file_name="SmiteGame_classified_data.json")
    smite_awaiter = AwaitNewTweet(classifier=smite_classifier,
                                  trigger_targets=['fwotd', 'bonus_points'],
                                  twitter_screen_name="SmiteGame",
                                  last_id_file="last_ids.json")
    smite_awaiter.await()  # blocks, waiting for new tweet, classifies/predicts it, retweets if it's in trigger_targets