import unittest

import cobra as cb
import cobra.test
from sklearn.feature_extraction import DictVectorizer

from .base_pathway_model import BasePathwayModel
from .fg_subsystem_fba import FGSubsystemFBA
from .categorical_subsystem_fba import CategoricalSubsystemFBA
from .base_fva import BaseFVA
from models import *
from services import DataReader, NamingService
from preprocessing import MetabolicStandardScaler


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
        self.model.knock_out_pathway(self.oxi_phos)
        solution = self.model.solve()
        sum_flux = sum(solution.x_dict[r.id] for r in self.oxi_phos.reactions)
        self.assertTrue(sum_flux == 0)

    def test_increasing_metabolite_constrain(self):
        self.model.increasing_metabolite_constrain(self.h2o2_p)
        self.model.solve()
        sum_flux = sum(r.forward_variable.primal + r.reverse_variable.primal
                       for r in self.h2o2_p.reactions)
        self.assertTrue(sum_flux >= 2)

    def test_set_objective_coefficients(self):
        self.model.set_objective_coefficients({'h2o2_p': 1})
        for r in self.h2o2_p.producers():
            self.assertNotEqual(r.objective_coefficient, 0)

    def test_create_for(self):
        recon = BasePathwayModel.create_for()
        self.assertIsNotNone(recon)


class TestFGSubsystemFBA(unittest.TestCase):

    def setUp(self):
        model = DataReader().read_network_model('e_coli_core')
        self.model = FGSubsystemFBA(model)
        self.measured_metabolites = {'h2o_c': 1}
        import pdb; pdb.set_trace()


    def test__initial_activation_heuristic(self):
        activate_subsystems = self.model \
            ._initial_activation_heuristic(self.measured_metabolites)
        self.assertEqual(len(activate_subsystems), 8)
        self.assertEqual(self.model.solve().status, 'optimal')

    def test_analyze(self):
        solutions_subsystems = self.model.analyze(self.measured_metabolites)
        act_subs = self.model \
            ._initial_activation_heuristic(self.measured_metabolites)
        solution = next(solutions_subsystems)
        self.assertTrue(solution >= act_subs)
        self.assertTrue(self.model.subsystems() >= solution)

    def test_possibilities(self):
        analysis = FGSubsystemFBA(self.model, 4)
        solutions = analysis.analyze(self.measured_metabolites)
        self.assertTrue(len(next(solutions)), 4)

    def test_constrains(self):
        (X, y) = DataReader().read_all()
        vect = DictVectorizer(sparse=False)
        X = vect.fit_transform(X, y)
        X = MetabolicStandardScaler().fit_transform(X, y)
        X = vect.inverse_transform(X)
        X = NamingService('recon').to(X)

        for x in X[:10]:
            analysis = FGSubsystemFBA.create_for()
            analysis.increasing_metabolite_constrains(x)
            analysis.set_objective_coefficients(x)
            self.assertEqual(analysis.solve().status, 'optimal')


class TestCategoricalSubsystemFBA(unittest.TestCase):

    def setUp(self):
        self.analyzer = CategoricalSubsystemFBA.create_for()
        self.category = 'energy-metabolism'
        self.measured_metabolites = {'accoa_c': 1, 'focytC_m': 1}
        self.subsystems = set(['Oxidative phosphorylation'])

    def test_analyze_category(self):

        init_active = set()
        solution = self.analyzer.analyze_category(self.category, init_active)
        self.assertIsNotNone(list(solution))

        solution = self.analyzer.analyze_category(
            self.category, self.subsystems)
        self.assertEqual(list(solution), [self.subsystems])

    def test_analyze(self):
        solutions = self.analyzer.analyze(self.measured_metabolites)
        self.assertEqual(list(solutions[self.category]), [self.subsystems])


class TestBaseFVA(unittest.TestCase):

    def setUp(self):
        self.analyzer = BaseFVA.create_for('e_coli_core')

    def test_analyze(self):
        measured_metabolites = {'etoh_e': 1, 'gln__L_c': 1}
        reactions_range = self.analyzer.analyze(measured_metabolites)
        self.assertIsNotNone(reactions_range['EX_fum_e']['minimum'])
        self.assertIsNotNone(reactions_range['EX_fum_e']['maximum'])
