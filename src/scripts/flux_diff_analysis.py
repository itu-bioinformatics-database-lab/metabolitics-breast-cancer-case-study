from services import DataReader
from subprocess import call
from .cli import cli

@cli.command()
def flux_diff_analysis():
    files = ['fva_solutions.cameo.wconst.txt', 'fva_solutions.cameo.woconst.txt',
             'fva_solutions.cameo.wconst.weighted.txt', 'fva_solutions6.txt']

    model = DataReader().read_network_model()

    for file in files:
        fluxes, class_labels = DataReader().read_fva_solutions(file)

        flux_dict = {}
        ix = 0

        while ix < len(fluxes):
            class_label = class_labels[ix]
            for reaction, flux in fluxes[ix].items():
                rxn, qualifier = reaction[:-4], reaction[-3:]
                flux_dict.setdefault(rxn, {})
                flux_dict[rxn].setdefault(class_label, {})
                flux_dict[rxn][class_label][qualifier] = flux
            ix += 1

        healthy = 'h'
        diseased = 'bc'
        distances = []
        subsystem_dist_dict = {}
        for reaction, flux_vals in flux_dict.items():
            healthy_flux = (flux_vals[healthy]['min'], flux_vals[healthy]['max'])
            diseased_flux = (flux_vals[diseased]['min'], flux_vals[diseased]['max'])

            interval_length = max(healthy_flux[1], diseased_flux[1]) - min(healthy_flux[0], diseased_flux[0])

            dist = abs(healthy_flux[0] - diseased_flux[0]) + abs(healthy_flux[1] - diseased_flux[1])

            if healthy_flux == diseased_flux:
                distance = 0
            else:
                try:
                    dist = dist/float(interval_length)
                except ZeroDivisionError:
                    print(healthy_flux, diseased_flux)

            distances.append((dist, reaction))

            subsys = model.reactions.get_by_id(reaction).subsystem
            subsystem_dist_dict.setdefault(subsys, [])
            subsystem_dist_dict[subsys].append(dist)

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
            f.write("Subsystems:\n----------------------\n")
            for dist, subsys in subsystem_distances:
                f.write('%s\t\t\t%s\n' % (subsys, dist))

            f.write("\n\nReactions:\n----------------------\n")
            for dist, reaction in distances:
                f.write('%s\t\t\t%s\n' % (reaction, dist))


