from sklearn.preprocessing import StandardScaler
from services import filter_by_label


class MetabolicStandardScaler(StandardScaler):
    """StandardScaler for using only by healthy metabolism in dataset."""

    def __init__(self):
        super().__init__()

    def partial_fit(self, X, y):
        """
        Parameters
        ----------
        X : {array-like, sparse matrix}, shape [n_samples, n_features]
            The data used to compute the mean and standard deviation
            used for later scaling along the features axis.
        y: Healthy 'h' or 'sick_name'
        """
        (X, y) = filter_by_label(X, y, 'h')
        super().partial_fit(X, y)
        return self
