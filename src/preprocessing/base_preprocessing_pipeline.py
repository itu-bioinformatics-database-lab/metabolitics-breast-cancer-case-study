class BasePreprocessingPipeline(object):
    def __init__(self):
        self._model = object()

    def fit(self, X, y):
        '''
        Fits model
        '''
        self._model = self._pipe.fit(X, y)
        return self

    def transform(self, X):
        '''
        Transform model
        '''
        return self._pipe.transform(X)

    def fit_transform(self, X, y):
        '''
        Fit and transform model
        '''
        return self._pipe.fit_transform(X, y)

    def __str__(self):
        return str(self._model)
