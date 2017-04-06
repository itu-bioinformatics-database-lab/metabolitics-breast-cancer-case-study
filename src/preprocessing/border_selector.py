from sklearn.base import TransformerMixin
from models import *
from services import DataReader


class BorderSelector(TransformerMixin):
    """Select border reaction from dataset"""

    def __init__(self):
        super().__init__()
        self.model = DataReader().read_network_model()

    def fit(self, X, y):
        return self

    def transform(self, X, y=[]):
        new_X = list()
        for x in X:
            new_x = dict()
            for m in self.model.metabolites:
                if m.is_border():
                    for r in m.reactions:
                        if '%s_max' % r.id in x:
                            new_x['%s_max' % r.id] = x['%s_max' % r.id]
                            new_x['%s_min' % r.id] = x['%s_min' % r.id]
            new_X.append(new_x)
        return new_X

    def fit_transform(self, X, y):
        return self.fit(X, y).transform(X, y)
