from functools import reduce

import pandas as pd
import cobra as cb
from cobra import Model, Reaction, Metabolite

from .cli import cli


@cli.command()
def generate_unicelluler_network():
    df_flux = pd.DataFrame.from_csv(
        '../dataset/unicelluler/unicelluler_flux.csv')
    df_metabolite_names = pd.DataFrame.from_csv(
        '../dataset/unicelluler/unicelluler_metabolite_names.csv')
    df_metabolites = pd.DataFrame.from_csv(
        '../dataset/unicelluler/unicelluler_metabolites.csv')

    model = cb.Model('unicelluler')

    model.add_metabolites(
        Metabolite(id=row['id'], name=row['name'])
        for _, row in df_metabolite_names.iterrows())

    for i in df_flux.index:
        r = cb.Reaction(i)
        model.add_reaction(r)

        black_list = ['(Cell synthesis)', '(Evolution)', 'Exch. (', ')']
        r.reaction = reduce(lambda x, y: x.replace(y, ''), black_list,
                            i.replace('->', '-->'))

    cb.io.save_json_model(model, '../outputs/unicelluler.json')
