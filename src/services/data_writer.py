import json
import pickle


class DataWriter:
    def __init__(self):
        self.path = '../outputs'

    def write_json(self, data, file_name):
        json.dump(data, open('../outputs/%s' % file_name, 'w'))
