import uuid
import datetime
import json

from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import JSON
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
    public = db.Column(db.Boolean)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    results_pathway = db.Column(JSON)
    results_reaction = db.Column(JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="analysis")

    def __init__(self, name, user, status=False, public=False):
        self.name = name
        self.status = status
        self.public = public
        self.start_time = datetime.datetime.now()
        self.user = user

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

    def __repr__(self):
        return '<Analysis %r>' % self.name
