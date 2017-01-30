import click
import cobra as cb
import scripts


@click.group()
def cli():
    pass


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


if __name__ == '__main__':
    cli()
