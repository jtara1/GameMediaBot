from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
import numpy as np
import json
import twitter
from src.settings import *

class TweetClassifier:
    def __init__(self):
        self.x_train_tfidf = None  # x-values for data training (term freq, inverse doc freq)
        self.clf = None  # classifier
        self._load_fit()

    def _load_fit(self):
        # generator that yields a datum from the pre-classified dataset
        def get_documents(file_name="SmiteGame_classified_data.json", dict_key='text'):
            with open(file_name, 'r') as f:
                docs = json.loads(f.read())
            for doc in docs:
                yield doc[dict_key] if dict_key == 'text' else doc[dict_key][0]

        # for x-values
        count_vect = CountVectorizer()
        x_train_counts = count_vect.fit_transform(get_documents())  # get dict of word count in each document
        print(x_train_counts.shape)  # shape is the numb of docs and numb of unique words throughout all docs

        # term frequency times inverse document frequency (helps docs that spam certain words & downscale common words)
        tf_transformer = TfidfTransformer()
        self.x_train_tfidf = tf_transformer.fit_transform(x_train_counts)

        # for y-values
        count_vect = CountVectorizer()
        y_train_counts = count_vect.fit_transform(get_documents(dict_key='category'))
        print(y_train_counts.shape)

        tf_transformer = TfidfTransformer()
        y_train_tfidf = tf_transformer.fit_transform(y_train_counts)

        text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                                   alpha=1e-3, n_iter=5, random_state=42))])
        # text_clf = text_clf.fit(
        #     get_documents(),
        #     get_documents(dict_key='category'))
        y_raw_data = [x['category'][0] for x in json.load(open("SmiteGame_classified_data.json", 'r'))]
        text_clf = text_clf.fit(
            get_documents(),
            y_raw_data)

        predicted = text_clf.predict(get_documents())

        total = 0
        for prediction, real_answer in zip(predicted, y_raw_data):
            total += prediction == real_answer
            print(prediction == real_answer)
        print("accuracy = {}".format(total / len(predicted)))
        # fit data using Multinomial Naive Bayes
        # self.clf = MultinomialNB().fit(self.x_train_tfidf, y_train_counts)


if __name__ == "__main__":
    pass
