from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
import json
import os
import pickle
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV


class TweetClassifier:
    """ Automatically does the following given a file_name for the dataset to train classifier:
        1. Load data from a JSON file formatted as list of dictionaries:
        Example:
        [
          {
            "id": 873190710291431424,
            "text": "Get Boosted! This weekend, complete a FWOTD to earn 3 Team Boosters!\n\n
                https://t.co/KRylCKb1AZ https://t.co/LjGRReHAib",
            "category": ["fwotd"]
          }
        ]
        2. The x vector of raw data is the list of "text" value from each dict, and the y vector of raw data is
        the "category" value from each dict. (These vectors are both parallel of course)
        3. Raw data lists are passed through the sklearn Pipeline which transforms the data into ndarray to be 
        trained.
        
        Ready to classify a new document or test classification with the same x-values used to train it via
        print_metrics method.
        This class is more or less the boilerplate code from 
        http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
        It has 100% accuracy so far with my training dataset of 218 tweets for @SmiteGame
        
        Args:
            data_file_name (str):
                Name of the file containing the dataset which is used to train the classifier
    """
    def __init__(self, data_file_name="SmiteGame_classified_data.json"):
        self.clf = None  # classifier
        self.data_file_name = data_file_name  # file containing a list of dictionaries with 'text' and 'category' keys
        self.persistant_trained_model_file = "SGD_Trained_{}.pkl".format(data_file_name.split(".json")[0])

        if not os.path.isfile(self.persistant_trained_model_file):
            self._load_and_fit()
        else:
            self._load(get_classifier_from_file=True)

    def _load(self, get_classifier_from_file=False):
        # list of documents (each document is a body of text)
        self.x_raw_data = [d['text'] for d in json.load(open(self.data_file_name, 'r'))]
        # list of classification for each document
        self.y_raw_data = [d['category'][0] for d in json.load(open(self.data_file_name, 'r'))]

        # extract y-feature (categories) names
        v = CountVectorizer()
        v.fit_transform(self.y_raw_data)
        self.target_names = v.get_feature_names()

        # takes raw data, applies transforms on it, then trains the estimator / classifier with the data
        self.clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                                   alpha=1e-3, n_iter=5, random_state=42))])

        if get_classifier_from_file:
            self.clf = joblib.load(self.persistant_trained_model_file)

    def _load_and_fit(self):
        """ Load data from file via JSON and pass the data through the Pipeline """
        self._load()  # load raw data (x, y vectors and target names)

        self.clf = self.clf.fit(
            self.x_raw_data,
            self.y_raw_data)

        # save estimator to file
        joblib.dump(self.clf, self.persistant_trained_model_file)

    def print_metrics(self):
        predicted = self.clf.predict(self.x_raw_data)
        print(metrics.classification_report(self.y_raw_data, predicted, target_names=self.target_names))

    def classify(self, document):
        """ Classify a document (body of text) using the classifier that was trained
            Args:
                document (str):
                    Any text that'll be classified as a category.
            Returns (list of str):
                The list of the names of the categories this document has been classified as.
        """
        if not isinstance(document, list):
            document = [document]
        return self.clf.predict(document)

if __name__ == "__main__":
    pass
