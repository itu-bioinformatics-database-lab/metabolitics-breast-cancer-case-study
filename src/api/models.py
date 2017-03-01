from flask_sqlalchemy import SQLAlchemy
from .app import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    affiliation = db.Column(db.String(255))
    password = db.Column(db.String(255))  # TODO: hash password
    analysis = db.relationship("Analysis", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.email


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    status = db.Column(db.Boolean)
    filename = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="analysis")

    def __init__(self, name, filename, user, status=False):
        self.name = name
        self.filename = filename
        self.user = user
        self.status = status
