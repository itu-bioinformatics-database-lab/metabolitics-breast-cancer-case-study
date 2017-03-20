from sklearn.feature_selection import SelectKBest, VarianceThreshold
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from .base_preprocessing_pipeline import BasePreprocessingPipeline
from preprocessing import PathwayFvaScaler, InverseDictVectorizer


class PathwayFvaDiffScaler(BasePreprocessingPipeline):
    """Pathway level fva scaler"""

    def __init__(self):
        super().__init__()
        vect1 = DictVectorizer(sparse=False)
        vect2 = DictVectorizer(sparse=False)
        vt = VarianceThreshold(0.1)
        skb = SelectKBest(k=10)
        self._pipe = Pipeline([
            ('vect1', vect1),
            ('vt', vt),
            ('inv_vec1', InverseDictVectorizer(vect1, vt)),
            ('vect2', vect2),
            ('skb', skb),
            ('inv_vec2', InverseDictVectorizer(vect2, skb)),
            ('pathway_scoring', PathwayFvaScaler())
        ])
