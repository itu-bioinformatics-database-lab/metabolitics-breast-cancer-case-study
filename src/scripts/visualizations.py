import itertools

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import LinearSVC, SVC
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mlxtend.plotting import plot_decision_regions

from sklearn.linear_model import LogisticRegression
from .cli import cli
from scripts import DataReader
from preprocessing import PathwayFvaDiffScaler


@cli.command()
def visualize_pathways_for_desease():
    X, y = DataReader().read_fva_solutions('fva_without.transports.txt')
    X = PathwayFvaDiffScaler().fit_transform(X, y)
    vect = DictVectorizer(sparse=False)
    X = vect.fit_transform(X, y)
    # X = X[:, None]
    y = np.array([1 if i == 'bc' else 0 for i in y], dtype=int)
    # clf = LinearSVC(C=0.01, random_state=43).fit(X, y)
    if len(X) == 1:
        X = X + np.reshape(np.random.normal(1, 100, size=len(X)), X.shape)
        clf = DecisionTreeClassifier(max_depth=2).fit(X, y)
        plot_decision_regions(X, y, clf=clf, res=0.5, legend=2)
        plt.xlabel(vect.feature_names_[0])
    else:
        for fn in set(map(lambda x: x[:-4], vect.feature_names_)):
            try:
                x = X[:, (vect.feature_names_.index('%s_min' % fn),
                          vect.feature_names_.index('%s_max' % fn))]
            except:
                continue

            # clf = DecisionTreeClassifier(max_depth=1).fit(x, y)
            clf = LinearSVC(C=1e-4, random_state=43).fit(x, y)

            # clf = LogisticRegression(C=0.1e-1, random_state=43).fit(x, y)

            x = x + np.reshape(np.random.normal(1, 100,
                                                size=len(x) * 2), x.shape)
            plot_decision_regions(X=x, y=y, clf=clf, legend=2, res=10)
            plt.xlabel('%s_min' % fn)
            plt.ylabel('%s_max' % fn)
            plt.show()
