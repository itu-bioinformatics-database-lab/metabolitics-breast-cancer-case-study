from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from preprocessing import MetabolicStandardScaler, FVAScaler, \
    ReactionDiffScaler
from .base_preprocessing_pipeline import BasePreprocessingPipeline


class FVARangedMeasurement(BasePreprocessingPipeline):

    def __init__(self):
        super().__init__()
        vect = DictVectorizer(sparse=False)
        self._pipe = Pipeline([
            ('vect', vect),
            ('metabolic-standard-scaler', MetabolicStandardScaler()),
            ('fva-scaler', FVAScaler(vect)),
            ('flux-diff-scaler', ReactionDiffScaler())
        ])
