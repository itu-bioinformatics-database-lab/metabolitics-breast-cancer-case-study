import unittest

from .naming_service import NamingService
from .data_reader import DataReader


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
