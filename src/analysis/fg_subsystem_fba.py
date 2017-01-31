import logging
from copy import deepcopy
from itertools import combinations

from .base_subsystem_fba import BaseSubsystemFBA
from models import *

fgs_logger = logging.getLogger('fg_subsystem_fba')
fgs_logger.setLevel(logging.INFO)
fgs_logger.addHandler(logging.FileHandler('../logs/fg_subsystem_fba.log'))


class FGSubsystemFBA(BaseSubsystemFBA):

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

        counter = 0
        fgs_logger.info('Inital active subsystems: %d' % len(act_subs))

        for com in self.possible_configurations(unknown_subsystems):
            inactive_com = unknown_subsystems.difference(com)

            if self.has_solution(com, inactive_com):
                yield act_subs.union(com)

            if counter % 1 == 0:
                fgs_logger.info('%d of %d calculated' %
                                (counter, 2**len(unknown_subsystems)))
            counter += 1

    def has_solution(self, activate_subsystems, deactivate_subsystems):
        new_analysis = deepcopy(self)
        new_analysis.deactivate_subsystems(deactivate_subsystems)
        new_analysis.activate_subsystems(activate_subsystems)
        return new_analysis.solve().status == 'optimal'

    def possible_configurations(self, unknown_subsystems):
        for i in range(1, len(unknown_subsystems)):
            for com in combinations(unknown_subsystems, i):
                yield com

    def analyze_and_save_to_file(self, measured_metabolites, filename):
        with open('../outputs/%s' % filename, 'w') as f:
            for s in self.analyze(measured_metabolites):
                f.write('%s\n' % str(s))
