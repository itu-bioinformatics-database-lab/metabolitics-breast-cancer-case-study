import click
import cobra as cb

import scripts
from services import DataReader, NamingService
from api import app
from preprocessing import FVARangedMeasurement
from metrics import fva_solution_distance, diff_range_solutions


@click.group()
def cli():
    pass


@cli.command()
def run_api():
    app.run(debug=True)


@cli.command()
def naming_issue():
    scripts.naming_issue()


@cli.command()
def threshold_optimization():
    model = cb.io.load_json_model('../dataset/network/recon-model.json')
    print(scripts.optimal_currency_threshold(model, (2, 100)))


@cli.command()
def cobra_lp_example_with_set_of_constrain():
    scripts.cobra_lp_example_with_set_of_constrain()


@cli.command()
def metabolite_by_connected_subsystems():
    model = cb.io.load_json_model('../dataset/network/recon-model.json')
    metabolites = [(len(set([j.subsystem for j in i.reactions])), i.id)
                   for i in model.metabolites]
    print(sorted(metabolites, key=lambda x: x[0], reverse=True))


@cli.command()
def subsystem_naming():
    scripts.subsystem_naming()


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


if __name__ == '__main__':
    cli()
