import logging

from .cli import cli

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from services import DataReader, NamingService, DataWriter
from preprocessing import DynamicPreprocessing, InverseDictVectorizer
from noise import SelectNotKBest


@cli.command()
def eliminate_best_k():
    (X, y) = DataReader().read_data('BC')

    for i in range(1, len(X[0].keys()) + 1, 10):

        vect = DictVectorizer(sparse=False)
        selector = SelectNotKBest(k=i)

        pipe = Pipeline([
            # pipe for compare model with eliminating some features
            ('metabolic',
             DynamicPreprocessing(['naming', 'metabolic-standard'])),
            ('vect', vect),
            ('selector', selector),
            ('inv_vect', InverseDictVectorizer(vect, selector)),
            ('fva', DynamicPreprocessing(['fva']))
        ])

        X_result = pipe.fit_transform(X, y)

        DataWriter('bc_disease_analysis#k=%s' % i) \
            .write_json_dataset(X_result, y)
