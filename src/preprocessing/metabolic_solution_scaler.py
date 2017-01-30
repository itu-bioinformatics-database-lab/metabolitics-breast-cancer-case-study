
from sklearn.base import TransformerMixin
from sklearn.feature_extraction import DictVectorizer

from services import NamingService, DataReader
from analysis import FGSubsystemFBA


class MetabolicSolutionScaler(TransformerMixin):
    """Scaler for converting change level data to pathway level"""

    def __init__(self, vectorizer: DictVectorizer):
        self.vectorizer = vectorizer
        self.naming = NamingService('recon')
        self.analyzer = FGSubsystemFBA(
            DataReader.read_network_model('recon-model'))

    def fit(self, X, y):
        return self

    def transform(self, X, y=[]):
        human_X = self.naming.to(X)
        # FIXME: no solution service
        solutions = self.solution_service.get_solutions(human_X)
        return solutions

    def fit_transform(self, X, y):
        return self.fit(X, y).transform(X, y)
