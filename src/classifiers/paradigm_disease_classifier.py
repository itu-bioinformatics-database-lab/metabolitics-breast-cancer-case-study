from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

from .base_disease_classifier import BaseDiseaseClassifier
from preprocessing import DynamicPreprocessing


class ParadigmDiseaseClassifier(BaseDiseaseClassifier):
    def __init__(self):
        self._pipe = Pipeline([
            ('dy', DynamicPreprocessing([
                'feature-selection',
                'pathway-scoring',
            ])),
            ('vect', DictVectorizer(sparse=False)),
            ('pca', PCA(random_state=43)),
            ('clf', LogisticRegression(C=0.1, random_state=43)),
        ])
