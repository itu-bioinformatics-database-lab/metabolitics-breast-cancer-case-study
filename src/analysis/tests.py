import unittest

import cobra as cb
import cobra.test

from .base_subsystem_fba import BaseSubsystemFBA
from .fg_subsystem_fba import FGSubsystemFBA


class TestBaseFBA(unittest.TestCase):

    def setUp(self):
        model = cb.test.create_test_model('salmonella')
        self.analysis = BaseSubsystemFBA(model)

    def test_activate_subsystems(self):
        self.analysis.activate_subsystems(['GlycolysisGluconeogenesis'])
        glycogen_phosph = self.analysis._model.reactions.get_by_id('GLCP')
        self.assertEqual(glycogen_phosph.lower_bound, 0.1)
        self.assertEqual(glycogen_phosph.objective_coefficient, 1)


class TestFGSubsystemFBA(unittest.TestCase):

    def setUp(self):
        model = cb.test.create_test_model('salmonella')
        self.analysis = FGSubsystemFBA(model)
        self.measured_metabolites = {
            'h2o_p': 1
        }

    def test__initial_activation_heuristic(self):
        activate_subsystems = self.analysis._initial_activation_heuristic(
            self.measured_metabolites)
        self.assertEqual(len(activate_subsystems), 19)

    def test_analyze(self):
        solutions_subsystems = self.analysis.analyze(self.measured_metabolites)
