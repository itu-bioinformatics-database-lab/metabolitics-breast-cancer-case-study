import os
import datetime

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../db/db.sqlite3'
# "postgresql://postgres:%s@localhost"\
# % os.environ.get("POSTGRES_PASSWORD", "xpst123")

app.config['SECRET_KEY'] = open('../secret.txt').read()
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=25)

app.config['CELERY_BROKER_URL'] = os.environ.get(
    'CELERY_BROKER_URL', 'redis://localhost:6379')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379')

CORS(app)


from .celery import celery
from .models import *
from .auth import *
from .schemas import *
from .views import *
