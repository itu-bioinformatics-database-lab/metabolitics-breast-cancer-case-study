import logging

from cameo import fba, flux_variability_analysis
from cobra.core import DictList

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
            results = flux_variability_analysis(
                self, reactions=reactions, fraction_of_optimum=1)
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
