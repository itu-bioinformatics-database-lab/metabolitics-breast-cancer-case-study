from sklearn.svm import LinearSVC, SVC
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, VarianceThreshold
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from .base_disease_classifier import BaseDiseaseClassifier
from preprocessing import BorderSelector, PathwayFvaScaler, FVAScaler, \
    InverseDictVectorizer, MetabolicStandardScaler, ReactionDiffScaler, \
    TransportElimination


class FVADiseaseClassifier(BaseDiseaseClassifier):

    def __init__(self):
        super().__init__()
        vect1 = DictVectorizer(sparse=False)
        vect2 = DictVectorizer(sparse=False)
        vt = VarianceThreshold(0.1)
        skb = SelectKBest(k=50)
        self._pipe = Pipeline([
            # ('border-selector', BorderSelector()),
            ('flux-diff-scaler', ReactionDiffScaler()),
            ('vect1', vect1),
            ('vt', vt),
            ('inv_vec1', InverseDictVectorizer(vect1, vt)),
            ('vect2', vect2),
            ('skb', skb),
            ('inv_vec2', InverseDictVectorizer(vect2, skb)),
            ('pathway_scoring', PathwayFvaScaler()),
            ('vect3', DictVectorizer(sparse=False)),
            ('pca', PCA()),
            # ('clf', SVC(C=1e-6, kernel='rbf', random_state=0))
            # ('clf', KNeighborsClassifier(n_neighbors=31))
            # ('clf', DecisionTreeClassifier())
            # ('clf', RandomForestClassifier(n_estimators=10000, n_jobs=-1))
            # ('clf', LinearSVC(C=0.1e-5, random_state=43))
            ('clf', LogisticRegression(C=0.3e-6, random_state=43))
            # ('clf', MLPClassifier(activation="logistic",
            #                       random_state=43,
            #                       hidden_layer_sizes=(300, 100),
            #                       verbose=True,
            #                       #   alpha=1e-2,
            #                       max_iter=1000))
        ])
