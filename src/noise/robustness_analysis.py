import numpy.random as npr


class RobustnessAnalysis:
    def __init__(self, model, X, y, noise_generator):
        '''
        Robustness Analysis for scikit learn models
        :model: A scikit learn model which implements fit and predict methods 
        or a preprocessing step which implements fit and transform
        :X: dataset
        :y: labels
        :random_generator: a function which generator noise  
        '''
        self.model = model
        self.X = X
        self.y = y
