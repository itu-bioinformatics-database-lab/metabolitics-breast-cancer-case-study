from joblib import Parallel, delayed
from sklearn.base import TransformerMixin

from analysis import BaseFVA


class FVAScaler(TransformerMixin):
    """Scaler for converting metabolic level data
        into fva reaction min max values"""

    def __init__(self, vectorizer, dataset_name="recon-model"):
        super().__init__()
        self.analyzer = BaseFVA.create_for(dataset_name)
        self.vectorizer = vectorizer

    def fit(self, X, y):
        return self

    def transform(self, X, y=[]):
        return Parallel(n_jobs=-1)(
            delayed(self._sample_transformation)(i)
            for i in self.vectorizer.inverse_transform(X)
        )

    def _sample_transformation(self, x):
        nex_x = dict()
        for k, v in self.analyzer.analyze(x).items():
            nex_x['%s_max' % k] = v['maximum']
            nex_x['%s_min' % k] = v['minimum']
        return nex_x

    def fit_transform(self, X, y):
        return self.fit(X, y).transform(X, y)
