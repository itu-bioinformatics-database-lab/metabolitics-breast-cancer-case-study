from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from .base_disease_classifier import BaseDiseaseClassifier
from preprocessing import MostActivePathwayScaler


class SolutionLevelDiseaseClassifier(BaseDiseaseClassifier):

    def __init__(self):
        super().__init__()
        self._pipe = Pipeline([
            ('scaler_most_active', MostActivePathwayScaler()),
            ('vect', DictVectorizer(sparse=False)),
            ('pca', PCA()),
            ('clf', SVC(C=0.1, kernel='rbf', random_state=0))
        ])
