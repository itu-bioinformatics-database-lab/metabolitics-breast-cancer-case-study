from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../test.sqlite3'

from .celery import celery
from .models import *
from .schemas import *
from .views import *
