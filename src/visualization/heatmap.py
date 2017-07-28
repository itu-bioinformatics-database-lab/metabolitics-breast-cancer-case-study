import numpy as np
import pandas as pd

from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist, squareform

import plotly.plotly as py
from plotly.graph_objs import *
from plotly import figure_factory as ff
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go


class HeatmapVisualization:
    def __init__(self, X, y, method='complete', metric='cosine'):
        self.X = X
        self.y = y
        self.linkage_func = lambda x: linkage(x, method, metric)

    def _map_to_data_array(self):
        df = pd.DataFrame().from_records(self.X)
        return df.fillna(0).values, self.y, np.array(df.keys())

    def clustered_data(self):
        data_array, labels, pathways = self._map_to_data_array()

        dx = ff.create_dendrogram(
            data_array, orientation='bottom', linkagefun=self.linkage_func)

        dy = ff.create_dendrogram(
            data_array.T, orientation='right', linkagefun=self.linkage_func)

        x_dendro_leaves = list(map(int, dx['layout']['xaxis']['ticktext']))
        y_dendro_leaves = list(map(int, dy['layout']['yaxis']['ticktext']))

        heat_data = data_array.T
        heat_data = heat_data[y_dendro_leaves, :]
        heat_data = heat_data[:, x_dendro_leaves]

        hx = np.array(
            list(map(lambda x: '%s_%d' % x, zip(labels, range(len(labels))))))[
                x_dendro_leaves]
        hy = pathways[y_dendro_leaves]

        return {'x': hx.tolist(), 'y': hy.tolist(), 'z': heat_data.tolist()}

    def iplot_heatmap(self):
        init_notebook_mode(connected=True)
        
        layout = go.Layout(autosize=True,
            margin=go.Margin(l=250, r=15, b=75, t=15, pad=10))

        heatmap = Heatmap(**self.clustered_data())
        fig = go.Figure(data=[heatmap], layout=layout)
        iplot(fig, filename='heatmap_subject_pathway.html')
