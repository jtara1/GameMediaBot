from src.utility.twitter_user import TwitterUser
from src.utility.classification_category import ClassificationCategory


def main():
    # Note: each str is used to create a regex pattern [wip]
    fwotd = ClassificationCategory(["FWOTD", "[Ff]irst win of the day"])  # first win of the day
    bonus_points = ClassificationCategory(['2x', '3x', '[4-9]x', 'favor', 'gems?', 'free', 'earn', 'worshippers?',
                                           'tribute points?', 'exp', 'experience', 'double', 'triple'])
    smite = TwitterUser("SmiteGame", [fwotd, bonus_points])  # smite twitter & its categories of tweets we're matching
