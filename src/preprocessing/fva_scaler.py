from joblib import Parallel, delayed
from sklearn.base import TransformerMixin
from analysis import BaseFVA


class FVAScaler(TransformerMixin):
    """Scaler for converting metabolic level data
        into fva reaction min max values"""

    def __init__(self, vectorizer=None, dataset_name="recon-model",
                 filter_by_subsystem=False):
        super().__init__()
        self.analyzer = BaseFVA.create_for(dataset_name)
        self.filter_by_subsystem = filter_by_subsystem
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
        analyzer = self.analyzer.copy()
        for r in analyzer.analyze(
            x, filter_by_subsystem=self.filter_by_subsystem) \
                .data_frame.itertuples():
            nex_x['%s_max' % r.Index] = r.upper_bound
            nex_x['%s_min' % r.Index] = r.lower_bound
        return nex_x

    def fit_transform(self, X, y):
        return self.fit(X, y).transform(X, y)
