import numpy as np
import numpy.random as npr
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

from services import DataReader
from preprocessing import FVAScaler, ReactionDiffScaler

from .cli import cli


@cli.command()
def hypothetical_ecoli():

    model = DataReader().read_network_model('e_coli_core')
    metabolite_ids = list(map(lambda x: x.id, model.metabolites))

    X = [
        dict(zip(metabolite_ids, npr.randn(len(metabolite_ids))))
        for x in range(2)
    ]
    y = ['h', 'else']
    df = pd.DataFrame(X).T
    df.columns = y
    df.to_csv('../outputs/hypothetical_ecoli_input.csv')

    vect = DictVectorizer(sparse=False)
    pipe = Pipeline([
        ('vect', vect),
        ('fva', FVAScaler(vectorizer=vect, dataset_name='e_coli_core')),
        ('diff-scaler', ReactionDiffScaler(dataset_name='e_coli_core')),
    ])

    X_results = pipe.fit_transform(X, y)
    df = pd.DataFrame(X_results).T
    df.columns = y
    df.to_csv('../outputs/hypothetical_ecoli_output.csv')
