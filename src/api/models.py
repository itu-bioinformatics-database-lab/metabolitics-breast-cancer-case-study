import uuid
import datetime
import json

from sqlalchemy import and_
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import jwt_required, current_identity

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
        with open('%s/reaction-%s.json' % t) as f:
            self.results['reaction'] = json.load(f)
        with open('%s/pathway-%s.json' % t) as f:
            self.results['pathway'] = json.load(f)

    def save_results(self, reaction_scores, pathway_scores):
        t = (self._path, self.filename)
        with open('%s/reaction-%s.json' % t, 'w') as f:
            json.dump(list(self.clean_name_tag(reaction_scores)), f)
        with open('%s/pathway-%s.json' % t, 'w') as f:
            json.dump(list(self.clean_name_tag(pathway_scores)), f)

    def clean_name_tag(self, dataset):
        for d in dataset:
            yield {k[:-4]: v for k, v in d.items()}

    @staticmethod
    def get_multiple(ids):
        analyses = list(
            Analysis.query.filter(
                and_(
                    Analysis.id.in_(ids),
                    Analysis.user.has(id=current_identity.id))))

        for i in analyses:
            i.load_results()

        return analyses
