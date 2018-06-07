import json
from weka.classifiers import Classifier, Evaluation
from weka.core.classes import Random
from weka.core.converters import Loader, Saver
from os.path import dirname, basename, join
from transform_to_arff import transform

import weka.core.jvm as jvm
jvm.start()


class TweetClassifier2:
    def __init__(self, twitter_user='SmiteGame'):
        self.__dir = dirname(__file__)
        self.twitter_user = twitter_user
        self.training_data_file = join(
            dirname(__file__),
            '../{}_classified_data.arff'.format(twitter_user)
        )

        self.loader = Loader(classname="weka.core.converters.ArffLoader")
        data = self.loader.load_file(self.training_data_file)
        data.class_is_last()

        # the classes / categories we are classifying tweets as
        self.categories = data.attribute(data.class_index).values

        self.classifier = Classifier(classname='weka.classifiers.trees.J48',
                                     options=['-C', '0.3'])
        self.classifier.build_classifier(data)

    def classify(self, document):
        """Use the trained classifier to determine the class of this
        new document

        :param document: <str> body of text to classify
        :return: <str> name of the class / category of the document
        """
        document = {
            'text': document,
            'category': ['?'],
        }
        # save as json
        fp = join(self.__dir, '../{}_new_doc.json'.format(self.twitter_user))
        json.dump([document], open(fp, 'w'))

        # transform to arff conforming to attributes from trained data set
        arff_file = transform(
            fp,
            'dont_care',
            80,
            self.training_data_file
        )

        data = self.loader.load_file(arff_file)
        data.class_is_last()
        predicted = self.classifier.classify_instance(data.get_instance(0))

        return self.categories[int(predicted)]


if __name__ == '__main__':
    t = TweetClassifier2()
    print(t.classify("Grab a friend and Party Up!\n\nIt's time for Party Up Weekend! Earn bonus Worshipers, Favor, and XP for having partyi\u2026 https://t.co/2xaVgekmaD"))