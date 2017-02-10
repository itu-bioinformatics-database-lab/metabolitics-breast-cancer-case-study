import unittest

from sklearn.feature_extraction import DictVectorizer

from .metabolic_standard_scaler import MetabolicStandardScaler
from .metabolic_change_scaler import MetabolicChangeScaler
from .most_active_pathway_scaler import MostActivePathwayScaler
from .fva_scaler import FVAScaler
from services import DataReader, NamingService
from .fva_ranged_mesearument import FVARangedMeasurement
from .border_selector import BorderSelector


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


class TestMetabolicChangeScaler(unittest.TestCase):

    def setUp(self):
        self.scaler = MetabolicChangeScaler()
        self.X = [[10, -1,  3, 12],
                  [-1, 10,  2,  1],
                  [1,   1, -1,  3],
                  [1,   1,  3,  5],
                  [1,   1,  3,  0]]

        self.y = ['bc', 'bc', 'bc', 'h', 'h']

    def test_fit(self):
        expected_avgs = [1, 1, 3, 5]
        transformed_avgs = self.scaler.fit(self.X, self.y)._avgs
        self.assertListEqual(expected_avgs, transformed_avgs)

    def test_transform(self):
        expected_X = [[1, -1,  0,  1],
                      [-1, 1, -1, -1],
                      [0,  0, -1, -1],
                      [0,  0,  0,  0],
                      [0,  0,  0, -1]]
        self.scaler.fit(self.X, self.y)
        transformed_X = self.scaler.transform(self.X, self.y)
        self.assertListEqual(self.y, ['bc', 'bc', 'bc', 'h', 'h'])
        self.assertListEqual(expected_X, transformed_X)


class TestMetabolicSolutionScaler(unittest.TestCase):

    def setUp(self):
        self.data = [{'acon_C_c': 1}, ]
        self.vict = DictVectorizer(sparse=False)
        self.vict.fit(self.data)
        self.scaler = MetabolicSolutionScaler(self.vict)


class TestMostActivePathwayScaler(unittest.TestCase):

    def setUp(self):
        self.scaler = MostActivePathwayScaler()

    def test_transform(self):
        solutions = [{
            's1': ['a', 'b', 'c', 'd'],
            's2': ['b', 'c', 'd'],
            's3': ['b', 'c'],
            's4': ['a', 'c', 'd']
        }]

        scores = self.scaler.transform(solutions)
        expected_scores = [{'a': 2, 'b': 3, 'c': 4, 'd': 3}]
        self.assertEqual(expected_scores, scores)


def assert_min_max_defined(self, X):
    self.assertIsNotNone(X['MDH_max'])
    self.assertIsNotNone(X['MDH_min'])


class TestFVAScaler(unittest.TestCase):

    def setUp(self):
        (X, y) = DataReader().read_all()
        X = NamingService('recon').to(X)
        self.vect = DictVectorizer(sparse=False)
        X = self.vect.fit_transform(X, y)
        X = MetabolicChangeScaler().fit_transform(X, y)
        self.measured_metabolites = X[0]
        self.scaler = FVAScaler(self.vect)

    def test_transform(self):
        X = self.scaler.transform([self.measured_metabolites])
        assert_min_max_defined(self, X[0])

    def test__sample_transformation(self):
        X = self.vect.inverse_transform([self.measured_metabolites])
        X = self.scaler._sample_transformation(X[0])
        assert_min_max_defined(self, X)


class TestFVARangedMeasurement(unittest.TestCase):

    def setUp(self):
        (X, self.y) = DataReader().read_all()
        self.X = NamingService('recon').to(X)
        self.fva = FVARangedMeasurement()

    def test_fit_transform(self):
        X = self.fva.fit_transform([self.X[0]], [self.y[0]])
        assert_min_max_defined(self, X[0])


class TestBorderSelector(unittest.TestCase):

    def setUp(self):
        self.selector = BorderSelector()
        self.data = [{'TAXOLte_max': 1, 'TAXOLte_min': -1,
                      'AM1CCSitr_max': 1, 'AM1CCSitr_min': -1}]

    def test_fit_transform(self):
        transformed_data = self.selector.fit_transform(self.data, [])
        self.assertEqual(transformed_data[0], {
                         'TAXOLte_max': 1, 'TAXOLte_min': -1})
