from sklearn.base import TransformerMixin


class TransportElimination(TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None, metrics='mean'):
        for x in X:
            keys = list(x.keys())
            for key in keys:
                if key.startswith('Transport'):
                    del x[key]
        return X
