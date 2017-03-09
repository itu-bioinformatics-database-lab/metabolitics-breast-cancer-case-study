from collections import defaultdict
from sklearn.base import TransformerMixin
from services import DataReader


class PathwayFvaScaler(TransformerMixin):
    """Pathway level fva scaler"""

    def __init__(self, dataset_name="recon2"):
        super().__init__()
        self.model = DataReader.read_network_model(dataset_name)

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None, metrics='sum'):
        subsystem_scores = list()
        for x in X:
            sub_flux = defaultdict(int)
            sub_count = defaultdict(int)
            for reaction_id, flux in x.items():
                reaction = self.model.reactions.get_by_id(reaction_id[:-4])
                min_max = reaction_id[-3:]
                sub_flux['%s_%s' % (reaction.subsystem, min_max)] += flux
                sub_count['%s_%s' % (reaction.subsystem, min_max)] += 1
            if metrics == 'mean':
                subsystem_scores.append({
                    s: sub_flux[s] / sub_count[s] for s in sub_flux
                })
            elif metrics == 'sum':
                subsystem_scores.append({
                    s: sub_flux[s] / 1 for s in sub_flux
                })
        return subsystem_scores
