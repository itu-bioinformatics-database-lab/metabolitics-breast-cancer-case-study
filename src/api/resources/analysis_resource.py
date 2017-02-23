from flask_restful import reqparse
from .base_resource import BaseResource
from ..tasks import save_analysis


class FVAAnalysis(BaseResource):

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name')
        self.parser.add_argument('concentration-changes', type=dict)

    def post(self):
        data = self.parser.parse_args()
        save_analysis.delay(data['name'], data['concentration-changes'])
        return '', 202
