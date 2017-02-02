from .base_subsystem_fba import BaseSubsystemFBA
import cobra as cb


class BaseFVA(BaseSubsystemFBA):

    def _init_analysis(self, measured_metabolites):
        # self._init_inc_met_constrains(measured_metabolites)
        self._init_objective_coefficients(measured_metabolites)

    def analyze(self, measured_metabolites):
        self._init_analysis(measured_metabolites)
        return cb.flux_analysis.flux_variability_analysis(self._model)
