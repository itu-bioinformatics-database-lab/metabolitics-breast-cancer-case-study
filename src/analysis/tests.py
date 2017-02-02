import unittest

import cobra as cb
import cobra.test

from .base_subsystem_fba import BaseSubsystemFBA
from .fg_subsystem_fba import FGSubsystemFBA
from .categorical_subsystem_fba import CategoricalSubsystemFBA
from .base_fva import BaseFVA
from models import *
from services import DataReader


class TestBaseSubsystemFBA(unittest.TestCase):

    def setUp(self):
        model = cb.test.create_test_model('salmonella')
        self.analysis = BaseSubsystemFBA(model)
        self.subsystems = ['GlycolysisGluconeogenesis']
        self.glycogen_phosph = self.analysis._model.reactions.get_by_id('GLCP')
        self.measured_metabolites = {'glycogen_c': 1}
        self.glycogen_c = self.analysis._model.metabolites.get_by_id(
            'glycogen_c')

    def test_activate_subsystems(self):
        self.analysis.activate_subsystems(self.subsystems)

        cdm_name = 'cdm_%s' % self.subsystems[0]
        cdm = self.analysis._model.metabolites.get_by_id(cdm_name)
        reactions_count = len([r for r in self.analysis._model.reactions
                               if r.subsystem == self.subsystems[0]])

        self.assertIsNotNone(cdm)
        self.assertEqual(reactions_count, len(cdm.reactions))

    def test_deactivate_subsystems(self):
        self.analysis.deactivate_subsystems(self.subsystems)
        self.assertEqual(self.glycogen_phosph.upper_bound, 0)
        self.assertEqual(self.glycogen_phosph.objective_coefficient, 0)

    def test__init_increasing_metabolites_constrains(self):
        self.analysis._init_inc_met_constrains(self.measured_metabolites)

        self.assertEqual(self.glycogen_c._constraint_sense, 'G')
        self.assertEqual(self.glycogen_c._bound, 1)

    def test__init_objective_coefficients(self):
        self.analysis._init_objective_coefficients(self.measured_metabolites)
        for r in self.glycogen_c.producers():
            self.assertNotEqual(r.objective_coefficient, 0)


class TestFGSubsystemFBA(unittest.TestCase):

    def setUp(self):
        self.model = cb.test.create_test_model('salmonella')
        self.analysis = FGSubsystemFBA(self.model)
        self.measured_metabolites = {'h2o_p': 1}

    def test__initial_activation_heuristic(self):
        activate_subsystems = self.analysis._initial_activation_heuristic(
            self.measured_metabolites)
        self.assertEqual(len(activate_subsystems), 19)

    def test_analyze(self):
        solutions_subsystems = self.analysis.analyze(self.measured_metabolites)
        act_subs = self.analysis._initial_activation_heuristic(
            self.measured_metabolites)
        solution = next(solutions_subsystems)
        self.assertTrue(solution >= act_subs)
        self.assertTrue(self.model.subsystems() >= solution)

    def test_possibilities(self):
        analysis = FGSubsystemFBA(self.model, 4)
        solutions = analysis.analyze(self.measured_metabolites)
        self.assertTrue(len(next(solutions)), 4)


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
