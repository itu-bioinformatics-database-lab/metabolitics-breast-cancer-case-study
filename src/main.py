import click
import cobra as cb
from scripts import optimal_currency_threshold, \
    cobra_lp_example_with_set_of_constrain as cobra_lp_example
from analysis import FGSubsystemFBA


@click.group()
def cli():
    pass


@cli.command()
def threshold_optimization():
    model = cb.io.load_json_model('../dataset/recon-model.json')
    print(optimal_currency_threshold(model, (2, 100)))


@cli.command()
def cobra_lp_example_with_set_of_constrain():
    cobra_lp_example()


@cli.command()
def metabolite_by_connected_subsystems():
    model = cb.io.load_json_model('../dataset/recon-model.json')
    metabolites = [(len(set([j.subsystem for j in i.reactions])), i.id)
                   for i in model.metabolites]
    print(sorted(metabolites, key=lambda x: x[0], reverse=True))


@cli.command()
def fg_subsystem_fba():
    model = cb.io.load_json_model('../dataset/recon-model.json')

    # ecolin_measured_metabolites = {'etoh_e': 1, 'gln__L_c': 1}
    measured_metabolites = {'glu_L_c': 1}
    analysis = FGSubsystemFBA(model)

    analysis.analyze_and_save_to_file(
        measured_metabolites, 'recon-model.fg_subsystem_fba.txt')

if __name__ == '__main__':
    cli()
