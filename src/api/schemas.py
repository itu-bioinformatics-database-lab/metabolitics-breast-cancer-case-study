from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow

from .app import app
from .models import User

ma = Marshmallow(app)


class AnalysisSchema(Schema):
    name = fields.String(required=True)
    concentration_changes = fields.Dict(required=True)


class SignUpSchema(ma.ModelSchema):
    name = fields.String(required=True)
    surname = fields.String(required=True)
    email = fields.String(required=True)
    affiliation = fields.String(required=True)
    password = fields.String(required=True)

    class Meta:
        model = User
