from flask_jwt import JWT
from werkzeug.security import safe_str_cmp

from .app import app
from .models import User


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and safe_str_cmp(
            user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    return User.query.get(payload['identity'])


jwt = JWT(app, authenticate, identity)
