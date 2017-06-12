from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
import json


class TweetClassifier:
    def __init__(self, data_file_name="SmiteGame_classified_data.json"):
        self.x_train_tfidf = None  # x-values for data training (term freq, inverse doc freq)
        self.clf = None  # classifier
        self.data_file_name = data_file_name  # file containing a list of dictionaries with 'text' and 'category' keys

        self._load_and_fit()
        self.print_metrics()

    def _load_and_fit(self):
        # takes raw data, applies transforms on it, then puts the transformed data through the estimator / classifier
        self.clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                                   alpha=1e-3, n_iter=5, random_state=42))])

        # list of documents (each document is a body of text)
        self.x_raw_data = [d['text'] for d in json.load(open(self.data_file_name, 'r'))]
        # list of classification for each document
        self.y_raw_data = [d['category'][0] for d in json.load(open(self.data_file_name, 'r'))]
        self.clf = self.clf.fit(
            self.x_raw_data,
            self.y_raw_data)

        # extract y-feature (categories) names
        v = CountVectorizer()
        v.fit_transform(self.y_raw_data)
        self.target_names = v.get_feature_names()

    def print_metrics(self):
        predicted = self.clf.predict(self.x_raw_data)
        print(metrics.classification_report(self.y_raw_data, predicted, target_names=self.target_names))

    def classify(self, document):
        if not isinstance(document, list):
            document = [document]
        return self.clf.predict(document)

if __name__ == "__main__":
    pass
