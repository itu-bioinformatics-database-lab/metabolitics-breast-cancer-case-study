import os
import json

import cobra as cb
import pandas as pd


class DataReader(object):

    def __init__(self):
        self.path = '../dataset/disease'
        self.y_label = 'stage'

    def read_data(self, disease_name):
        df = pd.read_csv('%s/%s.csv' % (self.path, disease_name), header=0)
        X = df.ix[:, df.columns != self.y_label].to_dict('records')
        y = df[self.y_label].values
        y = ['h' if i == 'h' else disease_name.lower() for i in y]
        return (X, y)

    def read_columns(self, disease_name):
        return pd.read_csv('%s/%s.csv' % (self.path, disease_name),
                           header=0).columns

    def read_all(self):
        disease_names = [f[:-4] for f in os.listdir(self.path)]
        (X, y) = (list(), list())
        for i in disease_names:
            (tX, ty) = self.read_data(i)
            X += tX
            y += ty
        return (X, y)

    def read_avg_data(self):
        raise NotImplementedError()

    def read_small_data(self):
        self.path = '../dataset/small-disease'
        return self.read_all()

    def read_solutions(self):
        path = '../dataset/solutions/solution_for_dataset.json'
        with open(path) as f:
            X = [json.loads(l) for l in f]
            y = self.read_all()[1]
            return (X, y)

    def read_categorical_solutions(self):
        raise NotImplemented()

    def read_network_model(self, name='recon-model'):
        return cb.io.load_json_model('../dataset/network/%s.json' % name)

    def read_subsystem_categories(self, name='recon'):
        path = '../dataset/subsystem-categories/%s.json' % name
        with open(path) as f:
            return {k: set(v) for k, v in json.load(f).items()}

    # def read_measured_metabolites_formated(self, name='recon'):
    #     '''Read measured metabolites metablites named and stadart scaled'''
    #     (X, y) = DataReader().read_all()
    #     vect = DictVectorizer(sparse=False)
    #     X = vect.fit_transform(X, y)
    #     X = MetabolicStandardScaler().fit_transform(X, y)
    #     X = vect.inverse_transform(X)
    #     X = NamingService('recon').to(X)
    #     return (X, y)
