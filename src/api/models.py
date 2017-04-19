import uuid
import datetime
import json

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
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="analysis")

    _path = '../db/analysis-result'

    def __init__(self, name, user, status=False):
        self.name = name
        self.filename = str(uuid.uuid4())
        self.start_time = datetime.datetime.now()
        self.user = user
        self.status = status

    def load_results(self):
        self.results = dict()
        t = (self._path, self.filename)
        with open('%s/reaction/%s.json' % t) as f:
            self.results['reaction'] = json.load(f)
        with open('%s/pathway/%s.json' % t) as f:
            self.results['pathway'] = json.load(f)

    def save_results(self, reaction_scores, pathway_scores):
        t = (self._path, self.filename)
        with open('%s/reaction/%s.json' % t, 'w') as f:
            json.dump(reaction_scores, f)
        with open('%s/pathway/%s.json' % t, 'w') as f:
            json.dump(pathway_scores, f)
