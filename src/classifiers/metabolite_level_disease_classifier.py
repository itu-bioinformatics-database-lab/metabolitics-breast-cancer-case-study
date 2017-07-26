from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from .base_disease_classifier import BaseDiseaseClassifier
from preprocessing import MetabolicStandardScaler, NameMatching


class MetaboliteLevelDiseaseClassifier(BaseDiseaseClassifier):
    def __init__(self):
        super().__init__()
        self._pipe = Pipeline([
            # Metabolite level classification
            ('naming', NameMatching()),
            ('vect', DictVectorizer(sparse=False)),
            ('scaler', MetabolicStandardScaler()),
            ('pca', PCA(random_state=43)),
            ('clf', LogisticRegression(C=0.01, random_state=43))
        ])
