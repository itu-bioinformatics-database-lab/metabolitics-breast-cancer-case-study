from copy import deepcopy
from itertools import combinations

from .base_subsystem_fba import BaseSubsystemFBA
from models import *


class FGSubsystemFBA(BaseSubsystemFBA):

    def __init__(self, model: cb.Model):
        super().__init__(model)
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
        unknown_subsystems = self._model.subsystems().difference(act_subs)

        for i in range(1, len(unknown_subsystems)):
            for com in combinations(unknown_subsystems, i):
                new_analysis = deepcopy(self)

                new_analysis.activate_subsystems(com)
                inactive_com = unknown_subsystems.difference(com)
                new_analysis.deactivate_subsystems(inactive_com)

                if new_analysis.solve().status == 'optimal':
                    yield act_subs.union(com)

    def analyze_and_save_to_file(self, measured_metabolites, filename):
        with open('../outputs/%s' % filename, 'w') as f:
            for s in self.analyze(measured_metabolites):
                f.write('%s\n' % str(s))
