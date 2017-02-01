import logging

from .fg_subsystem_fba import FGSubsystemFBA
from services import DataReader
import cobra as cb


ctg_logger = logging.getLogger('ctg_subsystem_fba')
ctg_logger.setLevel(logging.INFO)
ctg_logger.addHandler(logging.FileHandler('../logs/ctg_subsystem_fba.log'))


class CategoricalSubsystemFBA(FGSubsystemFBA):

    def __init__(self, model: cb.Model, possibilities='all'):
        super().__init__(model, possibilities)
        self.categories = DataReader().read_subsystem_categories()

    def analyze(self, measured_metabolites):
        act_subs = self._init_analysis(measured_metabolites)
        categorical_solutions = dict()
        for k, v in self.categories.items():
            if k == 'fixed-subsystems':
                continue
            init_active = act_subs.intersection(v)
            categorical_solutions[k] = self.analyze_category(k, init_active)
        return categorical_solutions

    def analyze_category(self, category: str, init_active):
        # TODO: Eliminate code repeating between fg_subsystem_fba analyze
        unknown_subsystems = self.categories[category].difference(init_active)

        if not unknown_subsystems:
            yield init_active

        for com in self.possible_configurations(unknown_subsystems):
            inactive_com = unknown_subsystems.difference(com)

            if self.has_solution(com, inactive_com):
                yield init_active.union(com)

    def analyze_and_save_to_file(self, measured_metabolites, filename):
        with open('../outputs/%s' % filename, 'w', 1) as f:

            for k, v in self.analyze(measured_metabolites).items():
                f.write('%s:\n' % k)
                for i in v:
                    f.write('%s\n' % str(i))
