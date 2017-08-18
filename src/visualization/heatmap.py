import numpy as np
import pandas as pd

from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist, squareform

import plotly.plotly as py
from plotly.graph_objs import *
from plotly import figure_factory as ff
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import VarianceThreshold

from preprocessing import *


class HeatmapVisualization:
    def __init__(self, X, y, method='complete', metric='cosine'):
        self.X = X
        self.y = y
        self.linkage_func = lambda x: linkage(x, method, metric)

    def _map_to_data_array(self):
        df = pd.DataFrame().from_records(self.eliminate_low_variance())
        return df.fillna(0).values, self.y, np.array(df.keys())

    def eliminate_low_variance(self):
        vect = DictVectorizer(sparse=False)
        vt = VarianceThreshold(100)

        pipe = Pipeline([
            ('vect', vect),
            ('vt', vt),
            ('inv_vec', InverseDictVectorizer(vect, vt)),
        ])

        return pipe.fit_transform(self.X)

    def clustered_data(self):
        data_array, labels, pathways = self._map_to_data_array()

        dx = ff.create_dendrogram(
            data_array, orientation='bottom', linkagefun=self.linkage_func)

        dy = ff.create_dendrogram(
            data_array.T, orientation='right', linkagefun=self.linkage_func)

        x_leaves = list(map(int, dx['layout']['xaxis']['ticktext']))
        y_leaves = list(map(int, dy['layout']['yaxis']['ticktext']))

        heat_data = data_array.T
        heat_data = heat_data[y_leaves, :]
        heat_data = heat_data[:, x_leaves]

        hx = np.array(['%s_%d' % i[::-1] for i in enumerate(labels)])[x_leaves]

        hy = pathways[y_leaves]

        return {'x': hx.tolist(), 'y': hy.tolist(), 'z': heat_data.tolist()}

    def iplot_heatmap(self):
        init_notebook_mode(connected=True)

        layout = go.Layout(
            autosize=True, margin=go.Margin(l=250, r=15, b=75, t=15, pad=10))

        heatmap = Heatmap(**self.clustered_data())
        fig = go.Figure(data=[heatmap], layout=layout)
        iplot(fig, filename='heatmap_subject_pathway.html')
