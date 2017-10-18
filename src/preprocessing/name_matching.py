from sklearn.base import TransformerMixin
from services import NamingService


class NameMatching(TransformerMixin):
    def __init__(self, naming='recon'):
        super().__init__()
        self.naming = NamingService(naming)

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return self.naming.to(X)
