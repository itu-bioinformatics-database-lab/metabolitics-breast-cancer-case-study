import unittest

import numpy as np
import numpy.testing as npt
import pandas as pd
from scipy.spatial.distance import euclidean

from .naming_service import NamingService
from .data_reader import DataReader
from .data_utils import *
from .data_writer import DataWriter


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

    def test_read_subsystem_categories(self):
        self.assertNotEqual(len(self.service.read_subsystem_categories()), 0)

    def test_read_hmdb_diseases(self):
        self.assertIsNotNone(self.service.read_hmdb_diseases())

    def test_read_healthy(self):
        X, y = self.service.read_healthy('BC')
        self.assertNotEqual(len(X), 0)
        self.assertNotEqual(len(y), 0)

    def test_read_hmdb_diseases(self):
        self.assertIsNotNone(self.service.read_escher_map('unicellular'))


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

        return npt.assert_almost_equal(
            similarty_dict(x, y, euclidean), [-0.4142136, -1.4494897])

    def test_variance_threshold_on_df(self):
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [1, 1, 1]})
        df_expected = pd.DataFrame({'a': [1, 2, 3]})
        return pd.testing.assert_frame_equal(
            variance_threshold_on_df(df), df_expected)

    def test_feature_importance_anova(self):
        X = [{
            'a': 1,
            'b': 2
        }, {
            'a': 1,
            'b': 2
        }, {
            'a': 2,
            'b': 2
        }, {
            'a': 2,
            'b': 2
        }]

        df = feature_importance_anova(X, self.y)
        self.assertListEqual(list(df.values[0]), [1, 2, np.inf, 0])

    def test_fisher_exact_test_for_pathway(self):
        X = [{
            'GLUDym_dif': -1,
            'GLUNm_dif': -1
        }, {
            'GLUDym_dif': 1,
            'GLUNm_dif': 2
        }]
        y = ['h', 'x']
        pvals = fisher_exact_test_for_pathway(X, y)

        import pdb
        pdb.set_trace()

        self.assertEqual(list(pvals.keys())[0], 'Glutamate metabolism')
        self.assertEqual(
            list(pvals.values())[0], (np.inf, 0.33333333333333343))


class TestDataWriter(unittest.TestCase):
    def setUp(self):
        self.X = [1] * 4
        self.y = ['bc', 'bc', 'h', 'h']

    def test_write_json(self):
        DataWriter('a', gz=True).write_json(self.X)
        DataWriter('a').write_json(self.X)
