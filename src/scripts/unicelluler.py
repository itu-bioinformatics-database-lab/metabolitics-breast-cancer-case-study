from functools import reduce

import pandas as pd
import cobra as cb
from cobra import Model, Reaction

from .cli import cli


@cli.command()
def generate_uniceller_network():
    df = pd.DataFrame.from_csv('../dataset/unicelluler_flux.csv')

    model = cb.Model('unicelluler')

    for i in df.index:
        r = cb.Reaction(i)
        model.add_reaction(r)

        black_list = ['(Cell synthesis)', '(Evolution)', 'Exch. (', ')']
        r.reaction = reduce(lambda x, y: x.replace(y, ''), black_list,
                            i.replace('->', '-->'))

    cb.io.save_json_model(model, '../outputs/unicelluler.json')
