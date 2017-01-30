from copy import deepcopy
from typing import List
import cobra as cb


class BaseSubsystemFBA:

    def __init__(self, model: cb.Model):
        self._model = deepcopy(model)

    def activate_subsystems(self, subsystem_names: List[str]):
        '''
        Active subsystem means that
        S is active subsystem where
        r is set of reaction
        r_x \in S
        \sum_{i=1}^{n} r_i > 0
        and
        C is objective coefficient of fba
        C_{r_i} = 1

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
                r.objective_coefficient = 1.0

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

    def solve(self):
        return self._model.optimize()

    def analyze(self, measured_metabolites):
        raise NotImplemented()
