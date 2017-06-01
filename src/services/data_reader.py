import os
import json

import cobra as cb
import pandas as pd
from cobra.core import Model, DictList, Reaction, Metabolite


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

    def read_healthy(self, disease_name):
        return list(
            zip(*filter(lambda y: y[1] == 'h',
                        zip(*DataReader().read_data(disease_name)))))

    def read_columns(self, disease_name):
        return pd.read_csv(
            '%s/%s.csv' % (self.path, disease_name), header=0).columns

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

    def read_fva_solutions(self, file_name='fva.cobra.txt'):
        path = '../dataset/solutions/%s' % file_name
        with open(path) as f:
            (X, y) = zip(*map(lambda x: (eval(x[1].strip()), x[0]),
                              [l.split(" ", 1) for l in f]))
            return (X, y)

    def read_solutions(self):
        path = '../dataset/solutions/solution_for_dataset.json'
        with open(path) as f:
            X = [json.loads(l) for l in f]
            y = self.read_all()[1]
            return (X, y)

    def read_categorical_solutions(self):
        raise NotImplemented()

    def read_network_model(self, name='recon2'):
        return cb.io.load_json_model('../dataset/network/%s.json' % name)

    def read_subsystem_categories(self, name='recon'):
        path = '../dataset/subsystem-categories/%s.json' % name
        with open(path) as f:
            return {k: set(v) for k, v in json.load(f).items()}

    def create_example_model(self):
        model = Model('example_model')

        rs = (r1, r2, r3) = (Reaction('R1'), Reaction('R2'), Reaction('R3'))
        for r in rs:
            r.lower_bound = 0.
            r.upper_bound = 1000.
            r.objective_coefficient = 0.

        ACP_c = Metabolite(
            'ACP_c',
            formula='C11H21N2O7PRS',
            name='acyl-carrier-protein',
            compartment='c')

        r1.add_metabolites({ACP_c: 1.0})
        r2.add_metabolites({ACP_c: 1.0})
        r3.add_metabolites({ACP_c: -1.0})

        model.add_reactions(rs)

        return model

    def read_hmdb_diseases(self):
        path = '%s/hmdb_disease_measurements.json' % self.path
        with open(path) as f:
            return json.load(f)
