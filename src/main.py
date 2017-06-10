from src.utility.twitter_user import TwitterUser
from src.utility.classification_category import ClassificationCategory


def main():
    fwotd = ClassificationCategory(["FWOTD"])  # first win of the day
    # Note: each str is used to create a regex pattern
    bonus_points = ClassificationCategory(['2x', '3x', '[4-9]x', 'favor', 'gems?', 'free', 'earn', 'worshippers',
                                           'tribute points?', 'exp', 'experience'])
    smite = TwitterUser("SmiteGame", [fwotd, bonus_points])  # smite twitter & its categories of tweets we're matching
