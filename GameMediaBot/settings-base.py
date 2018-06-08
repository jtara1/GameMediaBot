from os.path import dirname, join, basename, abspath

# enter info here from your own twitter app (apps.twitter.com)
# then rename this file as settings.py

consumer_key = ""
consumer_secret = ""
access_token_key = ""
access_token_secret = ""

# used along with python-twitter module & to retweet
my_twitter_screen_name = ""

# used in Emailer class & helps setup yagmail to send emails
__settings_dir = dirname(__file__)
email = ''
gmail_oauth2_file = join(__settings_dir, '../oauth2_creds.json')
email_csv = join(__settings_dir, '../email_list.csv')

