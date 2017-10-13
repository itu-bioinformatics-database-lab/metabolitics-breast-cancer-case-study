import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from preprocessing import InverseDictVectorizer

from .cli import cli

from noise import NoiseGenerator
from preprocessing import DynamicPreprocessing
from services import DataReader, DataWriter


@cli.command()
def robustness_test_with_noise():

    X, y = DataReader().read_data('BC')

    for i in np.linspace(0.1, 1, 10):

        vect = DictVectorizer(sparse=False)

        pipe = Pipeline([
            ('naming-scale',
             DynamicPreprocessing(['naming', 'metabolic-standard'])),
            ('vect', vect),
            ('noise', NoiseGenerator(np.random.uniform, (-i, i))),
            ('inv_vect', InverseDictVectorizer(vect)),
            ('fva', DynamicPreprocessing(['fva'])),
        ])

        X_result = pipe.fit_transform(X, y)

        DataWriter('bc_noise#k=%f' % i, gz=True) \
            .write_json_dataset(X_result, y)
