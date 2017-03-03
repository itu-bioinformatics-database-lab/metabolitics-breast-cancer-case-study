from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow

from .app import app
from .models import User, Analysis

ma = Marshmallow(app)


class AnalysisInputSchema(Schema):
    name = fields.String(required=True)
    concentration_changes = fields.Dict(required=True)


class PasswordChangeSchema(Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True)


class UserSchema(ma.ModelSchema):
    name = fields.String(required=True)
    surname = fields.String(required=True)
    email = fields.Email(required=True)
    affiliation = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

    class Meta:
        model = User
        exclude = ('analysis',)


class AnalysisSchema(ma.ModelSchema):
    result = fields.Dict()

    class Meta:
        model = Analysis
        exclude = ('user',)
