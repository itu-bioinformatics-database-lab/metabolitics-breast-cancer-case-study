import unittest
import numpy as np

from .select_not_k_best import SelectNotKBest


class SelectNotKBestTests(unittest.TestCase):
    def setUp(self):
        self.notk_best = SelectNotKBest(k=1)
        self.X = np.matrix([[1, 1, 3], [2, 2, 3], [2, 2, 3]])
        self.y = [1, 2, 2]

    def test_fit(self):
        self.notk_best.fit(self.X, self.y)

    def test_transform(self):
        self.test_fit()
        np.testing.assert_array_equal(
            self.notk_best.transform(self.X), self.X[:, 1:3])
