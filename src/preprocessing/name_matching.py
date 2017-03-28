from sklearn.base import TransformerMixin
from services import NamingService


class NameMatching(TransformerMixin):

    def __init__(self):
        super().__init__()
        self.naming = NamingService('recon')

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return self.naming.to(X)
