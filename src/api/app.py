from flask import Flask
from flask_restful import Resource, Api
from .resources import StartWithQuery

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):

    def __init__(self):
        pass

    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')
api.add_resource(StartWithQuery, '/search/<query>')
