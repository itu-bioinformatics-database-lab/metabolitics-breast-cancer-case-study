import numpy as np
import numpy.linalg as la
import scipy.spatial.distance as sci_dist
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
        noise = self._noise_func(*self._args, size=X.shape)
        results = X + noise
        self.relative_noise_size_ = self.relative_noise_size(X, results)
        return results

    def relative_noise_size(self, data, noise):
        '''
        :data: original data as numpy matrix
        :noise: noise matrix as numpy matrix
        '''
        return np.mean([
            sci_dist.cosine(u / la.norm(u), v / la.norm(v))
            for u, v in zip(noise, data)
        ])
