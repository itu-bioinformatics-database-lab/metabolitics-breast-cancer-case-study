from functional import seq
from sklearn.base import TransformerMixin
from scipy.stats import fisher_exact
import cobra as cb

import models
from services import DataReader, average_by_label


class FunctionalEnrichmentAnalysis(TransformerMixin):
    """Functional Enrichment Analysis"""

    def __init__(self,
                 reference_label,
                 feature_groups,
                 method="fisher_exact",
                 alternative='two-sided',
                 filter_func=None):
        '''
        :reference_label: label of refence values in the calculation
        :method: only fisher exact test avaliable so far
        :feature_groups: list of dict where keys are new feature and values are set of old features
        '''
        if method != "fisher_exact":
            raise NotImplemented('Only fisher exact test is implemented')

        self.reference_label = reference_label
        self.feature_groups = feature_groups
        self.alternative = alternative
        self.filter_func = filter_func or (lambda x: round(x, 3) <= 0)

    def fit(self, X, y):
        self._references = average_by_label(X, y, self.reference_label)
        return self

    def transform(self, X):
        '''
        :X: list of dict
        :y: labels
        :filter_func: function return true or false
        '''
        X_t = list()
        for x in X:
            x_key_set = set(x.keys())
            X_t.append({
                new_feature: self._fisher_pval(x, old_features)
                for new_feature, old_features in self.feature_groups.items()
                if len(x_key_set & old_features)
            })
        return X_t

    def _filtered_values(self, x: dict, feature_set: list=None):
        '''
        :x: dict which contains feature names and values
        :return: pairs of values which shows number of feature makes filter function true or false
        '''
        feature_set = feature_set or x
        n = sum(self.filter_func(x[i]) for i in feature_set if i in x)
        return [len(feature_set) - n, n]

    def _contingency_table(self, x: dict, feature_set: list):
        return list(
            zip(*[
                self._filtered_values(xs, feature_set)
                for xs in [self._references, x]
            ]))

    def _fisher_pval(self, x: dict, feature_set: list):
        return fisher_exact(
            self._contingency_table(x, feature_set),
            alternative=self.alternative)[1]


class PathwayReactionEnrichment(FunctionalEnrichmentAnalysis):
    """Functional Enrichment Analysis"""

    def __init__(self, reference_label='h', dataset_name='recon2', **kwargs):
        '''
        :reference_label: label of refence values in the calculation
        :dataset_name: name of metabolitics network
        '''
        model = DataReader().read_network_model(dataset_name)

        feature_groups = seq(model.reactions) \
                         .map(lambda r: (r.subsystem, '%s_dif' % r.id)) \
                         .filter(lambda x: not cb.Model.is_transport_subsystem(x[0])) \
                         .group_by_key() \
                         .map(lambda x: (x[0], set(x[1]))) \
                         .to_dict()

        super().__init__(reference_label, feature_groups, **kwargs)
