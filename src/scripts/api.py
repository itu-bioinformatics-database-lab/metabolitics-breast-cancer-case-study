from subprocess import call
import os
from api import app
from .cli import cli
from api.models import db


@cli.command()
def run_api():
    app.run(
        host=os.environ.get('HOST', 'localhost'),
        debug=os.environ.get('DEBUG', True)
    )


@cli.command()
def run_celery():
    call('celery -A api.celery worker')


@cli.command()
def migrate():
    db.create_all()
