from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from .base_disease_classifier import BaseDiseaseClassifier
from preprocessing import MetabolicStandardScaler, FVAScaler


class FVADiseaseClassifier(BaseDiseaseClassifier):

    def __init__(self):
        super().__init__()
        vect = DictVectorizer(sparse=False)
        self._pipe = Pipeline([
            ('vect', vect),
            ('metabolic-standard-scaler', MetabolicStandardScaler()),
            ('fva-scaler', FVAScaler(vect)),
            ('vect2', DictVectorizer(sparse=False)),
            ('pca', PCA()),
            ('clf', SVC(C=0.01, kernel='linear', random_state=0))
        ])
