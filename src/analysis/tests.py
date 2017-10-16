import unittest

import cobra as cb
import cobra.test
from sklearn.feature_extraction import DictVectorizer

from .base_pathway_model import BasePathwayModel
from .base_fva import BaseFVA
from models import *
from services import DataReader, NamingService
from preprocessing import MetabolicStandardScaler
from cobra.core import Model, Reaction
from cameo.core import SolverBasedModel, Metabolite
from cameo.core.solution import Solution
from cameo.flux_analysis import fba
import optlang


class TestBasePathwayModel(unittest.TestCase):
    def setUp(self):
        model = cb.test.create_test_model('salmonella')
        self.model = BasePathwayModel(description=model)
        self.oxi_phos = self.model.get_pathway('Oxidative Phosphorylation')
        self.h2o2_p = self.model.metabolites.get_by_id('h2o2_p')

    def test_get_pathway(self):
        pathway = self.model.get_pathway('Transport Inner Membrane')
        r_12DGR120tipp = self.model.reactions.get_by_id('12DGR120tipp')
        self.assertTrue(r_12DGR120tipp in pathway.reactions)

    def test_activate_pathway(self):
        self.model.activate_pathway(self.oxi_phos)
        solution = self.model.solve()
        sum_flux = sum(solution.x_dict[r.id] for r in self.oxi_phos.reactions)
        self.assertTrue(sum_flux >= 0)

    def test_deactivate_pathway(self):
        self.model.make_pathway_inactive(self.oxi_phos)
        solution = self.model.solve()
        sum_flux = sum(solution.x_dict[r.id] for r in self.oxi_phos.reactions)
        self.assertEqual(sum_flux, 0)

    def test_set_objective_coefficients(self):
        self.model.set_objective_coefficients(
            {
                'h2o2_p': 1
            }, without_transports=False)
        for r in self.h2o2_p.producers():
            self.assertNotEqual(r.objective_coefficient, 0.0)

    def test_create_for(self):
        recon = BasePathwayModel.create_for()
        self.assertIsNotNone(recon)


class TestBaseFVA(unittest.TestCase):
    def setUp(self):
        self.analyzer = BaseFVA.create_for('e_coli_core')

    def test_analyze_base_on_example_two(self):
        analyzer = BaseFVA.create_for('example2')
        measured_metabolites = {'M2': 1, 'M3': 1}
        df = analyzer.analyze(
            measured_metabolites, without_transports=False).data_frame
        print(df)
        self.assertIsNotNone(df)

    def test_analyze(self):
        measured_metabolites = {'fru_e': '1.1'}

        df = self.analyzer.analyze(measured_metabolites).data_frame
        self.assertIsNotNone(df.loc['EX_fum_e'].upper_bound)
        self.assertIsNotNone(df.loc['EX_fum_e'].lower_bound)

    def test_filter_reaction_by_subsystems(self):
        reactions = self.analyzer.filter_reaction_by_subsystems()
        self.assertTrue(len(self.analyzer.reactions) > len(reactions))
        num_systems = set(r.subsystem for r in self.analyzer.reactions)
        self.assertTrue(len(num_systems) * 3 >= len(reactions))
