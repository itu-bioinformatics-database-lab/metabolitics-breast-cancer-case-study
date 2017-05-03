from subprocess import call
import click
import os
import uuid
import json
from collections import defaultdict
import pickle

import pandas as pd
from preprocessing import PathwayFvaScaler, ReactionDiffScaler, \
    DynamicPreprocessing
from sklearn.pipeline import Pipeline

from api import app
from .cli import cli
from api.models import db
from services import DataReader


@cli.command()
def run_api():
    app.run(
        host=os.environ.get('HOST', 'localhost'),
        debug=True
        # os.environ.get('DEBUG', True)
    )


@cli.command()
def run_celery():
    call('celery -A api.celery worker')


@cli.command()
def migrate():
    db.create_all()


@cli.command()
def generate_secret():
    with open('../secret.txt', 'w') as f:
        f.write(str(uuid.uuid4()))


@cli.command()
def generate_angular_friendly_model():
    '''
    This function convert json model into angular friendly json
    '''
    model = DataReader().read_network_model()
    model_json = json.load(open('../dataset/network/recon2.json'))

    reactions, metabolites = model_json['reactions'], model_json['metabolites']
    model_json = defaultdict(dict)
    model_json['pathways'] = defaultdict(list)

    for m in metabolites:
        m['reactions'] = [
            r.id for r in model.metabolites.get_by_id(m['id']).reactions
        ]
        model_json['metabolites'][m['id']] = m

    for r in reactions:
        # r['gene_reaction_rule'], r['notes'] = [], {}
        del r['gene_reaction_rule']
        del r['notes']

        model_json['reactions'][r['id']] = r
        model_json['pathways'][r.get('subsystem', 'NOpathway')].append(r['id'])

    json.dump(model_json, open('../outputs/ng-recon.json', 'w'))


@cli.command()
@click.argument('num_of_reactions')
def healty_for_heatmap(num_of_reactions):
    (X, y) = DataReader().read_fva_solutions('fva_without.transports.txt')
    X = Pipeline([
        ('flux-diff-scaler', ReactionDiffScaler()),
        ('pathway_scoring', PathwayFvaScaler()),
    ]).fit_transform(X, y)

    df = pd.DataFrame(ix for ix, iy in zip(X, y) if iy == 'h')

    hjson = {
        'x': [i[:-4] for i in df],
        'z': df.values.tolist(),
        'type': 'heatmap'
    }

    json.dump(hjson, open('../outputs/healties_heatmap.json', 'w'))


@cli.command()
def healties_model():
    (X, y) = DataReader().read_data('BC')
    pre_model = DynamicPreprocessing(['naming', 'metabolic-standard'])
    X = pre_model.fit_transform(X, y)

    model = DynamicPreprocessing(['fva', 'flux-diff'])
    model.fit(X, y)
    with open('../outputs/api_model.p', 'wb') as f:
        pickle.dump(model, f)
