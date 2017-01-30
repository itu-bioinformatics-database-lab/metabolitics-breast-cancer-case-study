from flask_restful import Resource
from services import DataReader


_model = DataReader().read_network_model()


class BaseResource(Resource):

    def __init__(self):
        self._model = _model
