from typing import List
import logging
from cobra.core import Model, DictList, Reaction

from cameo.core import SolverBasedModel, Metabolite
from cameo.core.pathway import Pathway

from sympy.core.singleton import S

from services import DataReader
import re
from optlang.exceptions import ContainerAlreadyContains

bpathway_model_logger = logging.getLogger('bpathway_model_logger')
bpathway_model_logger.setLevel(logging.INFO)
bpathway_model_logger \
    .addHandler(logging.FileHandler('../logs/bpathway_model_logger.log'))


class BasePathwayModel(SolverBasedModel):
    '''
    This is base model for subsystem level analysis.
    It adds subsystem level constraints to analysis type
    '''

    @classmethod
    def create_for(cls, dataset_name="recon-model"):
        if dataset_name == 'example':
            model = DataReader().create_example_model()
        else:
            model = DataReader().read_network_model(dataset_name)

        self = cls(description=model)
        return self

    def get_pathway(self, name: str):
        '''
        Gets pathway for given pathway name
        '''
        return Pathway([r for r in self.reactions if r.subsystem == name])

    def activate_pathway(self, pathway):
        '''
        Active subsystem means that
        S is active subsystem where
        r is set of reaction
        r_x \in S
        \sum_{i=1}^{n} V_{r_i} >= 0
        '''
        p = self.get_pathway(pathway) if type(pathway) == str else pathway
        sum_flux = sum(r.flux_expression for r in p.reactions)
        self.solver.add(self.solver.interface.Constraint(sum_flux, lb=0))

    def activate_pathways(self, pathway_names: List[str]):
        '''
        Active all subsystems in names
        '''
        for n in set(pathway_names):
            self.activate_pathway(n)

    def knock_out_pathway(self, pathway):
        '''
        Knock outing subsystems means knock outing all reactions of subsystems
        '''
        p = self.get_pathway(pathway) if type(pathway) == str else pathway
        for r in p.reactions:
            r.knock_out()

    def knock_out_pathways(self, pathway_names: List[str]):
        '''
        Knock outs all pathways in pathway_names list
        '''
        for s in set(pathway_names):
            self.knock_out_pathway(s)

    def increasing_metabolite_constraint(self, metabolite: Metabolite, v, reactions):
        '''
        Set increasing metaolite constraint which is
        m is increasing metabolite where
        r is reactions of m
        constraint is \sum_{i=1}^{n} |V_{r_i}| >= 2
        '''
        lb = 10 ** -5
        bpathway_model_logger.info(metabolite.id)

        metabolite_list = []
        suffixes = 'crmg'  # compartment suffixes

        pat = re.compile('_[%s]$' % suffixes)
        m = re.search(pat, metabolite.id)

        if m == None:
            metabolite_list.append(metabolite.id)
        else:
            prefix = metabolite.id[:m.start()]
            for ch in suffixes:
                metabolite_list.append('%s_%s' % (prefix, ch))

        new_reactions = []

        for mid in metabolite_list:
            try:
                metabolite = self.metabolites.get_by_id(mid)
            except KeyError as err:
                continue  # non-existing compartmental version

            for r in metabolite.producers():
                if r in reactions:
                    continue
                new_reactions.append(r)

        count_new_reactions = len(new_reactions)
        if count_new_reactions == 0:
            return
        elif count_new_reactions == 1:
            r = new_reactions[0]
            c = self.solver.interface.Constraint(r.flux_expression,
                                                 lb=lb)
            self.solver.add(c)
            bpathway_model_logger.info(c)
            reactions.append(r)
            return
        else:
            indicator_vars = []
            for r in new_reactions:
                var = self.solver.interface.Variable(
                    "var_%s" % r.id, type="binary")

                try:
                    # When the indicator is 1, constraint is enforced)
                    c = self.solver.interface.Constraint(r.flux_expression,
                                                         lb=lb,
                                                         indicator_variable=var,
                                                         active_when=1)
                    self.solver.add(c)
                    indicator_vars.append(var)
                    bpathway_model_logger.info(c)
                    reactions.append(r)
                except ContainerAlreadyContains as e:
                    continue
                except:
                    print(r)

            expr = sum(indicator_vars)
            c = self.solver.interface.Constraint(
                expr, lb=1, ub=len(indicator_vars))
            self.solver.add(c)
            bpathway_model_logger.info(c)

    def increasing_metabolite_constraints(self, measured_metabolites):
        '''
        Set increasing metabolite constraint
        for increasing metabolite in measurements
        '''
        reactions = DictList()
        for k, v in measured_metabolites.items():
            if v > 0:
                m = self.metabolites.get_by_id(k)
                self.increasing_metabolite_constraint(m, v, reactions)
        bpathway_model_logger.info(self.solver)
        return reactions

    def set_objective_coefficients(self, measured_metabolites):
        '''
        Set objective function for given measured metabolites
        '''
        self.clean_objective()
        for k, v in measured_metabolites.items():
            m = self.metabolites.get_by_id(k)
            total_stoichiometry = m.total_stoichiometry()

            for r in m.producers():
                update_rate = v * r.metabolites[m] / total_stoichiometry
                r.objective_coefficient += update_rate

    def clean_objective(self):
        self.objective = S.Zero
