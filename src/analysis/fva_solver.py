from cobra.core import Model, DictList
from cobra.solvers import solver_dict
from cobra.flux_analysis.variability import calculate_lp_variability


class FVASolver:

    def __init__(self, model: Model, measured_metabolites):
        super().__init__()
        self._solver = solver_dict['cplex']
        self.measured_metabolites = measured_metabolites

    def create_fva_problem(self, fraction_of_optimum=1.0):
        """Runs flux variability analysis to find max/min flux values
        fraction_of_optimum : fraction of optimum which must be maintained.
            The original objective reaction is constrained to be greater than
            maximal_value * fraction_of_optimum
        """
        lp = self._solver.create_problem(self._model)
        self._solver.solve_problem(lp, objective_sense="maximize")
        solution = self._solver.format_solution(lp, self._model)
        if solution.status != "optimal":
            raise ValueError("FVA requires the solution status to be optimal, "
                             "not " + solution.status)
        # set all objective coefficients to 0
        for i, r in enumerate(self._model.reactions):
            if r.objective_coefficient != 0:
                f = solution.x_dict[r.id]
                new_bounds = (f * fraction_of_optimum, f)
                self._solver.change_variable_bounds(lp, i,
                                                    min(new_bounds),
                                                    max(new_bounds))
                self._solver.change_variable_objective(lp, i, 0.)
        self.lp_ = lp

    def solve(self, reactions=None):
        if reactions is None:
            reactions = self._model.reactions
        self.result_ = calculate_lp_variability(self.lp_, self._solver,
                                                self._model, reactions)
        return self.result_

    def analyze(self, filter_by_subsystem=False,
                increasing_metabolite_constraints=False):

        self.set_objective_coefficients(measured_metabolites)
        self.create_fva_problem()

        if increasing_metabolite_constraints:
            self.increasing_metabolite_constraints(self.measured_metabolites)

        reactions = None
        if filter_by_subsystem:
            reactions = self.filter_reaction_by_subsystems()

        return self.solve(reactions)

    def result_as_dataframe(self):
        pass

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
