from subprocess import call
from .cli import cli
import click
import cobra as cb

from sklearn.feature_selection import f_classif, VarianceThreshold
from sklearn.feature_extraction import DictVectorizer
import numpy as np

from services import DataReader, NamingService
#from api import app
from preprocessing import FVARangedMeasurement
from metrics import fva_solution_distance, diff_range_solutions
from classifiers import FVADiseaseClassifier
from .optimal_currency_threshold import optimal_currency_threshold


@cli.command()
def run_api():
    app.run(debug=True)


@cli.command()
def run_celery():
    call('celery -A api.celery worker')


@cli.command()
def threshold_optimization():
    model = cb.io.load_json_model('../dataset/network/recon-model.json')
    print(optimal_currency_threshold(model, (2, 100)))


@cli.command()
def metabolite_by_connected_subsystems():
    model = cb.io.load_json_model('../dataset/network/recon-model.json')
    metabolites = [(len(set([j.subsystem for j in i.reactions])), i.id)
                   for i in model.metabolites]
    print(sorted(metabolites, key=lambda x: x[0], reverse=True))


@cli.command()
def subsystem_statistics():
    categories = DataReader().read_subsystem_categories()
    total = 0
    for k, v in categories.items():
        print(k, len(v))
        total += len(v)
    print('total:', total)


@cli.command()
def fva_range_analysis_save():
    (X, y) = DataReader().read_data('BC')
    X = NamingService('recon').to(X)
    X = FVARangedMeasurement().fit_transform(X, y)
    with open('../outputs/fva_solutions.txt', 'w') as f:
        for x, label in zip(X, y):
            f.write('%s %s\n' % (label, x))


@cli.command()
def constraint_logging():
    (X, y) = DataReader().read_data('BC')
    X = NamingService('recon').to(X)
    (X_h, y_h) = [(x, l) for x, l in zip(X, y) if l == 'h'][0]
    (X_bc, y_bc) = [(x, l) for x, l in zip(X, y) if l == 'bc'][0]
    FVARangedMeasurement().fit_transform([X_bc, X_h], [y_bc, y_h])


@cli.command()
def border_rate():
    model = DataReader().read_network_model()
    num_border_reaction = len(set(r.id
                                  for m in model.metabolites
                                  for r in m.reactions
                                  if m.is_border()))
    print(num_border_reaction / len(model.reactions))


@cli.command()
@click.argument('filename')
def fva_min_max_mean(filename):
    (X, y) = DataReader().read_fva_solutions(filename)
    print(fva_solution_distance(X))


@cli.command()
@click.argument('filename')
def fva_diff_range_solutions(filename):
    (X, y) = DataReader().read_fva_solutions(filename)
    X_h = [x for x, l in zip(X, y) if l == 'h']
    X_bc = [x for x, l in zip(X, y) if l == 'bc']
    print(diff_range_solutions(X_h, X_bc))


@cli.command()
@click.argument('top_num_reaction')
def most_correlated_reactions(top_num_reaction):
    file_name = 'fva.recon2.cameo.8.txt'
    (X, y) = DataReader().read_fva_solutions(file_name)
    vect = DictVectorizer(sparse=False)
    X = vect.fit_transform(X)
    vt = VarianceThreshold(0.1)
    X = vt.fit_transform(X)
    (F, pval) = f_classif(X, y)

    feature_names = np.array(vect.feature_names_)[vt.get_support()]
    top_n = sorted(zip(feature_names, F),
                   key=lambda x: x[1],
                   reverse=True)

    if int(top_num_reaction) > 0:
        top_n = top_n[:int(top_num_reaction)]

    model = DataReader().read_network_model()
    subsystem_stats = {}
    with open('../outputs/corr_rxns_%s' % file_name, 'w') as f:
        max_subsys_length = 0
        for n, v in top_n:
            reaction = model.reactions.get_by_id(n[:-4])
            # f.write('name: %s\n' % n[:-4])
            # f.write('reaction: %s\n' % reaction.reaction)
            # f.write('subsystem: %s\n' % reaction.subsystem)
            # f.write('min-max: %s\n' % n[-3:])
            # f.write('F: %s\n' % v)
            # f.write('-' * 10 + '\n')
            subsystem_stats.setdefault(reaction.subsystem, [0, []])
            subsystem_stats[reaction.subsystem][0] += 1
            subsystem_stats[reaction.subsystem][1] += [v]

            if len(reaction.subsystem) > max_subsys_length:
                max_subsys_length = len(reaction.subsystem)

        f.write("\n\n")
        for v, cnt, subsys in sorted([(max(stats[1]), stats[0], subsys) for subsys, stats in subsystem_stats.items()], reverse=True):
            f.write(('{:>' + str(max_subsys_length) + '}\t{}\t{:.2f}\n').format(subsys, cnt, v))