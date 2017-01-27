import click
import math
import cobra as cb
import cobra.test
from scripts import optimal_currency_threshold


@click.group()
def cli():
    pass


@cli.command()
def threshold_optimization():
    model = cb.io.load_json_model('../dataset/recon-model.json')
    print(optimal_currency_threshold(model, (2, 100)))


if __name__ == '__main__':
    cli()


# asd = [(len(i.reactions), i.id) for i in model.metabolites]
#
#

# model = cb.io.load_json_model('../dataset/recon-model.json')
# model.metabolites.currency_threshold = math.inf
#
# asd = [(len(set([j.subsystem for j in i.reactions])), i.id)
#        for i in model.metabolites if not i.is_currency()]
#
# asd = sorted(asd, key=lambda x: x[0], reverse=True)[:100]
#
# print(asd)
