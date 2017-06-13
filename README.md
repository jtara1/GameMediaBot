# GameMediaBot

Have you followed your favorite online game's social media to 
receive notices of the special events such as 2x exp, gold,
f2p weekend,
or other similar events only to realize 90% of their tweets
you really don't care about?

This program solves this by: awaiting for new tweets from
a twitter user, classifying the new tweet using the 
support vector machine (SVM) machine learning algo
trained with pre-classified data (created by running my
script which assists one in building it), and retweets
the tweet when it's classified as a desired or target
categorized tweet.

---

### Helpful links

- [sklearn: working with text data](http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)
- [multiclass/label (haven't used this)](http://scikit-learn.org/stable/modules/multiclass.html#multiclass)
