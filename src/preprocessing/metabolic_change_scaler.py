from sklearn.base import TransformerMixin


class MetabolicChangeScaler(TransformerMixin):
    """Scaler for converting metabolic level data to change level"""

    def fit(self, X, y):
        '''Calculate average metabolite of healthy people'''
        (healthies, _) = zip(*filter(lambda xy: xy[1] == 'h', zip(X, y)))
        healthiesT = zip(*healthies)
        healthiesT_with_zero = [list(filter(lambda x: x != 0, i))
                                for i in healthiesT]
        self._avgs = [sum(i) / max(len(i), 1)
                      for i in healthiesT_with_zero]
        return self

    def transform(self, X, y=[]):
        '''0:no change  1:increase  -1:decrease'''
        for i in range(len(X)):
            for j in range(len(X[i])):
                if self._avgs[j] == X[i][j]:
                    X[i][j] = 0
                elif self._avgs[j] > X[i][j]:
                    X[i][j] = -1
                else:
                    X[i][j] = 1
        return list(X)

    def fit_transform(self, X, y):
        return self.fit(X, y).transform(X, y)
