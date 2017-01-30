from sklearn.base import TransformerMixin


class PathifierScaler(TransformerMixin):
    """Pathifier Scaler for converting metabolic level data to pathway level"""

    def __init__(self):
        super().__init__(self)

    def fit(self, X, y):
        return self
