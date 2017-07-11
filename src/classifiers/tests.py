import unittest
import logging
import json

import numpy as np
from sklearn.model_selection import cross_val_score, StratifiedKFold

from services import DataReader

from .dummy_disease_classifier import DummyDiseaseClassifier
from .metabolite_level_disease_classifier \
    import MetaboliteLevelDiseaseClassifier
from .fva_disease_classifier import FVADiseaseClassifier
from .pathifier_disease_classifier import PathifierDiseaseClassifier

classification_logger = logging.getLogger('classification')
classification_logger.setLevel(logging.INFO)
classification_logger.addHandler(
    logging.FileHandler('../logs/classification.log'))


class MachineLearningTestCases:
    class ClassificationTestCase(unittest.TestCase):
        def setUpClf(self):
            raise NotImplementedError

        def setUpData(self):
            raise NotImplementedError

        def setUp(self):
            self.clf = self.setUpClf()
            (self.X, self.y) = self.setUpData()
            self.X = np.array(self.X)
            self.y = np.array(self.y)
            self.kf = StratifiedKFold(n_splits=10, random_state=43)
            classification_logger.info('\n %s \n' % str(self.clf))

        def folds(self):
            for train_index, test_index in self.kf.split(self.X, self.y):
                yield (self.X[train_index], self.X[test_index],
                       self.y[train_index], self.y[test_index])

        def accuracy_scores(self, X_train, X_test, y_train, y_test):
            classification_logger.info(
                'train accuracy: %f' % self.clf.score(X_train, y_train))
            classification_logger.info(
                'test accuracy: %f' % self.clf.score(X_test, y_test))

        def classification_report(self, X_test, y_test):
            cr = self.clf.classification_report(X_test, y_test)
            classification_logger.info('\n %s' % cr)

        def test_kfold(self):
            for X_train, X_test, y_train, y_test in self.folds():
                self.clf.fit(X_train, y_train)
                self.accuracy_scores(X_train, X_test, y_train, y_test)
                self.classification_report(X_test, y_test)

        def test_kfold_on_average_test_accuracy(self):
            for scoring in ['accuracy', 'f1_micro']:
                score = cross_val_score(
                    self.clf,
                    self.X,
                    self.y,
                    cv=self.kf,
                    n_jobs=-1,
                    scoring=scoring)
                classification_logger.info('kfold test %s: %s' % (scoring,
                                                                  score))
                classification_logger.info('mean: %s' % score.mean())
                classification_logger.info('std: %s' % score.std())


class TestMetaboliteLevelDiseaseClassifier(
        MachineLearningTestCases.ClassificationTestCase):
    def setUpClf(self):
        return MetaboliteLevelDiseaseClassifier()

    def setUpData(self):
        return DataReader().read_data('BC')
        # return DataReader().read_data('HCC')


class TestPathifierDiseaseClassifier(
        MachineLearningTestCases.ClassificationTestCase):
    def setUpClf(self):
        return PathifierDiseaseClassifier()

    def setUpData(self):
        return DataReader().read_data('BC_regulization')


class TestFVAClass(MachineLearningTestCases.ClassificationTestCase):
    def setUpClf(self):
        return FVADiseaseClassifier()

    def setUpData(self):
        path = '../dataset/solutions/bc_disease_analysis#k=1.json'

        X, y = zip(*[json.loads(i) for i in open(path)][0])

        return X, y
        # return DataReader().read_fva_solutions(
        #     'fva_solution_with_basic_fold_change.json')


class TestDummyClassifier(MachineLearningTestCases.ClassificationTestCase):
    def setUpClf(self):
        return DummyDiseaseClassifier()

    def setUpData(self):
        return DataReader().read_solutions()
