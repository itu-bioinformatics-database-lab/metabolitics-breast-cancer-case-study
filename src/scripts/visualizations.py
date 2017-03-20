from .cli import cli
from scripts import DataReader
from preprocessing import PathwayFvaDiffScaler
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from mlxtend.plotting import plot_decision_regions
import numpy as np
from sklearn.svm import LinearSVC, SVC


@cli.command()
def visualize_pathways_for_desease():
    X, y = DataReader().read_fva_solutions('fva.cameo.0.10.txt')
    X = PathwayFvaDiffScaler().fit_transform(X, y)
    vect = DictVectorizer(sparse=False)
    X = vect.fit_transform(X, y)
    # X = X[:, None]
    y = np.array([1 if i == 'bc' else 0 for i in y], dtype=int)
    clf = DecisionTreeClassifier(max_depth=1).fit(X, y)

    # clf = LinearSVC(C=0.01, random_state=43).fit(X, y)

    X = X + np.reshape(np.random.normal(1, 100, size=len(X)), X.shape)

    # ss = {'h': list(), 'bc': list()}
    # for i in ss:
    #     ss[i] = list(map(lambda x: list(x[0].values())[0],
    #                      filter(lambda s: s[1] == i, zip(X, y))))
    #
    # pp.plot(ss['h'], 'x')
    # pp.plot(ss['bc'], 'o')
    # pp.show()

    plot_decision_regions(X, y, clf=clf, res=0.5, legend=2)
    plt.xlabel(vect.feature_names_[0])
    plt.show()
