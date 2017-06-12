from src.utility.load_data import TweetClassifier
from src.data_scripts.manual_classification import ManualClassification


if __name__ == "__main__":
    cls = TweetClassifier()
    # ManualClassification(twitter_screen_name="SmiteGame", search_keywords=["FWOTD"])