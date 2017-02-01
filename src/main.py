import click
import cobra as cb
import scripts
from services import DataReader
from api import app


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
def run_fg_subsystem_fba():
    scripts.run_fg_subsystem_fba()


@cli.command()
def run_categorical_subsystem_fba():
    scripts.run_categorical_subsystem_fba()


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


if __name__ == '__main__':
    cli()
