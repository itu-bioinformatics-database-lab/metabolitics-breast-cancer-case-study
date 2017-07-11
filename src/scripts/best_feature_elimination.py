import logging
import json

from .cli import cli

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold

from services import DataReader, NamingService, DataWriter
from preprocessing import DynamicPreprocessing, InverseDictVectorizer
from classifiers import FVADiseaseClassifier
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


@cli.command()
def elimination_tabular():
    (X, y) = DataReader().read_data('BC')

    datasets = {'metabolite': DataReader().read_data('BC')}
    scores = list()

    for i in range(1, len(X[0].keys()) + 1, 10):

        vect = DictVectorizer(sparse=False)
        selector = SelectNotKBest(k=i)

        clfs = dict()

        clfs['metabolite'] = Pipeline([
            # pipe for compare model with eliminating some features
            ('metabolic',
             DynamicPreprocessing(['naming', 'metabolic-standard'])),
            ('vect', vect),
            ('selector', selector),
            ('pca', PCA()),
            ('clf', LogisticRegression(C=0.01, random_state=43))
        ])

        try:
            path = '../dataset/solutions/bc_disease_analysis#k=%d.json' % i
            datasets['reaction'] = list(
                zip(*[json.loads(i) for i in open(path)][0]))
        except:
            print(pd.DataFrame(scores))
            return

        clfs['reaction'] = FVADiseaseClassifier()

        kf = StratifiedKFold(n_splits=10, random_state=43)

        score = {
            name: np.mean(
                cross_val_score(
                    clf,
                    datasets[name][0],
                    datasets[name][1],
                    cv=kf,
                    n_jobs=-1,
                    scoring='f1_micro'))
            for name, clf in clfs.items()
        }
        score['iteration'] = i
        scores.append(score)

    print(pd.DataFrame(scores))
