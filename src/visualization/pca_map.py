from sklearn.decomposition import PCA
from sklearn.feature_extraction import DictVectorizer
import matplotlib.pyplot as plt


def pca_map(df):
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(df.T.values)

    pc1, pc2 = zip(*X_pca)

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.scatter(pc1, pc2)

    for i, txt in enumerate(df.columns):
        ax.annotate(txt, (pc1[i], pc2[i]))
