import unittest
import logging
import json

import numpy as np
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import precision_recall_fscore_support

from services import DataReader

from .metabolite_level_disease_classifier \
    import MetaboliteLevelDiseaseClassifier
from .fva_disease_classifier import FVADiseaseClassifier
from .pathifier_disease_classifier import PathifierDiseaseClassifier
from .paradigm_disease_classifier import ParadigmDiseaseClassifier
from .biomass_disease_classifier import BiomassDiseaseClassifier

logger = logging.getLogger(__name__)


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
            logger.info('\n %s \n' % str(self.clf))

        def folds(self):
            for train_index, test_index in self.kf.split(self.X, self.y):
                yield (self.X[train_index], self.X[test_index],
                       self.y[train_index], self.y[test_index])

        def accuracy_scores(self, X_train, X_test, y_train, y_test):
            logger.info(
                'train accuracy: %f' % self.clf.score(X_train, y_train))
            logger.info('test accuracy: %f' % self.clf.score(X_test, y_test))

        def classification_report(self, X_test, y_test):
            cr = self.clf.classification_report(X_test, y_test)
            logger.info('\n %s' % cr)

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
                logger.info('kfold test %s: %s' % (scoring, score))
                logger.info('mean: %s' % score.mean())
                logger.info('std: %s' % score.std())

        @unittest.skip('long running tests')
        def test_on_average_classification_report(self):
            results = list()
            for X_train, X_test, y_train, y_test in self.folds():
                self.clf.fit(X_train, y_train)
                y_pred = self.clf.predict(X_test)

                result = precision_recall_fscore_support(y_test, y_pred)
                logger.info('\n %s' % str(result))
                results.append(np.array(result))

            logger.info('\n %s' % str(np.array(results).mean(0)))


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

    # @unittest.skip('long running tests')
    def setUpData(self):
        return DataReader().read_analyze_solution('bc_averaging_disease_analysis#k=0')


class TestBiomassClass(MachineLearningTestCases.ClassificationTestCase):
    def setUpClf(self):
        return BiomassDiseaseClassifier()

    @unittest.skip('long running tests')
    def setUpData(self):
        X, y = DataReader().read_analyze_solution(
            'biomass_maximization_fba_results', gz=False)
        X = [{k + '_mas': v for k, v in x.items()} for x in X]
        return X, y


class TestParadigmClass(MachineLearningTestCases.ClassificationTestCase):
    def setUpClf(self):
        return ParadigmDiseaseClassifier()

    @unittest.skip('long running tests')
    def setUpData(self):
        X, y = DataReader().read_analyze_solution(
            'paradigm_results#k=10', gz=False)
        X = [{k + '_par': v for k, v in x.items()} for x in X]
        return X, y
