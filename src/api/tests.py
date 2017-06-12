import unittest
import flask_testing

from .app import app
from .models import Analysis, db
from .tasks import save_analysis


class ApiTests(flask_testing.TestCase):
    pass


class TaskTests(unittest.TestCase):
    def test_save_analysis(self):
        # Warning: Do not use production db
        analysis = Analysis('test analysis', None)
        db.session.add(analysis)
        db.session.commit()
        analysis_id = analysis.id
        save_analysis(analysis.id, {'h_c': 1})

        q_anaylsis = Analysis.query.get(analysis_id)
        self.assertTrue(q_anaylsis)
        self.assertTrue(q_anaylsis.results_pathway)
        self.assertTrue(q_anaylsis.results_reaction)

        # db.session.delete(self.analysis)
        # db.session.commit()


class ModelsTests(flask_testing.TestCase):
    def setUp(self):
        self.reaction_result = [{'a_dif': 1, 'b_dif': 2}]
        self.pathway_result = [{'sa_dif': 1, 'sb_dif': 2}]
        self.analysis = Analysis('test analysis', None)

    def create_app(self):
        # Warning: Do not use production db
        app.config['TESTING'] = True
        return app

    @unittest.skip('Require db')
    def test_analysis(self):
        self.analysis.results_pathway = self.pathway_result
        self.analysis.results_reaction = self.reaction_result
        db.session.add(self.analysis)
        db.session.commit()

        q_anaylsis = Analysis.query.get(self.analysis.id)
        self.assertTrue(q_anaylsis)

        db.session.delete(self.analysis)
        db.session.commit()

    def test_clean_name_tag(self):
        cleaned = self.analysis.clean_name_tag(self.reaction_result)
        expected = [{'a': 1, 'b': 2}]
        self.assertEqual(list(cleaned), expected)
