import unittest

import cobra as cb
import cobra.test

from .base_subsystem_fba import BaseSubsystemFBA
from .fg_subsystem_fba import FGSubsystemFBA
from models import *


class TestBaseSubsystemFBA(unittest.TestCase):

    def setUp(self):
        model = cb.test.create_test_model('salmonella')
        self.analysis = BaseSubsystemFBA(model)
        self.subsystems = ['GlycolysisGluconeogenesis']
        self.glycogen_phosph = self.analysis._model.reactions.get_by_id('GLCP')

    def test_activate_subsystems(self):
        self.analysis.activate_subsystems(self.subsystems)

        cdm_name = 'cdm_%s' % self.subsystems[0]
        cdm = self.analysis._model.metabolites.get_by_id(cdm_name)
        reactions_count = len([r for r in self.analysis._model.reactions
                               if r.subsystem == self.subsystems[0]])

        self.assertIsNotNone(cdm)
        self.assertEqual(reactions_count, len(cdm.reactions))
        self.assertEqual(self.glycogen_phosph.objective_coefficient, 1)

    def test_deactivate_subsystems(self):
        self.analysis.deactivate_subsystems(self.subsystems)
        self.assertEqual(self.glycogen_phosph.upper_bound, 0)
        self.assertEqual(self.glycogen_phosph.objective_coefficient, 0)


class TestFGSubsystemFBA(unittest.TestCase):

    def setUp(self):
        self.model = cb.test.create_test_model('salmonella')
        self.analysis = FGSubsystemFBA(self.model)
        self.measured_metabolites = {
            'h2o_p': 1
        }

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
