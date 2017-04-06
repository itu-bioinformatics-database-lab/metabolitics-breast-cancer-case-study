import json
import numpy as np


class NamingService(object):

    def __init__(self, name):
        self._names = self._read(name)

    def _read(self, name: str):
        with open('../dataset/naming/%s-mapping.json' % name) as f:
            self._names = json.load(f)
        return {k.lower().strip(): v[0] for k, v in self._names.items() if v}

    def to(self, data):
        if type(data) == str:
            return self._names.get(data.lower().strip())
        elif type(data) == dict:
            return {self.to(k): v for k, v in data.items() if self.to(k)}
        elif type(data) == list or type(data) == np.ndarray:
            return [self.to(i) for i in data]
        else:
            raise ValueError(
                'data should be str, dict or list but not %s' % type(data))
