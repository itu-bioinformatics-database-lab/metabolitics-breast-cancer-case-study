from collections import Counter

from sklearn.base import TransformerMixin


class MostActivePathwayScaler(TransformerMixin):
    """Scaler for converting change level data to pathway level"""

    def fit(self, X, y):
        return self

    def transform(self, X, y=[]):
        return self._pathway_activation_score(X)

    def fit_transform(self, X, y):
        return self.fit(X, y).transform(X, y)

    def _pathway_activation_score(self, solutions):
        ''' Score subsystems by how many time it is repated in solutions '''
        return [dict(Counter([x for i in s.values() for x in i]))
                for s in solutions]
