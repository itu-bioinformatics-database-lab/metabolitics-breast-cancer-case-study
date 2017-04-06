from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from .base_disease_classifier import BaseDiseaseClassifier


class PathifierDiseaseClassifier(BaseDiseaseClassifier):

    def __init__(self):
        super().__init__()
        self._pipe = Pipeline([
            ('vect', DictVectorizer(sparse=False)),
            ('scaler', StandardScaler()),
            ('pca', PCA()),
            ('clf', LogisticRegression(C=0.01, random_state=0))
        ])
