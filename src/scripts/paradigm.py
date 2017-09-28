import click
import pandas as pd

from .cli import cli
import models
from services import DataReader, NamingService


@cli.command()
def paradigm():
    model = DataReader().read_network_model()
    X = NamingService('recon').to(DataReader().read_data('BC')[0])

    pd.DataFrame.from_records(X).T.to_csv(
        '../outputs/BC.tsv', sep='\t', header=False)

    write_reaction = lambda f, reaction_id: f.write('abstract\t%s\n' % reaction_id)
    write_metabolite = lambda f, metabolite_id: f.write('protein\t%s\n' % metabolite_id)
    write_pathway = lambda f, pathway_id: f.write('complex\t%s\n' % pathway_id)

    write_reactant = lambda f, metabolite_id, reaction_id: f.write('%s\t%s\t-a>\n' % (metabolite_id, reaction_id))
    write_product = lambda f, metabolite_id, reaction_id: f.write('%s\t%s\t-a|\n' % (metabolite_id, reaction_id))
    write_reaction_pathway = lambda f, reaction_id, pathway_id: f.write('%s\t%s\tcomponent>\n' % (reaction_id, pathway_id))

    files = dict()

    for s in model.subsystems():
        if s:
            files[s] = open('../outputs/%s' % s.replace('/', '-'), 'w')
            write_pathway(files[s], s)

    for m in model.metabolites:
        for s in m.connected_subsystems():
            if s:
                write_metabolite(files[s], m.id)

    for r in model.reactions:
        if r.subsystem:
            f = files[r.subsystem]
            write_reaction(f, r.id)
            write_reaction_pathway(f, r.id, r.subsystem)

            for rea in r.reactants:
                write_reactant(f, rea.id, r.id)

            for pro in r.products:
                write_product(f, pro.id, r.id)

    map(lambda f: f.close(), files.values())
