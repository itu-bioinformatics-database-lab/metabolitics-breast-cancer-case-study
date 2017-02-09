import logging
from copy import deepcopy
from itertools import combinations

import cobra as cb
from services import DataReader
from cameo.exceptions import Infeasible

from .base_pathway_model import BasePathwayModel
from models import *

fgs_logger = logging.getLogger('fg_subsystem_fba')
fgs_logger.setLevel(logging.INFO)
fgs_logger.addHandler(logging.FileHandler('../logs/fg_subsystem_fba.log'))


class FGSubsystemFBA(BasePathwayModel):

    def __init__(self, description: cb.Model =None, possibilities='all'):
        super(FGSubsystemFBA, self).__init__(description=description)
        self.possibilities = possibilities
        self.fixed_subsystems = DataReader() \
            .read_subsystem_categories()['fixed-subsystems']

    def _initial_activation_heuristic(self, measured_metabolites):
        '''
        This heuristic assign subsystem to active
        if those subsystems have increasing metabolite in measured metabolites
        to decrease running time of program.
        '''
        initial_active_subsystem = set()
        for k, v in measured_metabolites.items():
            if v > 0:
                m = self.metabolites.get_by_id(k)
                subs = m.connected_subsystems()
                initial_active_subsystem = initial_active_subsystem.union(subs)
        self.activate_pathways(initial_active_subsystem)
        return initial_active_subsystem

    def _init_analysis(self, measured_metabolites):
        # self.increasing_metabolite_constrains(measured_metabolites)
        self.set_objective_coefficients(measured_metabolites)
        return self._initial_activation_heuristic(measured_metabolites)
        # return set()

    def analyze(self, measured_metabolites):
        act_subs = self._init_analysis(measured_metabolites)

        unknown_subsystems = self.subsystems() \
            .difference(act_subs).difference(self.fixed_subsystems)

        if not unknown_subsystems:
            yield act_subs

        for com in self.possible_configurations(unknown_subsystems):
            inactive_com = unknown_subsystems.difference(com)

            if self.has_solution(com, inactive_com):
                yield act_subs.union(com)

    def has_solution(self, activate_subsystems, deactivate_subsystems):
        new_analysis = self.copy()
        new_analysis.knock_out_pathways(deactivate_subsystems)
        new_analysis.activate_pathways(activate_subsystems)
        try:
            return new_analysis.solve().status == 'optimal'
        except Infeasible:
            return False

    def possible_configurations(self, unknown_subsystems):
        if self.possibilities == 'all':
            for i in range(len(unknown_subsystems)):
                for com in combinations(unknown_subsystems, i):
                    yield com
        elif type(self.possibilities) == int and self.possibilities > 0:
            pos = min(self.possibilities, len(unknown_subsystems))
            for com in combinations(unknown_subsystems, pos):
                yield com
        else:
            raise ValueError('Possiblities shouldne all or positive int')

    def analyze_and_save_to_file(self, measured_metabolites, filename):
        with open('../outputs/%s' % filename, 'w', 1) as f:
            for s in self.analyze(measured_metabolites):
                f.write('%s\n' % str(s))
