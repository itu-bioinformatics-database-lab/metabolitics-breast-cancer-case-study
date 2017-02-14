import unittest
from .fva_solution_distance import *


class TestFVASolutionDistance(unittest.TestCase):

    def setUp(self):
        self.data = [{'a_min': -1, 'a_max': 1, 'b_min': -2, 'b_max': 2},
                     {'c_min': -5, 'c_max': 4}]

        self.data2 = [{'a_min': 0, 'a_max': 3, 'b_min': -1, 'b_max': 4},
                      {'c_min': 3, 'c_max': 5}]

    def test_diff_mix_max_fva_solution(self):
        self.assertEqual(diff_mix_max_fva_solution(self.data[0]), 6)

    def test_fva_solution_distance(self):
        self.assertEqual(fva_solution_distance(self.data), 7.5)

    def test__diff_range_solutions(self):
        diff_score = diff_range_solutions(self.data, self.data2)
        self.assertAlmostEqual(diff_score, -0.2375)
