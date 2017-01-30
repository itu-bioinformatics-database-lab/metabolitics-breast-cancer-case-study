from sklearn.preprocessing import StandardScaler


class MetabolicStandardScaler(StandardScaler):
    """StandardScaler for using only by healthy metabolism in dataset."""

    def __init__(self):
        super().__init__(self)

    def filter_healthies(self, X, y):
        return zip(*filter(lambda t: t[1] == 'h', zip(X, y)))

    def partial_fit(self, X, y):
        """
        Parameters
        ----------
        X : {array-like, sparse matrix}, shape [n_samples, n_features]
            The data used to compute the mean and standard deviation
            used for later scaling along the features axis.
        y: Healthy 'h' or 'sick_name'
        """
        (X, y) = self.filter_healthies(X, y)
        super().partial_fit(X, y)
        return self
