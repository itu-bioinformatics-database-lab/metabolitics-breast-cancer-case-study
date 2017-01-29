from copy import deepcopy
from itertools import combinations

from .base_subsystem_fba import BaseSubsystemFBA
from models import *


class FGSubsystemFBA(BaseSubsystemFBA):

    def __init__(self, model: cb.Model):
        BaseSubsystemFBA.__init__(self, model)
        self.model = {}

    def _initial_activation_heuristic(self, measured_metabolites):
        '''
        This heuristic assign subsystem to active
        if those subsystems have increasing metabolite in measured metabolites
        to decrease running time of program.
        '''
        initial_active_subsystem = set()
        for k, v in measured_metabolites.items():
            if v > 0:
                m = self._model.metabolites.get_by_id(k)
                subs = m.connected_subsystems()
                initial_active_subsystem = initial_active_subsystem.union(subs)
        self.activate_subsystems(initial_active_subsystem)
        return initial_active_subsystem

    def analyze(self, measured_metabolites):
        act_subs = self._initial_activation_heuristic(measured_metabolites)

        unknown_subsystems = self._model.subsystems().intersection(act_subs)

        for i in range(len(unknown_subsystems)):
            for c in combinations(unknown_subsystems, i):
                new_analysis = deepcopy(self)
                new_analysis.activate_subsystems(c)
                if new_analysis.solve().status == 'optimal':
                    yield c
