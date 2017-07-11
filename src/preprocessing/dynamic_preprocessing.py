from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import SelectKBest, VarianceThreshold

from preprocessing import *
from .base_preprocessing_pipeline import BasePreprocessingPipeline


class DynamicPreprocessing(BasePreprocessingPipeline):

    all_steps = set([
        'naming', 'imputer', 'metabolic-standard', 'basic-fold-change-scaler',
        'fva', 'flux-diff', 'feature-selection', 'pathway-scoring',
        'transport-elimination'
    ])

    def __init__(self, steps=None):
        steps = steps or [
            'naming', 'metabolic-standard', 'fva', 'flux-diff',
            'feature-selection', 'pathway-scoring'
        ]
        steps = set(steps)
        super().__init__()
        pipe = list()
        if 'naming' in steps:
            pipe.append(('naming', NameMatching()))
        if 'imputer' in steps:
            vect = DictVectorizer(sparse=False)
            pipe.append(('vect-imputer', vect)),
            pipe.append(('imputer-mean', Imputer(0, 'mean')))
            pipe.append(('inv_vec-imputer', InverseDictVectorizer(vect)))
        if 'metabolic-standard' in steps:
            vect = DictVectorizer(sparse=False)
            pipe.append(('vect-standard', vect)),
            pipe.append(('metabolic-standard', MetabolicStandardScaler()))
            pipe.append(('inv_vec-standard', InverseDictVectorizer(vect)))
        if 'basic-fold-change-scaler' in steps:
            pipe.append(('basic_fold_change_scaler', BasicFoldChangeScaler()))
        if 'fva' in steps:
            vect = DictVectorizer(sparse=False)
            pipe.append(('vect-fva', vect))
            pipe.append(('fva', FVAScaler(vect)))
        if 'flux-diff' in steps:
            pipe.append(('flux-diff', ReactionDiffScaler()))
        if 'feature-selection' in steps:
            vect1 = DictVectorizer(sparse=False)
            vect2 = DictVectorizer(sparse=False)
            vt = VarianceThreshold(0.1)
            skb = SelectKBest(k=50)
            pipe.extend([
                ('vect-vt', vect1),
                ('vt', vt),
                ('inv_vec-vt', InverseDictVectorizer(vect1, vt)),
                ('vect-skb', vect2),
                ('skb', skb),
                ('inv_vec-skb', InverseDictVectorizer(vect2, skb)),
            ])
        if 'pathway-scoring' in steps:
            pipe.append(('pathway_scoring', PathwayFvaScaler()))
        if 'transport-elimination' in steps:
            pipe.append(('transport_elimination', TransportElimination()))
        if not self.all_steps >= steps:
            raise ValueError('steps %s do not exist DynamicPreprocessing' %
                             str(steps - self.all_steps))
        self._pipe = Pipeline(pipe)
