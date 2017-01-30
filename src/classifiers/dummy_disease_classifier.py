from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.dummy import DummyClassifier

from .base_disease_classifier import BaseDiseaseClassifier
from preprocessing import MostActivePathwayScaler


class DummyDiseaseClassifier(BaseDiseaseClassifier):

    def __init__(self):
        super().__init__()
        self._pipe = Pipeline([
            ('scaler_most_active', MostActivePathwayScaler()),
            ('vect', DictVectorizer(sparse=False)),
            ('pca', PCA()),
            ('clf', DummyClassifier(strategy="uniform"))
        ])
