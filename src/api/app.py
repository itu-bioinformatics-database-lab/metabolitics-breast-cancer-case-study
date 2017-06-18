import os
import datetime

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%s:%s@%s/%s' % (
    os.environ.get('POSTGRES_USER', 'postgres'),
    os.environ.get('POSTGRES_PASSWORD', 'secret'),
    os.environ.get('POSTGRES_ADDRESS', 'localhost'),
    os.environ.get('POSTGRES_DB', 'AppDb'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

try:
    app.config['SECRET_KEY'] = open('../secret.txt').read()
except:
    print('Warning: You need to generate secret.txt file to use api')

app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=25)
app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL',
                                                 'redis://localhost:6379')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_RESULT_BACKEND',
                                                     'redis://localhost:6379')

CORS(app)

from .celery import celery
from .models import *
from .auth import *
from .schemas import *
from .views import *
from .admin import *
