from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from .base_disease_classifier import BaseDiseaseClassifier
from preprocessing import MetabolicStandardScaler


class MetaboliteLevelDiseaseClassifier(BaseDiseaseClassifier):

    def __init__(self):
        super().__init__()
        self._pipe = Pipeline([
            ('vect', DictVectorizer(sparse=False)),
            ('scaler', MetabolicStandardScaler()),
            ('pca', PCA()),
            ('clf', SVC(C=0.01, kernel='linear', random_state=0))
        ])
