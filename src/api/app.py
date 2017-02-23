from flask import Flask
from flask_restful import Api

from .celery import make_celery

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

celery = make_celery(app)
api = Api(app)


from .resources import *

api.add_resource(StartWithQuery, '/search/<query>')
api.add_resource(FVAAnalysis, '/analysis/fva')
