import json
import pickle


class DataWriter:
    def __init__(self, filename):
        self.path = '../outputs/%s.json' % filename

    def write_json(self, data):
        json.dump(data, open(self.path, 'w'))

    def write_json_dataset(self, X, y):
        self.write_json(list(zip(X, y)))
