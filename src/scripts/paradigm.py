import os

import pandas as pd

import models
from services import DataReader, NamingService
from .cli import cli


@cli.command()
def paradigm():
    model = DataReader().read_network_model()

    path = '../outputs/paradigm'
    if not os.path.exists(path):
        os.makedirs(path)

    def parse_disease_dataset():
        X, y = DataReader().read_data('BC')
        X = NamingService('recon').to(X)

        df = pd.DataFrame.from_records(X)
        df.to_csv('%s/BC.tsv' % path, sep='\t')

    def parse_network_as_pathway_files():
        write_reaction = lambda f, reaction_id: f.write('abstract\t%s\n' % reaction_id)
        write_metabolite = lambda f, metabolite_id: f.write('protein\t%s\n' % metabolite_id)
        write_relation = lambda f, metabolite_id, reaction_id: f.write('%s\t%s\t-a>\n' % (metabolite_id, reaction_id))

        # TOTHINK: be sure about right mapping

        files = {
            s: open('%s/pathway_%s.tab' %
                    (path, s.replace('/', '-').replace(' ', '-')), 'w')
            for s in model.subsystems() if s
        }

        # f = open('%s/pathway_data.tab' % path, 'w')

        for m in model.metabolites:
            for s in m.connected_subsystems():
                if s:
                    write_metabolite(files[s], m.id)
                    # write_metabolite(f, m.id)

        for r in model.reactions:
            if r.subsystem:
                write_reaction(files[r.subsystem], r.id)

        for r in model.reactions:
            if r.subsystem:
                for m in r.metabolites:
                    write_relation(files[r.subsystem], m.id, r.id)

        # f.close()
        map(lambda f: f.close(), files.values())

    def parse_configuration_file():
        with open('%s/bc.cfg' % path, 'w') as f:
            # f.write('inference [method=BP,updates=SEQFIX,tol=1,maxiter=100000]\n')
            f.write('inference [method=JTREE,updates=HUGIN,verbose=1]\n')
            f.write(
                'evidence [suffix=.tsv,node=mRNA,disc=–0.33;0.33,epsilon=0.1]\n'
            )

        pathway_names = [
            s.replace('/', '-').replace(' ', '-') for s in model.subsystems()
            if s
        ]
        # print('./paradigm -c bc.cfg %s  -b pathway' %
        #      ''.join(map(lambda x: ' -p pathway_%s.tab' % x, pathway_names)))

    parse_disease_dataset()
    parse_network_as_pathway_files()
    parse_configuration_file()
