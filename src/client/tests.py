import unittest
from .metabolitics_api import MetaboliticsApiClient


class TestMetaboliticsApiClient:
    def setUp(self):
        self.client = MetaboliticsApiClient()

    def test_login(self):
        pass

    def test_analyze(self, name, concentration_changes):
        pass

    def test_get_analysis(self, id):
        pass
