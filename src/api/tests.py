import unittest
from .models import Analysis, db
from .tasks import save_analysis


class ViewsTests(unittest.TestCase):
    pass


class TaskTests(unittest.TestCase):
    def test_save_analysis(self):
        analysis = Analysis('test analysis', None)
        db.session.add(analysis)
        db.session.commit()
        save_analysis(analysis.id, {'h_c': 1})


class ModelsTests(unittest.TestCase):
    def setUp(self):
        self.reaction_result = [{'a_dif': 1, 'b_dif': 2}]
        self.pathway_result = [{'sa_dif': 1, 'sb_dif': 2}]
        self.analysis = Analysis('test analysis', None)

    def test_clean_name_tag(self):
        cleaned = self.analysis.clean_name_tag(self.reaction_result)
        expected = [{'a': 1, 'b': 2}]
        self.assertEqual(list(cleaned), expected)

    def test_load_and_save_results(self):
        self.analysis.save_results(self.reaction_result, self.pathway_result)
        self.analysis.load_results()
        self.assertEqual(self.analysis.results['reaction'], [{'a': 1, 'b': 2}])
        self.assertEqual(self.analysis.results['pathway'], [{
            'sa': 1,
            'sb': 2
        }])
