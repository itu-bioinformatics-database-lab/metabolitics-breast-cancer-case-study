import unittest
from collections import defaultdict

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import VarianceThreshold

from .metabolic_standard_scaler import MetabolicStandardScaler
from .fva_scaler import FVAScaler
from services import DataReader, NamingService
from .fva_ranged_mesearument import FVARangedMeasurement
from .border_selector import BorderSelector
from .pathway_fva_scaler import PathwayFvaScaler
from .reaction_dist_scaler import ReactionDiffScaler
from .inverse_dict_vectorizer import InverseDictVectorizer
from .transport_elimination import TransportElimination
from .name_matching import NameMatching
from .dynamic_preprocessing import DynamicPreprocessing
from .basic_fold_change_preprocessing import BasicFoldChangeScaler


class TestMetabolicStandardScaler(unittest.TestCase):
    def setUp(self):
        self.scaler = MetabolicStandardScaler()
        self.X = [[10], [10], [10], [0], [0], [0]]
        self.y = ['bc', 'bc', 'bc', 'h', 'h', 'h']

    def test_partial_fit(self):
        self.scaler.partial_fit(self.X, self.y)
        expected_X = self.X
        transformed_X = self.scaler.transform(self.X, self.y).tolist()
        self.assertEqual(expected_X, transformed_X)


def assert_min_max_defined(self, X):
    self.assertIsNotNone(X['MDH_max'])
    self.assertIsNotNone(X['MDH_min'])


class TestFVAScaler(unittest.TestCase):
    def setUp(self):
        (X, y) = DataReader().read_all()
        X = NamingService('recon').to(X)
        self.vect = DictVectorizer(sparse=False)
        X = self.vect.fit_transform(X, y)
        X = MetabolicStandardScaler().fit_transform(X, y)
        self.measured_metabolites = X[0]
        self.scaler = FVAScaler(self.vect)

    @unittest.skip("long running test")
    def test_transform(self):
        X = self.scaler.transform([self.measured_metabolites])
        assert_min_max_defined(self, X[0])

    @unittest.skip("long running test")
    def test__sample_transformation(self):
        X = self.vect.inverse_transform([self.measured_metabolites])
        X = self.scaler._sample_transformation(X[0])
        assert_min_max_defined(self, X)


class TestFVARangedMeasurement(unittest.TestCase):
    def setUp(self):
        (X, y) = DataReader().read_data('BC')
        X = NamingService('recon').to(X)

        Xy = next(filter(lambda k: k[1] == 'h', zip(X, y)))
        (self.X, self.y) = ([Xy[0]], [Xy[1]])
        self.fva = FVARangedMeasurement()

    @unittest.skip("long running test")
    def test_fit_transform(self):
        X = self.fva.fit_transform(self.X, self.y)
        assert_min_max_defined(self, X[0])


class TestBorderSelector(unittest.TestCase):
    def setUp(self):
        self.selector = BorderSelector()
        self.data = [{
            'TAXOLte_max': 1,
            'TAXOLte_min': -1,
            'AM1CCSitr_max': 1,
            'AM1CCSitr_min': -1
        }]

    def test_fit_transform(self):
        transformed_data = self.selector.fit_transform(self.data, [])
        self.assertEqual(transformed_data[0],
                         {'TAXOLte_max': 1,
                          'TAXOLte_min': -1})


class TestPathwayFvaScaler(unittest.TestCase):
    def setUp(self):
        self.scaler = PathwayFvaScaler()
        self.data = [{
            'TAXOLte_max': 1,
            'TAXOLte_min': -1,
            'MAL_Lte_max': 5,
            'MAL_Lte_min': -4
        }]

    def test_fit_transform(self):
        sub_scores = self.scaler.fit_transform(self.data)
        self.assertTrue(sub_scores, [{
            'Transport, extracellular_min': -2.5,
            'Transport, extracellular_max': 3,
        }])


class TestReactionDiffScaler(unittest.TestCase):
    def setUp(self):
        self.scaler = ReactionDiffScaler()
        self.h = defaultdict(int, {'TAXOLte_max': 1, 'TAXOLte_min': -1})
        self.X = [
            self.h, defaultdict(int, {'TAXOLte_max': 2,
                                      'TAXOLte_min': 1})
        ]
        self.y = ['h', 'bc']

    def test_fit(self):
        self.scaler.fit(self.X, self.y)
        self.assertEqual(self.scaler.healthy_flux, self.h)

    def test_fit_transform(self):
        sub_scores = self.scaler.fit_transform(self.X, self.y)
        self.assertTrue(sub_scores, [{'TAXOLte_dif': 0}, {'TAXOLte_dif': 1}])


class TestInverseDictVectorizer(unittest.TestCase):
    def setUp(self):
        self.data = [{
            'a': 0,
            'b': 2,
            'c': 0,
            'd': 3
        }, {
            'a': 0,
            'b': 1,
            'c': 4,
            'd': 3
        }]
        self.vect = DictVectorizer(sparse=False)
        self.trans_data = self.vect.fit_transform(self.data)

    def test_fit_transform(self):
        scaler = InverseDictVectorizer(self.vect)
        expected_data = [{'b': 2, 'd': 3}, {'b': 1, 'd': 3, 'c': 4}]
        self.assertEqual(expected_data, scaler.transform(self.trans_data))

    def test_fit_transform_with_feature_selection(self):
        vt = VarianceThreshold()
        data = vt.fit_transform(self.trans_data)
        scaler = InverseDictVectorizer(self.vect, vt)
        expected_data = [{'b': 2, 'c': 0}, {'b': 1, 'c': 4}]
        self.assertEqual(expected_data, scaler.fit_transform(data))


class TestTransportElimination(unittest.TestCase):
    def setUp(self):
        self.data = [{
            'Transport, a': 0,
            'b': 2,
            '_dif': 1
        }, {
            'a': 0,
            'Transport, b': 1
        }]
        self.tranformer = TransportElimination()

    def test_transform(self):
        expected = [{'b': 2}, {'a': 0}]
        calculated = self.tranformer.transform(self.data)
        self.assertEqual(calculated, expected)


class TestNameMatching(unittest.TestCase):
    def setUp(self):
        self.service = NameMatching()

    def test_transform(self):
        self.service.naming._names = {'x': 'y'}
        self.assertEqual(self.service.transform({'x': 1}), {'y': 1})


class TestDynamaicPreprocessing(unittest.TestCase):
    def test_init(self):
        transformer = DynamicPreprocessing()
        self.assertEqual(len(transformer._pipe.steps), 14)

        transformer = DynamicPreprocessing(['metabolic-standard'])
        self.assertEqual(len(transformer._pipe.steps), 3)

        transformer = DynamicPreprocessing(['transport-elimination'])
        self.assertEqual(len(transformer._pipe.steps), 1)

        transformer = DynamicPreprocessing(transformer.all_steps)
        self.assertTrue(
            len(transformer._pipe.steps) > len(transformer.all_steps))

    def test_raise_nonexistent_item_error(self):
        with self.assertRaises(ValueError) as value_error:
            tranformer = DynamicPreprocessing(['no-name'])


class TestBasicFoldChangeScaler(unittest.TestCase):
    def setUp(self):
        self.X = [{'a': 2.5, 'b': 5, 'c': 10}, {'a': 20, 'b': 40, 'c': 80}]
        self.h = {'a': 10, 'b': 10, 'c': 10}
        self.X.append(self.h)
        self.y = ['b', 'b', 'h']
        self.scaler = BasicFoldChangeScaler()

    def test_fit(self):
        self.scaler.fit(self.X, self.y)
        self.assertEqual(self.scaler._avgs, self.h)

    def test_transform(self):
        X = self.scaler.fit_transform(self.X, self.y)
        expected_X = [{
            'a': -3,
            'b': -1,
            'c': 0
        }, {
            'a': 1,
            'b': 3,
            'c': 7
        }, {
            'a': 0,
            'b': 0,
            'c': 0
        }]
        self.assertEqual(X, expected_X)

    def test_scale(self):
        self.scaler._avgs = {'a': 10**-6}
        self.assertEqual(self.scaler._scale('a', 10**6), 10)

        self.scaler._avgs = {'a': 2}
        self.assertEqual(self.scaler._scale('a', 8), 3)

        self.scaler._avgs = {'a': 10**6}
        self.assertEqual(self.scaler._scale('a', 10**-6), -10)
