from sklearn.base import TransformerMixin
from services import average_by_label


class BasicFoldChangeScaler(TransformerMixin):
    '''
    Scales by measured value by distance to mean according to time of value
    '''

    def fit(self, X, y):
        self._avgs = average_by_label(self._round(X), y, 'h')
        return self

    def transform(self, X):
        return [{k: self._scale(k, v)
                 for k, v in x.items()} for x in self._round(X)]

    def _scale(self, k, v):
        e = v / self._avgs[k]
        return max(1 - e**-1, -10) if self._avgs[k] > v else min(e - 1, 10)

    def _round(self, X):
        for x in X:
            for k, v in x.items():
                x[k] = round(v, 3)
        return X
