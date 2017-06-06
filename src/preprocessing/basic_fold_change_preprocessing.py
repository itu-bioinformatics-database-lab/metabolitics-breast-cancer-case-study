from sklearn.base import TransformerMixin
from services import average_by_label


class BasicFoldChangeScaler(TransformerMixin):
    '''
    Scales by measured value by distance to mean according to time of value
    Thus scale is [inf, 1] and (-1, -inf)
    '''

    def fit(self, X, y):
        self.avgs_ = average_by_label(X, y, 'h')
        return self

    def transform(self, X):
        return [{
            k: -self.avgs_[k] / v if self.avgs_[k] > v else v / self.avgs_[k]
            for k, v in x.items()
        } for x in X]
