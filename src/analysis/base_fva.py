from .base_pathway_model import BasePathwayModel
import cobra as cb


class BaseFVA(BasePathwayModel):

    def analyze(self, measured_metabolites):
        self.set_objective_coefficients(measured_metabolites)
        return cb.flux_analysis.flux_variability_analysis(self._model)
