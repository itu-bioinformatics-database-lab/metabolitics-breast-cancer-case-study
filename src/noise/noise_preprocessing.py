import numpy.random as npr
from sklearn.base import TransformerMixin


class NoiseGenerator(TransformerMixin):
    '''
    Add noise to dataset
    '''

    def __init__(self, noise_func, noise_func_args):
        '''
        Add noise to data
        :noise_func: a function which generator noise with same shape with data
        :noise_func_args: arguments of noise function
        '''
        self._noise_func = noise_func
        self._args = noise_func_args

    def fit(self, X, y):
        return self

    def transform(self, X):
        '''
        :X: numpy ndarray 
        '''
        return self._noise_func(*self._args, size=X.shape)
