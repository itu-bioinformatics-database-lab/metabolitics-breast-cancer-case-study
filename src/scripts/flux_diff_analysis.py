from services import DataReader, NamingService
from subprocess import call
from .cli import cli

@cli.command()
def flux_diff_analysis():
    files = ['fva_solutions.enriched_measurements_in_obj.wconst.txt',
             'fva_solutions.enriched_measurements_in_obj.woconst.txt',
             'fva_solutions.enriched_measurements_in_obj.wconst.useV.txt',
             'fva_solutionsfva_solutions.enriched_measurements_in_obj.wconst.lb1.txt']
        #['fva_solutions.cameo.wconst.txt', 'fva_solutions.cameo.woconst.txt',
        #     'fva_solutions.cameo.wconst.weighted.txt', 'fva_solutions6.txt']

    model = DataReader().read_network_model()
    categories = DataReader().read_subsystem_categories()

    (X, y) = DataReader().read_data('BC')
    X = NamingService('recon').to(X)

    subsys_categories = {}
    subsys_measurement_mapping = {}
    max_category_len = 0
    for category, subsystems in categories.items():
        if len(category) > max_category_len:
            max_category_len = len(category)

        for subsys in subsystems:
            subsys_categories[subsys] = category
            subsys_measurement_mapping[subsys] = []

    category_active_counts = {}


    for measurement_dict in X:
        for mid, fold_change in measurement_dict.items():
            metabolite = model.metabolites.get_by_id(mid)
            met_subsystems = {}
            for r in metabolite.reactions:
                subsys = r.subsystem
                if subsys in met_subsystems:
                    continue

                subsys_measurement_mapping[subsys].append(abs(fold_change))
                met_subsystems[subsys] = None
        break


    for file in files:
        fluxes, class_labels = DataReader().read_fva_solutions(file)

        flux_dict = {}
        ix = 0

        max_reaction_length = 0
        while ix < len(fluxes):
            class_label = class_labels[ix]
            subsys_has_active_reaction = {}

            for reaction, flux in fluxes[ix].items():
                rxn, qualifier = reaction[:-4], reaction[-3:]
                flux_dict.setdefault(rxn, {})
                flux_dict[rxn].setdefault(class_label, {})
                flux_dict[rxn][class_label][qualifier] = flux

                subsys = model.reactions.get_by_id(rxn).subsystem
                subsys_has_active_reaction.setdefault(subsys, False)
                if abs(flux) > 0:
                    subsys_has_active_reaction[subsys] = True

                if len(rxn) > max_reaction_length:
                    max_reaction_length = len(rxn)

            for category in categories:
                active = 0
                for subsys in categories[category]:
                    try:
                        if subsys_has_active_reaction[subsys]:
                            active += 1
                    except:
                        continue
                category_active_counts.setdefault(category, [])
                category_active_counts[category].append(active)

            ix += 1

        healthy = 'h'
        diseased = 'bc'
        distances = []
        subsystem_dist_dict = {}
        max_subsys_length = 0

        for reaction, flux_vals in flux_dict.items():
            healthy_flux = (flux_vals[healthy]['min'], flux_vals[healthy]['max'])
            diseased_flux = (flux_vals[diseased]['min'], flux_vals[diseased]['max'])

            interval_length = max(healthy_flux[1], diseased_flux[1]) - min(healthy_flux[0], diseased_flux[0])

            dist = abs(healthy_flux[0] - diseased_flux[0]) + abs(healthy_flux[1] - diseased_flux[1])

            if healthy_flux == diseased_flux:
                dist = 0
            else:
                dist = dist/interval_length

            distances.append((dist, reaction))

            subsys = model.reactions.get_by_id(reaction).subsystem
            subsystem_dist_dict.setdefault(subsys, [])
            subsystem_dist_dict[subsys].append(dist)

            if len(subsys) > max_subsys_length:
                max_subsys_length = len(subsys)

        distances.sort(reverse=True)
        rmean = round(sum([dist for dist, reaction in distances])/len(distances), 4)
        rmedian = distances[(len(distances)//2) + 1][0]

        subsystem_distances = [(sum(distances)/len(distances), subsys) for subsys, distances in subsystem_dist_dict.items()]
        subsystem_distances.sort(reverse=True)
        smean = round(sum([dist for dist, subsys in subsystem_distances])/len(subsystem_distances), 4)
        smedian = subsystem_distances[(len(subsystem_distances) // 2) + 1][0]

        with open('../outputs/diff_%s' % file, 'w') as f:
            f.write('Reaction Level: mean: %s, median: %s, min: %s, max: %s\n' % (str(rmean), str(rmedian),
                                                                      str(distances[len(distances)-1]), str(distances[0])))
            f.write('Subsystem Level: mean: %s, median: %s, min: %s, max: %s\n\n\n' % (str(smean), str(smedian),
                                                                                      str(subsystem_distances[len(subsystem_distances) - 1]),
                                                                                      str(subsystem_distances[0])))

            f.write("Category Activeness (Actual, Avg, Min, Max):\n" + '-' * (max_category_len + 20) + "\n")
            for category, active_counts in category_active_counts.items():
                f.write(('{:>' + str(max_category_len) + '}\t{}\t{:.2f}\t{}\t{}\n').format(category,
                                                                                   len(categories[category]),
                                                                           round(sum(active_counts)/len(active_counts), 2),
                                                                           min(active_counts),
                                                                           max(active_counts)))
            for category in categories:
                if category in category_active_counts:
                    continue

                f.write(('{:>' + str(max_category_len) + '}\t{}\t{}\t{}\t{}\n').format(category,
                                                                                   len(categories[category]),
                                                                                   0, 0 ,0))

            f.write("\n\nSubsystems:\n" + '-'*(max_subsys_length + 25)+"\n")
            for dist, subsys in subsystem_distances:
                f.write(('{:>' + str(max_subsys_length) + '}\t{:.2f}\t{}\t{:.2f}\n').format(subsys, round(dist, 2),len(subsys_measurement_mapping.get(subsys, [])),
                                                                                round(sum(subsys_measurement_mapping.get(subsys, []))/
                                                                                        max(len(subsys_measurement_mapping.get(subsys, [])), 1), 2)))

            f.write("\n\nReactions:\n" + '-'*(max_reaction_length + 5)+"\n")
            for dist, reaction in distances:
                f.write(('{:>' + str(max_reaction_length) + '}\t{:.2f}\n').format(reaction, round(dist, 2)))
