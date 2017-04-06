from sklearn.base import TransformerMixin

import numpy as np
import pandas as pd


class InverseDictVectorizer(TransformerMixin):
    """Pathway level fva scaler"""

    def __init__(self, dict_vectorizer, feature_selector=None):
        self.dict_vectorizer = dict_vectorizer
        self.feature_selector = feature_selector

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if self.feature_selector:
            names = np.array(self.dict_vectorizer.feature_names_)[
                self.feature_selector.get_support()]
            return list(pd.DataFrame(X, columns=names).T.to_dict().values())
        return self.dict_vectorizer.inverse_transform(X)
