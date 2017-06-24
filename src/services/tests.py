import unittest

import numpy.testing as npt

from .naming_service import NamingService
from .data_reader import DataReader
from .data_utils import *


class TestNamingService(unittest.TestCase):
    def setUp(self):
        self.service = NamingService('recon')

    def test_to(self):
        self.assertNotEqual(len(self.service._names), 0)

        self.service._names = {'x': 'y'}
        self.assertEqual(self.service.to('x'), 'y')
        self.assertEqual(self.service.to('a'), None)

        named = self.service.to({'x': 1, 'c': 1})
        self.assertDictEqual(named, {'y': 1})


class TestDataReader(unittest.TestCase):
    def setUp(self):
        self.service = DataReader()

    def test_solution_reader(self):
        self.assertNotEqual(len(self.service.read_solutions()), 0)

    def test_read_subsystem_categories(self):
        self.assertNotEqual(len(self.service.read_subsystem_categories()), 0)

    def test_read_fva_solutions(self):
        (X, y) = self.service.read_fva_solutions()
        self.assertNotEqual(len(X), 0)
        self.assertNotEqual(len(y), 0)

    def test_read_hmdb_diseases(self):
        self.assertIsNotNone(self.service.read_hmdb_diseases())

    def test_read_healthy(self):
        X, y = self.service.read_healthy('BC')
        self.assertNotEqual(len(X), 0)
        self.assertNotEqual(len(y), 0)


class TestDataUtils(unittest.TestCase):
    def setUp(self):
        self.y = ['bc', 'bc', 'h', 'h']

    def test_filter_by_label(self):
        X, y = filter_by_label(range(4), self.y, 'h')
        self.assertEqual(X, (2, 3))
        self.assertEqual(y, ('h', 'h'))

    def test_average_by_label(self):
        Xi = [{
            'a': 1,
            'b': 2
        }, {
            'a': 2,
            'b': 3
        }, {
            'a': 4,
            'b': 5
        }, {
            'a': 6,
            'b': 7
        }]
        X = average_by_label(Xi, self.y, 'h')
        self.assertEqual(X, {'a': 5, 'b': 6})

    def test_similarty_dict(self):
        x = {'a': 1, 'b': 2}
        y = [{'b': 2, 'a': 2, 'c': 1}, {'b': 0, 'a': 2, 'd': 1}]
        return npt.assert_almost_equal(similarty_dict(x, y), [0.1055728, 0.6])
