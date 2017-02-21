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
        self.model.knock_out_pathway(self.oxi_phos)
        solution = self.model.solve()
        sum_flux = sum(solution.x_dict[r.id] for r in self.oxi_phos.reactions)
        self.assertTrue(sum_flux == 0)

    def test_increasing_metabolite_constrain(self):
        self.model.increasing_metabolite_constrain(self.h2o2_p)
        self.model.solve()
        sum_flux = sum(r.forward_variable.primal + r.reverse_variable.primal
                       for r in self.h2o2_p.reactions)
        self.assertTrue(sum_flux >= 0)

    def test_set_objective_coefficients(self):
        self.model.set_objective_coefficients({'h2o2_p': 1})
        for r in self.h2o2_p.producers():
            self.assertNotEqual(r.objective_coefficient, 0)

    def test_create_for(self):
        recon = BasePathwayModel.create_for()
        self.assertIsNotNone(recon)


class TestBaseFVA(unittest.TestCase):

    def setUp(self):
        self.analyzer = BaseFVA.create_for('e_coli_core')

    def test_analyze(self):
        measured_metabolites = {'etoh_e': 1, 'gln__L_c': 1}
        df = self.analyzer.analyze(measured_metabolites).data_frame
        self.assertIsNotNone(df.loc['EX_fum_e'].upper_bound)
        self.assertIsNotNone(df.loc['EX_fum_e'].lower_bound)

    def test_filter_reaction_by_subsystems(self):
        reactions = self.analyzer.filter_reaction_by_subsystems()
        self.assertTrue(len(self.analyzer.reactions) > len(reactions))
        num_systems = set(r.subsystem for r in self.analyzer.reactions)
        self.assertTrue(len(num_systems) * 3 >= len(reactions))

<<<<<<< HEAD
    def test_dataset_compatibility(self):
        (s, y) = DataReader().read_fva_solutions()
        (s6, y) = DataReader().read_fva_solutions('fva_solutions6.txt')
        for i in range(len(s)):
            a = 0
            for k, _ in s[i].items():
                if abs(s[i][k] - s6[i][k]) > 1e-6:
                    # print(k, s[i][k], s6[i][k])
                    a += 1
            print(a)
            # self.assertAlmostEqual(s[i][k], s6[i][k])
=======
class TestConstraint(unittest.TestCase):

    def setUp(self):
        self.model = BaseFVA.create_for()

    def test_increasing_metabolite_constraint(self):
        measured_metabolites = {'inost_r':1}
        reactions = self.model.increasing_metabolite_constraints(measured_metabolites)

        df = self.model.fba(measured_metabolites)

        flux_sum = sum([1 for r in reactions if df[r.id] >= 10**-3 - 10**-6])

        self.assertTrue(flux_sum >= 1)

    def test_indicator_constraints_integrated(self):
        self.model = BaseFVA.create_for('example')
        measured_metabolites = {'ACP_c':1}
        reactions = self.model.increasing_metabolite_constraints(measured_metabolites)
        df = self.model.fba(measured_metabolites)

        flux_sum = sum([1 for r in reactions if df[r.id] >= 10**-3 - 10**-6])

        self.assertTrue(flux_sum >= 1)

        #print(self.model.solver)

    def test_indicator_constraints_synthetic(self):
        model = Model('example_model')

        r1 = Reaction('R1')
        r1.name = 'R1'
        r1.lower_bound = 0.
        r1.upper_bound = 1000.
        r1.objective_coefficient = 0.

        r2 = Reaction('R2')
        r2.name = 'R2'
        r2.lower_bound = 0.
        r2.upper_bound = 1000.
        r2.objective_coefficient = 0.

        r3 = Reaction('R3')
        r3.name = 'R3'
        r3.lower_bound = 0
        r3.upper_bound = 1000
        r3.objective_coefficient = 0

        ACP_c = Metabolite(
            'ACP_c',
            formula='C11H21N2O7PRS',
            name='acyl-carrier-protein',
            compartment='c')

        r1.add_metabolites({ACP_c: 1.0})
        r2.add_metabolites({ACP_c: 1.0})
        r3.add_metabolites({ACP_c: -1.0})

        model.add_reactions([r1, r2, r3])
        smodel = SolverBasedModel(description=model)

        lb = 1
        metabolite = ACP_c

        indicator_vars = []
        for r in metabolite.producers():
            var = smodel.solver.interface.Variable("var_%s" % r.id, type="binary")
            c = smodel.solver.interface.Constraint(r.flux_expression, lb=lb, indicator_variable=var,
                                                   active_when=1)  # When the indicator is 1, constraint is enforced)
            smodel.solver.add(c)
            indicator_vars.append(var)

        expr = sum(indicator_vars)
        c = smodel.solver.interface.Constraint(expr, lb=1, ub=len(indicator_vars))
        smodel.solver.add(c)

        df = fba(smodel)

        flux_sum = sum([1 for r in metabolite.producers() if df[r.id] >= 1 - 10**-6])

        self.assertTrue(flux_sum >= 1)

        #print(self.model.solver)
>>>>>>> cc050d78f922ab3e7b71d6d98c72842430bb48a3
