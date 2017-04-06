from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from .base_preprocessing_pipeline import BasePreprocessingPipeline
from .metabolic_standard_scaler import MetabolicStandardScaler


class FormatedMeasurement(BasePreprocessingPipeline):

    def __init__(self):
        super().__init__()
        self._pipe = Pipeline([
            ('vect', DictVectorizer(sparse=False)),
            ('metabolic-standard-scaler', MetabolicStandardScaler()),
        ])

    def to_dict(self, X):
        return self._pipe.named_steps['vect'].inverse_transform(X)
