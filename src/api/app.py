import os

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

config = {
    "development": "api.config.DevelopmentConfig",
    "testing": "api.config.TestingConfig",
    "production": "api.config.ProductionConfig"
}

app.config.from_object(config[os.getenv('FLASK_CONFIGURATION', 'development')])

from .celery import celery
from .models import *
from .auth import *
from .schemas import *
from .views import *
from .admin import *
