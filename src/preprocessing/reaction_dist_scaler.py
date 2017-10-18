from collections import defaultdict
from sklearn.base import TransformerMixin
from services import DataReader, average_by_label
import pandas as pd


class ReactionDiffScaler(TransformerMixin):
    """Scaler reaction by diff"""

    def __init__(self, dataset_name="recon2"):
        super().__init__()
        self.model = DataReader().read_network_model(dataset_name)

    def fit(self, X, y=None):
        self.healthy_flux = average_by_label(X, y, 'h')
        return self

    def transform(self, X, y=None):
        return [{
            '%s_dif' % reaction.id: self._reaction_flux_dis(reaction, x)
            for reaction in self.model.reactions
        } for x in X]

    def _reaction_flux_dis(self, reaction, x):
        f_score = lambda label: x[label] - self.healthy_flux[label]
        return sum(f_score('%s_%s' % (reaction.id, i)) for i in ['min', 'max'])
