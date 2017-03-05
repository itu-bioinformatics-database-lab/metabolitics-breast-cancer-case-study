from flask import Flask
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../test.sqlite3'
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=25)
CORS(app)


from .celery import celery
from .models import *
from .auth import *
from .schemas import *
from .views import *
