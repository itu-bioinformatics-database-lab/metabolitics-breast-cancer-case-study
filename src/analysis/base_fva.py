import logging
from collections import OrderedDict

import pandas
from cobra.core import DictList
from cameo import fba, flux_variability_analysis

from .base_pathway_model import BasePathwayModel


class BaseFVA(BasePathwayModel):
    def analyze(self,
                measured_metabolites,
                filter_by_subsystem=False,
                add_constraints=False,
                without_transports=True):

        if add_constraints:
            self.increasing_metabolite_constraints(measured_metabolites)

        self.set_objective_coefficients(measured_metabolites,
                                        without_transports)

        reactions = None
        if filter_by_subsystem:
            reactions = self.filter_reaction_by_subsystems()

        self.solver.configuration.timeout = 10 * 60

        try:
            results = self._fva_averaging()
        except:
            logging.getLogger('timeout_errors').error('FVA timeout error')
            logging.getLogger('timeout_errors').error(self.solver.to_json())
            raise TimeoutError('FVA timeout error')

        return results

    def fba(self,
            measured_metabolites,
            filter_by_subsystem=False,
            add_constraints=False):
        if add_constraints:
            self.increasing_metabolite_constrains(measured_metabolites)

        if measured_metabolites is not None:
            self.set_objective_coefficients(measured_metabolites)

        reactions = None
        if filter_by_subsystem:
            reactions = self.filter_reaction_by_subsystems()

        return fba(self, reactions=reactions)

    def filter_reaction_by_subsystems(self):
        subsystem2reactions = {}
        for reaction in self.reactions:
            subsystem2reactions.setdefault(reaction.subsystem, [])
            subsystem2reactions[reaction.subsystem].append(reaction)

        fva_reactions = DictList()
        for subsys, reactions in subsystem2reactions.items():
            reactions = sorted(reactions,
                               key=lambda x: sum(
                                   [len([r for r in m.reactions if r != x])
                                    for m in x.metabolites]), reverse=True)
            for i in range(3):
                if i == len(reactions):
                    break
                fva_reactions.append(reactions[i])
        return fva_reactions

    def _fva_averaging(self):
        fva_sol = OrderedDict()
        lb_flags = dict()

        self.fix_objective_as_constraint(fraction=1)
        self.clean_objective()

        for r in self.reactions:
            lb_flags[r.id] = False
            fva_sol[r.id] = dict()
            fva_sol[r.id]['average_bound'] = 0

        self.objective.direction = 'min'
        for reaction in self.reactions:
            self.solver.objective.set_linear_coefficients({
                reaction.forward_variable:
                1.,
                reaction.reverse_variable:
                -1.
            })
            try:
                solution = self.solve()
                fva_sol[reaction.id]['lower_bound'] = solution.f
            except Unbounded:
                fva_sol[reaction.id]['lower_bound'] = -numpy.inf
            except Infeasible:
                lb_flags[reaction.id] = True

            for r in self.reactions:
                if r != reaction:
                    fva_sol[r.id]['average_bound'] += solution.fluxes[r.id]

            self.solver.objective.set_linear_coefficients({
                reaction.forward_variable:
                0.,
                reaction.reverse_variable:
                0.
            })

            assert self.objective.expression == 0, self.objective.expression

        self.objective.direction = 'max'
        for reaction in self.reactions:
            ub_flag = False
            self.solver.objective.set_linear_coefficients({
                reaction.forward_variable:
                1.,
                reaction.reverse_variable:
                -1.
            })

            try:
                solution = self.solve()
                fva_sol[reaction.id]['upper_bound'] = solution.f
            except Unbounded:
                fva_sol[reaction.id]['upper_bound'] = numpy.inf
            except Infeasible:
                ub_flag = True

            for r in self.reactions:
                if r != reaction:
                    fva_sol[r.id]['average_bound'] += solution.fluxes[r.id]

            if lb_flags[reaction.id] is True and ub_flag is True:
                fva_sol[reaction.id]['lower_bound'] = 0
                fva_sol[reaction.id]['upper_bound'] = 0
                [lb_flags[reaction.id], ub_flag] = [False, False]
            elif lb_flags[reaction.id] is True and ub_flag is False:
                fva_sol[reaction.id]['lower_bound'] = fva_sol[reaction.id][
                    'upper_bound']
                lb_flags[reaction.id] = False
            elif lb_flags[reaction.id] is False and ub_flag is True:
                fva_sol[reaction.id]['upper_bound'] = fva_sol[reaction.id][
                    'lower_bound']
                ub_flag = False

            self.solver.objective.set_linear_coefficients({
                reaction.forward_variable:
                0.,
                reaction.reverse_variable:
                0.
            })

            assert self.objective.expression == 0, self.objective.expression

            assert lb_flags[reaction.
                            id] is False and ub_flag is False, "Something is wrong with FVA (%s)" % reaction.id

        df = pandas.DataFrame.from_dict(fva_sol, orient='index')
        lb_higher_ub = df[df.lower_bound > df.upper_bound]

        # this is an alternative solution to what I did above with flags
        # Assert that these cases really only numerical artifacts
        assert ((lb_higher_ub.lower_bound - lb_higher_ub.upper_bound) <
                1e-6).all()
        df.lower_bound[lb_higher_ub.index] = df.upper_bound[lb_higher_ub.index]

        df.average_bound = df.average_bound / 2 / (len(self.reactions) - 1)

        return df
