import os
from collections import defaultdict

import pandas as pd
from functional import seq
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

import models
from services import DataReader, DataWriter, NamingService
from preprocessing import NameMatching, InverseDictVectorizer, DynamicPreprocessing
from .cli import cli


@cli.command()
def paradigm_generate():
    model = DataReader().read_network_model()

    path = '../outputs/paradigm'
    if not os.path.exists(path):
        os.makedirs(path)

    def parse_disease_dataset():
        X, y = DataReader().read_data('BC')

        # vect = DictVectorizer(sparse=False)
        # pipe = Pipeline([
        #     # prepare paradigm
        #     ('naming', NameMatching()),
        #     ('vect', vect),
        #     ('min-max', MinMaxScaler()),
        #     ('inv-vect', InverseDictVectorizer(vect))
        # ])

        pipe = DynamicPreprocessing(['naming', 'metabolic-standard'])
        X_scaled = pipe.fit_transform(X, y)

        df = pd.DataFrame.from_records(X_scaled)
        df.to_csv('%s/BC_data.tsv' % path, sep='\t', index_label='id')

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

        for m in model.metabolites:
            for s in m.connected_subsystems():
                if s:
                    write_metabolite(files[s], m.id)

        for r in model.reactions:
            if r.subsystem:
                write_reaction(files[r.subsystem], r.id)

        for r in model.reactions:
            if r.subsystem:
                for m in r.metabolites:
                    write_relation(files[r.subsystem], m.id, r.id)

        map(lambda f: f.close(), files.values())

    def parse_configuration_file(discs=(-1.33, 1.33), epsilons=(0.01, 0.2)):
        with open('%s/bc.cfg' % path, 'w') as f:
            f.write('inference [method=JTREE,updates=HUGIN,verbose=0]\n')
            f.write(
                'evidence [suffix=_data.tsv,node=mRNA,disc=%f;%f,epsilon=%f,epsilon0=%f]\n'
                % (*discs, *epsilons))

        pathway_names = [
            s.replace('/', '-').replace(' ', '-') for s in model.subsystems()
            if s
        ]

    parse_disease_dataset()
    parse_network_as_pathway_files()
    parse_configuration_file(discs=(-0.5, 0.5))


@cli.command()
def paradigm_run():

    model = DataReader().read_network_model()

    pathway_names = [
        s.replace('/', '-').replace(' ', '-') for s in model.subsystems() if s
    ]

    os.chdir(os.path.join(os.getcwd(), '../outputs/paradigm'))

    # os.chdir(os.path.join(os.getcwd(), '../dataset/paradigm'))

    def analysis_pathway(pathway_name):
        query = './paradigm -c bc.cfg -p pathway_%s.tab -b BC' % pathway_name
        results = os.popen(query).read()

        reaction_ids = set(r.id for r in model.reactions)

        return seq(results.split('> ')[1:]) \
            .map(lambda x: x.split(' ')) \
            .map(lambda x: (int(x[0]), x[1])) \
            .order_by(lambda x: x[0]) \
            .map(lambda x: x[1]) \
            .map(lambda x: x.split('\n')[1:-1]) \
            .map(lambda x: list(map(lambda y: y.split('\t'), x))) \
            .map(lambda x: list(map(lambda y: (y[0], float(y[1])), x))) \
            .map(lambda x: list(filter(lambda y: y[0] in reaction_ids, x))) \
            .to_list()

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    X = defaultdict(list)

    for p in pathway_names:
        print(p)
        results = analysis_pathway(p)
        if results:
            for i, v in enumerate(results):
                X[i] += v

    X = [dict(v) for v in X.values()]
    os.chdir(os.path.join(os.getcwd(), '../../src'))

    _, y = DataReader().read_data('BC')
    DataWriter('paradigm_results').write_json_dataset(X, y)
