from subprocess import call
from api import app
from .cli import cli
from api.models import db


@cli.command()
def run_api():
    app.run(host='0.0.0.0', debug=True)


@cli.command()
def run_celery():
    call('celery -A api.celery worker')


@cli.command()
def migrate():
    db.create_all()
