from copy import deepcopy
from typing import List
import cobra as cb


class BaseSubsystemFBA:

    def __init__(self, model: cb.Model):
        self._model = deepcopy(model)

    def activate_subsystems(self, subsystem_names: List[str]):
        act_sub_set = set(subsystem_names)
        for r in self._model.reactions:
            if r.subsystem in act_sub_set:
                r.lower_bound = 0.1
                r.objective_coefficient = 1.0

    def solve(self):
        return self._model.optimize()

    def analyze(self, measured_metabolites):
        raise NotImplemented()
