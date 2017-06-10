import twitter
from src.settings import *


def load():
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)

    statuses = api.GetUserTimeline(screen_name="SmiteGame")
    print(statuses[0].text)


if __name__ == "__main__":
    pass
