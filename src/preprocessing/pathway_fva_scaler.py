from collections import defaultdict
from sklearn.base import TransformerMixin
from services import DataReader


class PathwayFvaScaler(TransformerMixin):
    """Pathway level fva scaler"""

    healthy_rxn_fluxes = {}

    def __init__(self, dataset_name="recon2", file="fva.cameo.0.10.txt"):
        super().__init__()
        self.model = DataReader.read_network_model(dataset_name)
        self.file = file

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None, metrics='sum_distance'):
        subsystem_scores = list()
        distance_metric = False

        if metrics.split('_')[1] == 'distance':
            distance_metric = True

        for x in X:

            if not distance_metric:
                sub_flux = defaultdict(int)
                sub_count = defaultdict(int)
            else:
                # TO DO: Move this data to a more appropriate place
                if len(PathwayFvaScaler.healthy_rxn_fluxes) == 0:
                    print('populating healthy_rxn_fluxes')
                    fluxes, class_labels = DataReader().read_fva_solutions(self.file)
                    flux_dict = {}
                    ix = -1

                    while ix < len(fluxes) - 1:
                        ix += 1
                        class_label = class_labels[ix]

                        if class_label != 'h':
                            continue

                        for reaction, flux in fluxes[ix].items():
                            rxn, qualifier = reaction[:-4], reaction[-3:]
                            flux_dict.setdefault(rxn, {})
                            flux_dict[rxn].setdefault(qualifier, [])
                            flux_dict[rxn][qualifier].append(flux)

                    for reaction, flux_vals in flux_dict.items():
                        PathwayFvaScaler.healthy_rxn_fluxes[reaction] = {}
                        for qualifier in flux_vals:
                            PathwayFvaScaler.healthy_rxn_fluxes[reaction][qualifier] = \
                                sum(flux_vals[qualifier]) / len(flux_vals[qualifier])

            flux_dict = {}
            qualifier_dict = {}

            for reaction_id, flux in x.items():
                reaction = self.model.reactions.get_by_id(reaction_id[:-4])
                min_max = reaction_id[-3:]
                qualifier_dict[min_max] = None

                if distance_metric:
                    flux_dict.setdefault(reaction_id[:-4], {})
                    flux_dict[reaction_id[:-4]][min_max] = flux
                else:
                    sub_flux['%s_%s' % (reaction.subsystem, min_max)] += flux
                    sub_count['%s_%s' % (reaction.subsystem, min_max)] += 1

            if len(qualifier_dict) < 2:
                raise Exception('min or max boundaries are missing: %s' % x)

            if not distance_metric:
                if metrics == 'mean_flux':
                    subsystem_scores.append({
                        s: sub_flux[s] / sub_count[s] for s in sub_flux
                    })
                elif metrics == 'sum_flux':
                    subsystem_scores.append({
                        s: sub_flux[s] / 1 for s in sub_flux
                    })
            else:
                sub_dist = defaultdict(list)
                for reaction, flux_vals in flux_dict.items():
                    rxn = self.model.reactions.get_by_id(reaction)
                    healthy_flux = (PathwayFvaScaler.healthy_rxn_fluxes[reaction]['min'],
                                    PathwayFvaScaler.healthy_rxn_fluxes[reaction]['max'])

                    subject_flux = (flux_vals['min'], flux_vals['max'])
                    interval_length = max(healthy_flux[1], subject_flux[1]) - min(healthy_flux[0], subject_flux[0])

                    if healthy_flux == subject_flux:
                        dist = 0
                    else:
                        dist = (abs(healthy_flux[0] - subject_flux[0]) + abs(healthy_flux[1] - subject_flux[1])) / interval_length

                    sub_dist[rxn.subsystem].append(dist)

                if metrics == 'mean_distance':
                    subsystem_scores.append({
                        s: sum(sub_dist[s]) / len(sub_dist[s]) for s in sub_dist
                    })
                elif metrics == 'sum_distance':
                    subsystem_scores.append({
                        s: sum(sub_dist[s]) for s in sub_dist
                    })

        return subsystem_scores
