import unittest
import numpy as np

from .select_not_k_best import SelectNotKBest
from .noise_preprocessing import NoiseGenerator


class SelectNotKBestTests(unittest.TestCase):
    def setUp(self):
        self.notk_best = SelectNotKBest(k=1)
        self.X = np.matrix([[1, 1, 10], [2, 2, 20], [2, 2, 30]])
        self.y = [1, 2, 2]

    def test_fit(self):
        self.notk_best.fit(self.X, self.y)

    def test_transform(self):
        self.test_fit()
        np.testing.assert_array_equal(
            self.notk_best.transform(self.X), self.X[:, 1:3])


class NoiseGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.noise_gen = NoiseGenerator(np.random.uniform, (0.1, -0.1))
        self.ones = np.ones((3, 3))

    def test_relative_noise_size(self):
        ns = self.noise_gen.relative_noise_size(self.ones, self.ones)
        self.assertEqual(ns, 1)

    def test_fit_transform(self):
        t_X = self.noise_gen.fit_transform(self.ones, [1, 1, 1])
        self.assertGreater(1, self.noise_gen.relative_noise_size_)

        self.assertTrue(np.all(self.ones * 1.11 > t_X))
        self.assertTrue(np.all(self.ones * 0.89 < t_X))
