from scipy.cluster.hierarchy import dendrogram as sci_dendrogram, linkage
from scipy.spatial.distance import pdist, squareform, cosine, correlation


def dendrogram(df, method='complete', metric='correlation'):
    linkage_matrix = linkage(pdist(df.T, metric), method, metric)
    return sci_dendrogram(linkage_matrix, labels=df.columns, orientation='left')
