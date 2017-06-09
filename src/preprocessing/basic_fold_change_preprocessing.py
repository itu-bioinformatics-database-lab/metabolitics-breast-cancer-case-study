from sklearn.base import TransformerMixin
from services import average_by_label


class BasicFoldChangeScaler(TransformerMixin):
    '''
    Scales by measured value by distance to mean according to time of value
    '''

    def fit(self, X, y):
        self.avgs_ = average_by_label(X, y, 'h')
        return self

    def transform(self, X):
        return [{k: self.scale(k, v) for k, v in x.items()} for x in X]

    def scale(self, k, v):
        e = v / self.avgs_[k]
        return max(1 - e**-1, -100) if self.avgs_[k] > v else min(e - 1, 100)
