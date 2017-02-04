from sklearn.svm import LinearSVC, SVC
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from .base_disease_classifier import BaseDiseaseClassifier


class FVADiseaseClassifier(BaseDiseaseClassifier):

    def __init__(self):
        super().__init__()
        self._pipe = Pipeline([
            ('vect2', DictVectorizer(sparse=False)),
            ('pca', PCA()),
            # ('clf', SVC(C=10, kernel='poly', random_state=0))
            # ('clf', KNeighborsClassifier(n_neighbors=7))
            # ('clf', LinearSVC(C=0.00000001, ))
            ('clf', MLPClassifier(activation="logistic",
                                  random_state=0,
                                  hidden_layer_sizes=(300, 100),
                                  verbose=True,
                                  #   alpha=1e-2,
                                  max_iter=1000))
        ])
