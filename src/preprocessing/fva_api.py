from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from preprocessing import FVAScaler,     ReactionDiffScaler
from .base_preprocessing_pipeline import BasePreprocessingPipeline


class FVAApi(BasePreprocessingPipeline):

    def __init__(self):
        super().__init__()
        vect = DictVectorizer(sparse=False)
        self._pipe = Pipeline([
            ('vect', vect),
            ('fva-scaler', FVAScaler(vect)),
            ('flux-diff-scaler', ReactionDiffScaler())
        ])
