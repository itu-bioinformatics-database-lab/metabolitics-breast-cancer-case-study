from typing import List

from cameo.core import SolverBasedModel, Metabolite
from cameo.core.pathway import Pathway
from sympy.core.singleton import S

from services import DataReader


class BasePathwayModel(SolverBasedModel):
    '''
    This is base model for subsystem level analysis.
    It adds subsystem level constraints to analysis type
    '''

    @classmethod
    def create_for(cls, dataset_name="recon-model"):
        model = DataReader().read_network_model(dataset_name)
        self = cls(description=model)
        return self

    def get_pathway(self, name: str):
        '''
        Gets pathway for given pathway name
        '''
        return Pathway([r for r in self.reactions if r.subsystem == name])

    def activate_pathway(self, pathway):
        '''
        Active subsystem means that
        S is active subsystem where
        r is set of reaction
        r_x \in S
        \sum_{i=1}^{n} V_{r_i} >= 0
        '''
        p = self.get_pathway(pathway) if type(pathway) == str else pathway
        sum_flux = sum(r.flux_expression for r in p.reactions)
        self.solver.add(self.solver.interface.Constraint(sum_flux, lb=0))

    def activate_pathways(self, pathway_names: List[str]):
        '''
        Active all subsystems in names
        '''
        for n in set(pathway_names):
            self.activate_pathway(n)

    def knock_out_pathway(self, pathway):
        '''
        Knock outing subsystems means knock outing all reactions of subsystems
        '''
        p = self.get_pathway(pathway) if type(pathway) == str else pathway
        for r in p.reactions:
            r.knock_out()

    def knock_out_pathways(self, pathway_names: List[str]):
        '''
        Knock outs all pathways in pathway_names list
        '''
        for s in set(pathway_names):
            self.knock_out_pathway(s)

    def increasing_metabolite_constrain(self, metabolite: Metabolite):
        '''
        Set increasing metaolite constraint which is
        m is increasing metabolite where
        r is reactions of m
        constraint is \sum_{i=1}^{n} |V_{r_i}| >= 2
        '''
        sum_flux = sum(r.forward_variable for r in metabolite.reactions)
        self.solver.add(self.solver.interface.Constraint(sum_flux, lb=1e-5))

    def increasing_metabolite_constrains(self, measured_metabolites):
        '''
        Set increasing metabolite constraint
        for increasing metabolite in measurements
        '''
        for k, v in measured_metabolites.items():
            if v > 0:
                metabolite = self.metabolites.get_by_id(k)
                self.increasing_metabolite_constrain(metabolite)

    def set_objective_coefficients(self, measured_metabolites):
        '''
        Set objective function for given measured metabolites
        '''
        self.clean_objective()
        for k, v in measured_metabolites.items():
            m = self.metabolites.get_by_id(k)
            total_stoichiometry = m.total_stoichiometry()

            for r in m.producers():
                update_rate = v * r.metabolites[m] / total_stoichiometry
                r.objective_coefficient += update_rate

    def clean_objective(self):
        self.objective = S.Zero
