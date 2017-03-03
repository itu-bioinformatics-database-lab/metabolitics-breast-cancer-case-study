from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../test.sqlite3'
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_VERIFY_EXPIRATION'] = 60 * 60 * 24 * 10
CORS(app)


from .celery import celery
from .models import *
from .auth import *
from .schemas import *
from .views import *
