from src.utility.load_data import TweetClassifier
from src.data_scripts.manual_classification import ManualClassification


if __name__ == "__main__":
    clf = TweetClassifier()
    doc1 = """Earn 3 Fantasy Point Boosters for completing 1 First Win of the Day!\n
    http://www.smitegame.com/team-booster-weekend-june-9-11 …"""
    doc2 = """The Joki's on you! Unless you take advantage of 25% off Scarlet Court Chests - on sale now!
    pic.twitter.com/H58lx7r8xt"""

    print(clf.classify(doc1))
    print(clf.classify(doc2))
    # ManualClassification(twitter_screen_name="SmiteGame", search_keywords=["FWOTD"])