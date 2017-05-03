import unittest
from .models import Analysis, db
from .tasks import save_analysis


class ApiTests(unittest.TestCase):
    pass


class TaskTests(unittest.TestCase):
    def test_save_analysis(self):
        analysis = Analysis('test analysis', None)
        db.session.add(analysis)
        db.session.commit()
        save_analysis(analysis.id, {'h_c': 1})
