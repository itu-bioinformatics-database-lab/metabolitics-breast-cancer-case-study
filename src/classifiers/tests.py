import unittest
import logging

from sklearn.model_selection import train_test_split

from services import DataReader, NamingService

from .solution_level_disease_classifier import SolutionLevelDiseaseClassifier
from .dummy_disease_classifier import DummyDiseaseClassifier
from .metabolite_level_disease_classifier \
    import MetaboliteLevelDiseaseClassifier
from .fva_disease_classifier import FVADiseaseClassifier

classification_logger = logging.getLogger('classification')
classification_logger.setLevel(logging.INFO)
classification_logger.addHandler(
    logging.FileHandler('../logs/classification.log'))


class TestMetaboliteLevelDiseaseClassifier(unittest.TestCase):

    def setUp(self):
        self.clf = MetaboliteLevelDiseaseClassifier()
        (X, y) = DataReader().read_all()

        (self.X_train, self.X_test, self.y_train, self.y_test) =  \
            train_test_split(X, y, random_state=0)

        self.clf.fit(self.X_train, self.y_train)

    def test_accuracy(self):
        classification_logger.info('\n %s \n' % str(self.clf))

        train_accuracy = self.clf.score(self.X_train, self.y_train)
        classification_logger.info('train accuracy: %f' % train_accuracy)

        test_accuracy = self.clf.score(self.X_test, self.y_test)
        classification_logger.info('test accuracy: %f' % test_accuracy)

    def test_classification_report(self):
        cr = self.clf.classification_report(self.X_test, self.y_test)
        classification_logger.info('\n %s' % cr)


class TestSolutionLevelDiseaseClassifier(unittest.TestCase):

    def setUp(self):
        self.clf = SolutionLevelDiseaseClassifier()
        (X, y) = DataReader().read_solutions()
        (self.X_train, self.X_test, self.y_train, self.y_test) =  \
            train_test_split(X, y, random_state=0)

        self.clf.fit(self.X_train, self.y_train)

    def test_accuracy(self):
        classification_logger.info('\n %s \n' % str(self.clf))

        train_accuracy = self.clf.score(self.X_train, self.y_train)
        classification_logger.info('train accuracy: %f' % train_accuracy)

        test_accuracy = self.clf.score(self.X_test, self.y_test)
        classification_logger.info('test accuracy: %f' % test_accuracy)

    def test_classification_report(self):
        cr = self.clf.classification_report(self.X_test, self.y_test)
        classification_logger.info('\n %s' % cr)


# class TestFVAClass(unittest.TestCase):
#
#     def setUp(self):
#         self.clf = FVADiseaseClassifier()
#         (X, y) = DataReader().read_all()
#         X = NamingService('recon').to(X)
#         (self.X_train, self.X_test, self.y_train, self.y_test) =  \
#             train_test_split(X, y, random_state=0)
#
#         self.clf.fit(self.X_train, self.y_train)
#
#     def test_accuracy(self):
#         classification_logger.info('\n %s \n' % str(self.clf))
#
#         train_accuracy = self.clf.score(self.X_train, self.y_train)
#         classification_logger.info('train accuracy: %f' % train_accuracy)
#
#         test_accuracy = self.clf.score(self.X_test, self.y_test)
#         classification_logger.info('test accuracy: %f' % test_accuracy)
#
#     def test_classification_report(self):
#         cr = self.clf.classification_report(self.X_test, self.y_test)
#         classification_logger.info('\n %s' % cr)


class TestDummyClassifier(unittest.TestCase):

    def setUp(self):
        self.clf = DummyDiseaseClassifier()
        (X, y) = DataReader().read_solutions()
        (self.X_train, self.X_test, self.y_train, self.y_test) =  \
            train_test_split(X, y, random_state=0)

        self.clf.fit(self.X_train, self.y_train)

    def test_accuracy(self):
        classification_logger.info('\n %s \n' % str(self.clf))

        train_accuracy = self.clf.score(self.X_train, self.y_train)
        classification_logger.info('train accuracy: %f' % train_accuracy)

        test_accuracy = self.clf.score(self.X_test, self.y_test)
        classification_logger.info('test accuracy: %f' % test_accuracy)

    def test_classification_report(self):
        cr = self.clf.classification_report(self.X_test, self.y_test)
        classification_logger.info('\n %s' % cr)
