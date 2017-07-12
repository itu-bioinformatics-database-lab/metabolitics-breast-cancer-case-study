from typing import List
import logging
from cobra.core import Model, DictList, Reaction

from cameo.core import SolverBasedModel, Metabolite
from cameo.core.pathway import Pathway

from sympy.core.singleton import S

from services import DataReader
import re
from optlang.exceptions import ContainerAlreadyContains

bpathway_model_logger = logging.getLogger('bpathway_model_logger')
bpathway_model_logger.setLevel(logging.INFO)
bpathway_model_logger \
    .addHandler(logging.FileHandler('../logs/bpathway_model_logger.log'))


class BasePathwayModel(SolverBasedModel):
    '''
    This is base model for subsystem level analysis.
    It adds subsystem level constraints to analysis type
    '''

    @classmethod
    def create_for(cls, dataset_name="recon2"):
        if dataset_name == 'example':
            model = DataReader().create_example_model()
        elif dataset_name == 'example2':
            model = DataReader().create_example2_model()
        else:
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
        \sum_{i=1}^{n} V_{r_i} > 0
        '''
        p = self.get_pathway(pathway) if type(pathway) == str else pathway
        sum_flux = sum(r.forward_variable for r in p.reactions)
        self.solver.add(self.solver.interface.Constraint(sum_flux, lb=1e-5))

    def activate_pathways(self, pathway_names: List[str]):
        '''
        Active all subsystems in names
        '''
        for n in set(pathway_names):
            self.activate_pathway(n)

    def make_pathway_inactive(self, pathway):
        '''
        Knock outing subsystems means knock outing all reactions of subsystems
        '''
        p = self.get_pathway(pathway) if type(pathway) == str else pathway
        sum_flux = sum(r.forward_variable + r.reverse_variable
                       for r in p.reactions)
        self.solver.add(self.solver.interface.Constraint(sum_flux, lb=0, ub=0))

    def make_pathways_inactive(self, pathway_names: List[str]):
        '''
        Knock outs all pathways in pathway_names list
        '''
        for s in set(pathway_names):
            self.make_pathway_inactive(s)

    def set_objective_coefficients(self,
                                   measured_metabolites,
                                   without_transports=True):
        '''
        Set objective function for given measured metabolites
        '''
        self.clean_objective()
        for k, v in measured_metabolites.items():

            m = self.metabolites.get_by_id(k)
            bpathway_model_logger.info(m)
            bpathway_model_logger.info(k)

            total_stoichiometry = m.total_stoichiometry(without_transports)
            bpathway_model_logger.info(total_stoichiometry)

            for r in m.producers(without_transports):
                bpathway_model_logger.info(r.metabolites[m])
                bpathway_model_logger.info(total_stoichiometry)
                update_rate = v * r.metabolites[m] / total_stoichiometry
                r.objective_coefficient += update_rate

    def clean_objective(self):
        self.objective = S.Zero
