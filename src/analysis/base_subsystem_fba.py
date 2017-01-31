from copy import deepcopy
from typing import List

import cobra as cb

from services import DataReader


class BaseSubsystemFBA:

    def __init__(self, model: cb.Model):
        self._model = deepcopy(model)
        self._model.objective = dict()

    @classmethod
    def create_for(cls, dataset_name="recon-model"):
        model = DataReader().read_network_model(dataset_name)
        self = cls(model)
        return self

    def activate_subsystems(self, subsystem_names: List[str]):
        '''
        Active subsystem means that
        S is active subsystem where
        r is set of reaction
        r_x \in S
        \sum_{i=1}^{n} r_i > 0

        If you want to understand how implemented constrain above,
        check cobra_lp_example_with_set_of_constrain in script folder.
        '''
        act_sub_set = set(subsystem_names)
        constraining_dummy_metabolites = dict()

        for s in act_sub_set:
            name = 'cdm_%s' % s
            constraining_dummy_metabolites[name] = cb.Metabolite(name)
            constraining_dummy_metabolites[name]._constraint_sense = "G"
            constraining_dummy_metabolites[name]._bound = 0

        for r in self._model.reactions:
            if r.subsystem in act_sub_set:
                cdm = constraining_dummy_metabolites['cdm_%s' % s]
                r.add_metabolites({cdm: 1})

    def deactivate_subsystems(self, subsystem_names: List[str]):
        '''
        Deactive subsystem
        '''
        inact_sub_set = set(subsystem_names)
        for r in self._model.reactions:
            if r.subsystem in inact_sub_set:
                r.upper_bound = 0
                r.lower_bound = 0
                r.objective_coefficient = 0

    def _init_inc_met_constrains(self, measured_metabolites):
        '''Init increasing metabolite constrains'''
        for k, v in measured_metabolites.items():
            if v > 0:
                m = self._model.metabolites.get_by_id(k)
                m._constraint_sense = "G"
                m._bound = 1

    def _init_objective_coefficients(self, measured_metabolites):
        for k, v in measured_metabolites.items():
            m = self._model.metabolites.get_by_id(k)
            total_stoichiometry = m.total_stoichiometry()
            for r in m.producers():
                update_rate = v * r.metabolites[m] / total_stoichiometry
                r.objective_coefficient += update_rate

    def solve(self):
        return self._model.optimize()

    def analyze(self, measured_metabolites):
        raise NotImplemented()
