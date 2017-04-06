from sklearn.metrics import classification_report
from sklearn.base import BaseEstimator


class BaseDiseaseClassifier(BaseEstimator):

    def __init__(self):
        self._model = object()

    def fit(self, X, y):
        '''
        Fits model
        '''
        self._model = self._pipe.fit(X, y)

    def score(self, X, y):
        '''
        Score of model
        '''
        return self._model.score(X, y)

    def predict(self, X):
        '''
        Predicts star for given review and return star
        review: Review object
        '''
        return self._model.predict(X)

    def classification_report(self, X, y):
        '''
        '''
        return classification_report(y, self._model.predict(X))

    def __str__(self):
        return str(self._pipe)
