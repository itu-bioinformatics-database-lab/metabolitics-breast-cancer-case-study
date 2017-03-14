from collections import defaultdict
from sklearn.base import TransformerMixin
from services import DataReader
import pandas as pd


class ReactionDiffScaler(TransformerMixin):
    """Scaler reaction by diff"""

    def __init__(self, dataset_name="recon2"):
        super().__init__()
        self.model = DataReader.read_network_model(dataset_name)

    def fit(self, X, y=None):
        self.healthy_flux = defaultdict(int, pd.DataFrame(
            list(map(lambda x: x[0],
                     filter(lambda t: t[1] == 'h', zip(X, y)))))
            .mean().to_dict())
        return self

    def transform(self, X, y=None):
        return [{
            '%s_dif' % reaction.id: self._reaction_flux_dis(reaction, x)
            for reaction in self.model.reactions}
            for x in X
        ]

    def _reaction_flux_dis(self, reaction, x):
        r_min = x['%s_min' % reaction.id]
        r_max = x['%s_max' % reaction.id]
        hf_min = self.healthy_flux['%s_min' % reaction.id]
        hf_max = self.healthy_flux['%s_max' % reaction.id]

        if (hf_min, hf_max) == (r_min, r_max):
            return 0
        else:
            interval_len = max(hf_max, r_max) - min(hf_min, r_min)
            return (abs(hf_min - r_min) + abs(hf_max - r_max)) / interval_len
