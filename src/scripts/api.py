from subprocess import call
import os
import uuid
import json
from collections import defaultdict

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
        m['reactions'] = [r.id for r in
                          model.metabolites.get_by_id(m['id']).reactions]
        model_json['metabolites'][m['id']] = m

    for r in reactions:
        model_json['reactions'][r['id']] = r
        model_json['pathways'][r.get('subsystem', 'NOpathway')].append(r['id'])

    json.dump(model_json, open('../outputs/ng-recon.json', 'w'))
