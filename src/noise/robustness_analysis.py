import numpy.random as npr


class RobustnessAnalysis:
    def __init__(self, noise_generator, X):
        '''
        Robustness Analysis for scikit learn models
        :model: A scikit learn model which implements fit and predict methods 
        or a preprocessing step which implements fit and transform
        :X: dataset
        :y: labels
        :evaluation_metrics: metrics to evaluate noise added results. 
        For example, sklearn.metrics.accuracy_score 
        '''
        self._X = X
        self._generate = noise_generator
