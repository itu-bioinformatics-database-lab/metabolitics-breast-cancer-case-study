import uuid
import datetime
import json

from sqlalchemy import and_, or_
from sqlalchemy.types import Float
from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy, BaseQuery
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

    class AnalysisQuery(BaseQuery):
        def get_pathway_score(self, pathway):
            return Analysis.results_pathway[0][pathway].astext.cast(Float)

        def filter_by_change(self, pathway, change):
            score = self.get_pathway_score(pathway)
            return self.filter(score > 0 if change >= 0 else score < 0)

        def for_many(self, iterable, func):
            f = self
            for i in iterable:
                f = func(i)
            return f

        def filter_by_change_many(self, data):
            return self.for_many(
                data,
                lambda x: self.filter_by_change(x['pathway'], x['change']))

        def filter_by_change_amount(self, pathway, qualifier, amount):
            if not (qualifier and amount):
                return self

            score = self.get_pathway_score(pathway)
            if qualifier == 'lt':
                return self.filter(amount >= score)
            elif qualifier == 'gt':
                return self.filter(score >= amount)
            elif qualifier == 'eq':
                return self.filter(
                    or_(score + 10 >= amount, score - 10 <= amount))
            else:
                raise ValueError(
                    'qualifier should be lt, gt or eq but not %s ' % qualifier)

        def filter_by_change_amount_many(self, data):
            return self.for_many(
                data,
                lambda x: self.filter_by_change_amount(x['pathway'], x['qualifier'], x['amount'])
            )

    query_class = AnalysisQuery

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

    def authenticated(self):
        return (self.type in ['private', 'noise'] and
                self.user_id != current_identity.id)

    @staticmethod
    def get_multiple(ids):
        return Analysis.query.filter(
            and_(
                Analysis.id.in_(ids),
                Analysis.user.has(id=current_identity.id)))

    def __repr__(self):
        return '<Analysis %r>' % self.name
