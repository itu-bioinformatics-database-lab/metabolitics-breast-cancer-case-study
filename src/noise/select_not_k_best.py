import numpy as np

from sklearn.base import TransformerMixin
from sklearn.feature_selection import SelectKBest


class SelectNotKBest(TransformerMixin):
    """Select all feature except best K feature"""

    def __init__(self, **kwargs):
        self.kbest = SelectKBest(**kwargs)

    def fit(self, X, y):
        self.kbest.fit(X, y)
        return self

    def transform(self, X):
        """
        Transform to select not k best feature
        :param X: np.matrix
        """
        return X[:, self.get_support()]

    def get_support(self):
        return np.invert(self.kbest.get_support())
