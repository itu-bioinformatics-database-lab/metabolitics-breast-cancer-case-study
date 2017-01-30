from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from .base_disease_classifier import BaseDiseaseClassifier
from preprocessing import MetabolicChangeScaler, MetabolicSolutionScaler
from preprocessing import MetabolicStandardScaler, MostActivePathwayScaler


class SolutionLevelDiseaseClassifier(BaseDiseaseClassifier):

    def __init__(self):
        super().__init__()
        vectorizer = DictVectorizer(sparse=False)
        self._pipe = Pipeline([
            ('vect', vectorizer),
            ('scaler', MetabolicStandardScaler()),
            ('scaler_change', MetabolicChangeScaler()),
            ('scaler_solution', MetabolicSolutionScaler(vectorizer)),
            ('scaler_most_active', MostActivePathwayScaler())
            ('vect2', DictVectorizer(sparse=False)),
            ('pca', PCA()),
            ('clf', SVC(C=0.01, kernel='linear', random_state=0))
        ])
