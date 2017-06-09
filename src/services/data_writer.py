import json
import pickle

import numpy as np


class DataWriter:
    def __init__(self, filename):
        self.path = '../outputs/%s.json' % filename
        self.file = open(self.path, 'w', 1)

    def write_json(self, data):
        json.dump(data, self.file)

    def write_json_dataset(self, X, y):
        self.write_json(list(zip(X, y)))

    def write_json_stream(self, func, X, splits=24):
        for xs in np.array_split(X, splits):
            for x in func(xs):
                self.file.write('%s\n' % json.dumps(x))

    def write_json_dataset_stream(self, func, X, y):
        self.write_json_stream(lambda Xy: func([Xy[0]], [Xy[1]]), zip(X, y))
