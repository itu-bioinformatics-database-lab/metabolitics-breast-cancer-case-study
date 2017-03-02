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

    def increasing_metabolite_constraint_cobra_indicator_var(self, metabolite: Metabolite, v, reactions):
        '''
        Set increasing metaolite constraint which is
        m is increasing metabolite where
        r is reactions of m
        constraint is that at least one of the producers should be active (>=10^-5)
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

            met_reactions = []
            consumer_reaction_count = 0
            consumer_reaction = None

            for r in metabolite.reactions:
                if 'biomass' in r.name.lower():
                    continue

                coeff = r.get_coefficient(mid)
                if coeff == 0:
                    continue

                if coeff > 0 or r.lower_bound < 0:
                    met_reactions.append((r, coeff))

                if coeff < 0 or r.lower_bound < 0:
                    consumer_reaction_count += 1
                    consumer_reaction = r

            if consumer_reaction_count > 1 or \
                    (consumer_reaction_count == 1 and (len(met_reactions) > 1 or consumer_reaction.lower_bound >= 0)):
                new_reactions.extend(met_reactions)

        count_new_reactions = len(new_reactions)
        if count_new_reactions == 0:
            return
        else:
            indicator_vars = []
            for r, coeff in new_reactions:
                if (r.id, coeff) in reactions:
                    indicator_var_name = reactions[(r.id, coeff)][1]
                    constraint_name = reactions[(r.id, coeff)][2]
                else:
                    # indicator variable creation
                    indicator_var_name = "var_%s_%d" % (r.id, coeff)
                    self.lp.variables.add(names=[indicator_var_name],
                                          lb=[0],
                                          ub=[1],
                                          types=[self.lp.variables.type.binary])

                    # create the constraint on reaction flux
                    constraint_name = "const_%s_%s" % (metabolite.id, r.id)
                    if coeff > 0:
                        expr_val = 1
                    else:
                        expr_val = -1

                    ic_dict = {}
                    ic_dict["lin_expr"] = SparsePair(
                        ind=[r.id], val=[expr_val])
                    ic_dict["rhs"] = lb
                    ic_dict["sense"] = "G"
                    ic_dict["indvar"] = indicator_var_name
                    ic_dict["complemented"] = 1
                    self.lp.indicator_constraints.add(**ic_dict)

                    reactions[(r.id, coeff)] = [
                        r, indicator_var_name, constraint_name]

                indicator_vars.append(indicator_var_name)
                bpathway_model_logger.info(constraint_name)

            vars = indicator_vars
            coeffs = [1] * len(indicator_vars)
            self.lp.linear_constraints.add(lin_expr=[SparsePair(ind=vars, val=coeffs)],
                                           senses=["G"],
                                           rhs=[1],
                                           names=['Const_OR_%s' % metabolite.id])

            bpathway_model_logger.info('Const_OR_%s' % metabolite.id)

    def increasing_metabolite_constraint_cameo_indicator_const(self, metabolite: Metabolite, v, reactions):
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

            met_reactions = []
            consumer_reaction_count = 0
            consumer_reaction = None

            for r in metabolite.reactions:
                #     if r in reactions:
                #         continue
                if 'biomass' in r.name.lower():
                    continue

                coeff = r.get_coefficient(mid)
                if coeff == 0:
                    continue

                if coeff > 0 or r.lower_bound < 0:
                    met_reactions.append((r, coeff))

                if coeff < 0 or r.lower_bound < 0:
                    consumer_reaction_count += 1
                    consumer_reaction = r

            if consumer_reaction_count > 1 or \
                    (consumer_reaction_count == 1 and (len(met_reactions) > 1 or consumer_reaction.lower_bound >= 0)):
                new_reactions.extend(met_reactions)

        count_new_reactions = len(new_reactions)
        if count_new_reactions == 0:
            return
        else:
            indicator_vars = []
            for r, coeff in new_reactions:
                if (r.id, coeff) in reactions:
                    var = reactions[(r.id, coeff)][1]
                    c = reactions[(r.id, coeff)][2]
                    c = None
                else:
                    var = self.solver.interface.Variable(
                        "var_%s_%d" % (r.id, coeff), type="binary")
                    try:
                        if coeff > 0:
                            expr = r.flux_expression
                        else:
                            expr = -1 * r.flux_expression
                        # When the indicator is 1, constraint is enforced)
                        c = self.solver.interface.Constraint(expr,
                                                             lb=lb,
                                                             indicator_variable=var,
                                                             active_when=1)
                        self.solver.add(c)
                    except ContainerAlreadyContains as e:
                        raise
                    except:
                        print(r)
                        raise

                    reactions[(r.id, coeff)] = [r, var, c]

                indicator_vars.append(var)
                try:
                    if c == None:
                        bpathway_model_logger.info('existing constraint')
                    else:
                        bpathway_model_logger.info(c)
                except:
                    raise

            ub = len(indicator_vars)
            lb = 1
            if ub > 1:
                expr = sum(indicator_vars)
            else:
                expr = var + var
                lb = 2
                ub = 2

            try:
                c = self.solver.interface.Constraint(expr, lb=lb, ub=ub)
                self.solver.add(c)
                bpathway_model_logger.info(c)
            except:
                raise

    def increasing_metabolite_constraint_linear(self, metabolite: Metabolite, v, reactions):
        '''
        Set increasing metaolite constraint which is
        m is increasing metabolite where
        r is reactions of m
        constraint is \sum_{i=1}^{n} |V_{r_i}| >= 2
        '''
        lb = 10 ** -5
        bpathway_model_logger.info(metabolite.id)

        metabolite_list = []
        suffixes = 'crmge'  # compartment suffixes

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

            met_reactions = []
            consumer_reaction_count = 0
            consumer_reaction = None

            for r in metabolite.reactions:
                #     if r in reactions:
                #         continue
                if 'biomass' in r.name.lower():
                    continue

                coeff = r.get_coefficient(mid)
                if coeff == 0:
                    continue

                if coeff > 0 or r.lower_bound < 0:
                    met_reactions.append((r, coeff))

                if coeff < 0 or r.lower_bound < 0:
                    consumer_reaction_count += 1
                    consumer_reaction = r

            if consumer_reaction_count > 1 or \
                    (consumer_reaction_count == 1 and (len(met_reactions) > 1 or consumer_reaction.lower_bound >= 0)):
                new_reactions.extend(met_reactions)

        count_new_reactions = len(new_reactions)
        if count_new_reactions == 0:
            return
        else:
            vars = []

            # create the constraint on reaction flux
            constraint_name = "const_%s_%s" % (metabolite.id, r.id)

            for r, coeff in new_reactions:
                if r.id in reactions:
                    continue

                if coeff > 0:
                    vars.append(r.forward_variable)
                else:
                    vars.append(r.reverse_variable)

                reactions[r.id] = [r]

            expr = sum(vars)
            c = self.solver.interface.Constraint(expr, lb=lb)
            self.solver.add(c)

    def increasing_metabolite_constraints(self, measured_metabolites):
        '''
        Set increasing metabolite constraint
        for increasing metabolite in measurements
        '''
        reactions = {}
        #reactions = DictList()

        measured_metabolites = list(measured_metabolites.items())
        measured_metabolites.sort()
        counter = 0
        for k, v in measured_metabolites:
            if v > 0:
                m = self.metabolites.get_by_id(k)
                self.increasing_metabolite_constraint_linear(m, v, reactions)

                # if counter >= 0:
                #     break
                counter += 1
        bpathway_model_logger.info(self.solver)
        return DictList(set([rxn_const_triplet[0] for rxn_const_triplet in reactions.values()]))

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
