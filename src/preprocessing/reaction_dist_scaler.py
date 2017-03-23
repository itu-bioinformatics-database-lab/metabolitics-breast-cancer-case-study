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

    # def transform(self, X, y=None):
    #     return [{
    #         k:v for reaction in self.model.reactions
    #             for k, v in self._reaction_flux_dis(reaction, x).items()
    #         }
    #         for x in X
    #     ]


    def _reaction_flux_dis(self, reaction, x):
        r_min = x['%s_min' % reaction.id]
        r_max = x['%s_max' % reaction.id]

        hf_min = self.healthy_flux['%s_min' % reaction.id]
        hf_max = self.healthy_flux['%s_max' % reaction.id]

        max_diff = r_max - hf_max
        min_diff = r_min - hf_min

        return max_diff + min_diff


    def _reaction_flux_dis0(self, reaction, x):
        r_min = x['%s_min' % reaction.id]
        r_max = x['%s_max' % reaction.id]
        hf_min = self.healthy_flux['%s_min' % reaction.id]
        hf_max = self.healthy_flux['%s_max' % reaction.id]

        return {'%s_min' % reaction.id: r_min - hf_min, '%s_max' % reaction.id: r_max - hf_max}


    def _reaction_flux_dis1(self, reaction, x):
        r_min = x['%s_min' % reaction.id]
        r_max = x['%s_max' % reaction.id]
        hf_min = self.healthy_flux['%s_min' % reaction.id]
        hf_max = self.healthy_flux['%s_max' % reaction.id]

        if (hf_min, hf_max) == (r_min, r_max):
            return 0
        else:
            interval_len = max(hf_max, r_max) - min(hf_min, r_min)
            return 1000*(abs(hf_min - r_min) + abs(hf_max - r_max)) / interval_len


    def _reaction_flux_dis_1_1(self, reaction, x):
        r_min = x['%s_min' % reaction.id]
        r_max = x['%s_max' % reaction.id]
        hf_min = self.healthy_flux['%s_min' % reaction.id]
        hf_max = self.healthy_flux['%s_max' % reaction.id]

        if (hf_min, hf_max) == (r_min, r_max):
            return 1*1000

        overlap_length = min(hf_max, r_max) - max(hf_min, r_min)
        interval_len = max(hf_max, r_max) - min(hf_min, r_min)

        return 1000*overlap_length / interval_len
