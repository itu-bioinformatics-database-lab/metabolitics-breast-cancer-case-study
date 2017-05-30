from sklearn.base import TransformerMixin


class TransportElimination(TransformerMixin):

    black_list = ['Transport', 'Exchange', '_']

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for x in X:
            keys = list(x.keys())
            for key in keys:
                for b in self.black_list:
                    if key.startswith(b):
                        del x[key]
        return X
