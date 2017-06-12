from src.utility.tweet_classifier import TweetClassifier
from src.data_scripts.manual_classification import ManualClassification
from src.utility.await_new_tweet import AwaitNewTweet


if __name__ == "__main__":
    clf = TweetClassifier(data_file_name="SmiteGame_classified_data.json")
    # doc1 = """Earn 3 Fantasy Point Boosters for completing 1 First Win of the Day!\n
    # http://www.smitegame.com/team-booster-weekend-june-9-11 …"""
    # doc2 = """The Joki's on you! Unless you take advantage of 25% off Scarlet Court Chests - on sale now!
    # pic.twitter.com/H58lx7r8xt"""
    #
    # print(clf.classify(doc1))
    # print(clf.classify(doc2))
    # ManualClassification(twitter_screen_name="SmiteGame", search_keywords=["FWOTD"])
    awaiter = AwaitNewTweet(classifier=clf,
                            trigger_targets=['fwotd', 'bonus_points'],
                            twitter_screen_name="gamsee21329131",
                            data_file="SmiteGame_classified_data.json")
