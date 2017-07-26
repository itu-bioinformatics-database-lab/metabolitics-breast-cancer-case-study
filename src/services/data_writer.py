import json
import gzip
import pickle

import numpy as np


class DataWriter:
    def __init__(self, filename, gz=False):
        self.path = '../outputs/%s.json' % filename
        self.gz = gz

    def write_json(self, data):
        with gzip.open('%s.gz' % self.path, 'wt') if self.gz else open(
                self.path, 'w') as file:
            json.dump(data, file)

    def write_json_dataset(self, X, y):
        self.write_json(list(zip(X, y)))

    def write_json_stream(self, func, X, splits=24):
        with open(self.path, 'w', 1) as file:
            for xs in np.array_split(X, len(X) / splits):
                for x in func(xs):
                    file.write('%s\n' % json.dumps(x))

    def write_json_dataset_stream(self, func, X, y):
        self.write_json_stream(lambda Xy: func([Xy[0]], [Xy[1]]), zip(X, y))
