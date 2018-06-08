# GameMediaBot

Have you followed your favorite online game's social media to 
receive notices of the special events such as 2x exp, gold,
f2p weekend,
or other similar events only to realize 90% of their tweets
you really don't care about?

This program solves this by: awaiting for new tweets from
a twitter user, classifying the new tweet using sklearn support vector machine
trained with pre-classified data (created by running my
script which assists one in building it), and retweets
the tweet when it's classified as a desired or target
categorized tweet.

Program tested on Linux with Python 3.5
 

## Install

```bash
git clone https://github.com/jtara1/GameMediaBot
sudo pip3.5 install -r requirements.txt

python3 -c "import nltk;
	nltk.download('stopwords');
	nltk.download('punkt')"
```

- You'll also need to go to [apps twitter site](https://apps.twitter.com/) to create an app to get the four things
(and your twitter username/screen name) to update the file `settings-base.py` then 
rename the file to `settings.py`

## Usage
By default, the code will use the tweets I've classified myself as training data to classify
future tweets from SmiteGame twitter.
```
python3 run.py
```

__or__

You can train your own set of tweets from a certain twitter account by running
```
sudo python3 manual_classification.py 
```
_Note:_ sudo is needed by the `keyboard` library when running on Linux.

Then you'd need to update the code in `run.py` to monitor the twitter account of interest
using the data to classified as training data for the classification algorithm.

---

### Helpful links

- [sklearn: working with text data](http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)
- [multiclass/label (haven't used this)](http://scikit-learn.org/stable/modules/multiclass.html#multiclass)
