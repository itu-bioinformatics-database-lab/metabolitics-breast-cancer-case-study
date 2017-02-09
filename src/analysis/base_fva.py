from .base_pathway_model import BasePathwayModel
from cameo import flux_variability_analysis


class BaseFVA(BasePathwayModel):

    def analyze(self, measured_metabolites):
        self.increasing_metabolite_constrains(measured_metabolites)
        self.set_objective_coefficients(measured_metabolites)
        return flux_variability_analysis(self)
