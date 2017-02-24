import unittest

import cobra as cb
import cobra.test
from sklearn.feature_extraction import DictVectorizer

from models import *
from services import DataReader

from .base_solver import BaseSolver
from .fva_solver import FVASolver


class TestBaseSolver(unittest.TestCase):

    def setUp(self):
        model = cb.test.create_test_model('salmonella')
        self.model = BaseSolver(model)
        self.oxi_phos = 'Oxidative Phosphorylation'
        self.h2o2_p = self.model._model.metabolites.get_by_id('h2o2_p')
        self.r_12DGR120tipp = self.model._model.reactions.get_by_id(
            '12DGR120tipp')

    def test_get_pathway(self):
        pathway = self.model.get_pathway('Transport Inner Membrane')
        self.assertTrue(self.r_12DGR120tipp in pathway)

    @unittest.skip('not migrated')
    def test_activate_pathway(self):
        self.model.activate_pathway(self.oxi_phos)
        solution = self.model.solve()
        sum_flux = sum(solution.x_dict[r.id] for r in self.oxi_phos.reactions)
        self.assertTrue(sum_flux >= 0)

    def test_knock_out_pathway(self):
        self.model.knock_out_pathway(self.oxi_phos)
        solution = self.model.solve()
        reactions = self.model.get_pathway(self.oxi_phos)
        sum_flux = sum(solution.x_dict[r.id] for r in reactions)
        self.assertTrue(sum_flux == 0)

    @unittest.skip('not migrated')
    def test_increasing_metabolite_constraint(self):
        pass

    def test_set_objective_coefficients(self):
        self.model.set_objective_coefficients({'h2o2_p': 1})
        for r in self.h2o2_p.producers():
            self.assertNotEqual(r.objective_coefficient, 0)

    def test_create_for(self):
        recon = BaseSolver.create_for()
        self.assertIsNotNone(recon)


class TestFVASolver(unittest.TestCase):

    def setUp(self):
        self.analyzer = FVASolver.create_for('e_coli_core')

    def test_analyze(self):
        measured_metabolites = {'etoh_e': 1, 'gln__L_c': 1}
        result = self.analyzer.analyze(measured_metabolites)
        self.assertIsNotNone(result['EX_fum_e']['minimum'])
        self.assertIsNotNone(result['EX_fum_e']['maximum'])

    def test_filter_reaction_by_subsystems(self):
        reactions = self.analyzer.filter_reaction_by_subsystems()
        self.assertTrue(len(self.analyzer._model.reactions) > len(reactions))
        num_systems = set(r.subsystem for r in self.analyzer._model.reactions)
        self.assertTrue(len(num_systems) * 3 >= len(reactions))

    @unittest.skip('for prestored solution')
    def test_dataset_compatibility(self):
        (s, y) = DataReader().read_fva_solutions()
        (s6, y) = DataReader().read_fva_solutions('fva_solutions6.txt')
        for i in range(len(s)):
            # a = 0
            # for k, _ in s[i].items():
            #     if abs(s[i][k] - s6[i][k]) > 1e-6:
            #         # print(k, s[i][k], s6[i][k])
            #         a += 1
            # print(a)
            self.assertAlmostEqual(s[i][k], s6[i][k])


class TestConstraint(unittest.TestCase):

    def setUp(self):
        self.model = BaseFVA.create_for()

    @unittest.skip('not migrated')
    def test_increasing_metabolite_constraint(self):
        measured_metabolites = {'inost_r': 1}
        reactions = self.model.increasing_metabolite_constraints(
            measured_metabolites)

        df = self.model.fba(measured_metabolites)

        flux_sum = sum([1 for r in reactions if df[r.id] >= 10**-3 - 10**-6])

        self.assertTrue(flux_sum >= 1)

    @unittest.skip('not migrated')
    def test_indicator_constraints_integrated(self):
        self.model = BaseFVA.create_for('example')
        measured_metabolites = {'ACP_c': 1}
        reactions = self.model.increasing_metabolite_constraints(
            measured_metabolites)
        df = self.model.fba(measured_metabolites)

        flux_sum = sum([1 for r in reactions if df[r.id] >= 10**-3 - 10**-6])

        self.assertTrue(flux_sum >= 1)

        # print(self.model.solver)
    @unittest.skip('not migrated')
    def test_indicator_constraints_synthetic(self):
        model = DataReader().create_example_model()
        smodel = SolverBasedModel(description=model)

        lb = 1
        metabolite = model.metabolites.get_by_id('ACP_c')

        indicator_vars = []
        for r in metabolite.producers():
            var = smodel.solver.interface.Variable(
                "var_%s" % r.id, type="binary")

            # When the indicator is 1, constraint is enforced)
            c = smodel.solver.interface.Constraint(
                r.flux_expression,
                lb=lb,
                indicator_variable=var,
                active_when=1)

            smodel.solver.add(c)
            indicator_vars.append(var)

        expr = sum(indicator_vars)
        c = smodel.solver.interface.Constraint(
            expr, lb=1, ub=len(indicator_vars))
        smodel.solver.add(c)

        df = fba(smodel)

        flux_sum = sum(df[r.id] >= 1 - 10**-6 for r in metabolite.producers())

        self.assertTrue(flux_sum >= 1)

        # print(self.model.solver)
