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
    analysis = db.relationship(
        "Analysis", back_populates="user", lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.email


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    status = db.Column(db.Boolean)
    type = db.Column(db.String(255))
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    results_pathway = db.Column(JSON)
    results_reaction = db.Column(JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="analysis")

    def __init__(self, name, user, status=False, type='private'):
        self.name = name
        self.status = status
        self.type = type
        self.start_time = datetime.datetime.now()
        self.user = user

    def clean_name_tag(self, dataset):
        cleaned_dataset = list()
        for d in dataset:
            cleaned_dataset.append({k[:-4]: v for k, v in d.items()})
        return cleaned_dataset

    @staticmethod
    def get_multiple(ids):
        return Analysis.query.filter(
            and_(
                Analysis.id.in_(ids),
                Analysis.user.has(id=current_identity.id)))

    def __repr__(self):
        return '<Analysis %r>' % self.name
