from typing import List
import logging

from cobra.core import Metabolite
from services import DataReader

bpathway_model_logger = logging.getLogger('bpathway_model_logger')
bpathway_model_logger.setLevel(logging.INFO)
bpathway_model_logger \
    .addHandler(logging.FileHandler('../logs/bpathway_model_logger.log'))


class BaseSolver:

    def __init__(self, model):
        self._model = model.copy()

    @classmethod
    def create_for(cls, dataset_name="recon-model"):
        if dataset_name == 'example':
            model = DataReader().create_example_model()
        else:
            model = DataReader().read_network_model(dataset_name)
        return BaseSolver(model)

    def get_pathway(self, name: str):
        '''
        Gets pathway for given pathway name
        '''
        return [r for r in self.reactions if r.subsystem == name]

    def activate_pathway(self, pathway):
        '''
        Active subsystem means that
        S is active subsystem where
        r is set of reaction
        r_x \in S
        \sum_{i=1}^{n} V_{r_i} >= 0
        '''
        pass

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

    def increasing_metabolite_constraint(self, metabolite: Metabolite, v):
        '''
        Set increasing metaolite constraint which is
        m is increasing metabolite where
        r is reactions of m
        constraint is \sum_{i=1}^{n} |V_{r_i}| >= 2
        '''
        pass

    def increasing_metabolite_constraints(self, measured_metabolites):
        '''
        Set increasing metabolite constraint
        for increasing metabolite in measurements
        '''
        for k, v in measured_metabolites.items():
            if v > 0:
                m = self.metabolites.get_by_id(k)
                self.increasing_metabolite_constraint(m, v)

    def set_objective_coefficients(self, measured_metabolites):
        '''
        Set objective function for given measured metabolites
        '''
        for k, v in measured_metabolites.items():
            m = self.metabolites.get_by_id(k)
            total_stoichiometry = m.total_stoichiometry()

            for r in m.producers():
                update_rate = v * r.metabolites[m] / total_stoichiometry
                r.objective_coefficient += update_rate
