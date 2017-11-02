import numpy as np
import numpy.random as npr
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
import matplotlib.pyplot as plt

from noise import NoiseGenerator
from preprocessing import DynamicPreprocessing, InverseDictVectorizer, FVAScaler
from services import DataReader, DataWriter

from .cli import cli


@cli.command()
def stability_test_for_recon():

    X, y = DataReader().read_data('BC')

    for i in np.linspace(0.1, 1, 10) + 1:

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

        noise_size = pipe.named_steps['noise'].relative_noise_size_

        DataWriter('bc_noise#k=%f' % noise_size, gz=True) \
            .write_json_dataset(X_result, y)


@cli.command()
def stability_test_for_ecoli():

    model = DataReader().read_network_model('e_coli_core')
    metabolite_ids = list(map(lambda x: x.id, model.metabolites))

    X = [
        dict(zip(metabolite_ids, npr.randn(len(metabolite_ids))))
        for _ in range(100)
    ]
    y = np.random.randint(2, size=len(metabolite_ids))

    vect = DictVectorizer(sparse=False)
    pipe = Pipeline([
        ('vect', vect),
        ('fva', FVAScaler(vectorizer=vect, dataset_name='e_coli_core')),
        ('re-vect', vect),
    ])

    X_ref = pipe.fit_transform(X, y)

    xs = list()
    ys = list()

    for i in np.linspace(0.1, 1, 10):
        xss = list()
        yss = list()

        for _ in range(100):
            vect = DictVectorizer(sparse=False)
            pipe = Pipeline([
                ('vect', vect),
                ('noise', NoiseGenerator(np.random.uniform, (-i, i))),
                ('inv_vect', InverseDictVectorizer(vect)),
                ('vect2', vect),
                ('fva', FVAScaler(vectorizer=vect,
                                  dataset_name='e_coli_core')),
                ('revec', vect),
            ])

            X_result = pipe.fit_transform(X, y)
            noise_size = pipe.named_steps['noise'].relative_noise_size_

            noise_fva_size = pipe.named_steps['noise'] \
                                 .relative_noise_size(X_result, X_ref)

            xss.append(noise_size)
            yss.append(noise_fva_size)

        xs.append(np.mean(xss))
        ys.append(np.mean(yss))

        print(xs)
        print(ys)
        print()

    plt.plot(xs, ys)
    plt.show()
