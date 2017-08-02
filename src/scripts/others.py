from collections import defaultdict
import json

from .cli import cli

import click
import cobra as cb
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import f_classif, VarianceThreshold, SelectKBest

from services import DataReader, NamingService, DataWriter
from preprocessing import DynamicPreprocessing, FVARangedMeasurement, PathwayFvaScaler, InverseDictVectorizer
from classifiers import FVADiseaseClassifier
from .optimal_currency_threshold import optimal_currency_threshold


@cli.command()
def threshold_optimization():
    model = cb.io.load_json_model('../dataset/network/recon-model.json')
    print(optimal_currency_threshold(model, (2, 100)))


@cli.command()
def metabolite_by_connected_subsystems():
    model = cb.io.load_json_model('../dataset/network/recon-model.json')
    metabolites = [(len(set([j.subsystem for j in i.reactions])), i.id)
                   for i in model.metabolites]
    print(sorted(metabolites, key=lambda x: x[0], reverse=True))


@cli.command()
def subsystem_statistics():
    categories = DataReader().read_subsystem_categories()
    total = 0
    for k, v in categories.items():
        print(k, len(v))
        total += len(v)
    print('total:', total)


@cli.command()
def fva_range_analysis_save():
    # (X, y) = DataReader().read_data('BC')
    (X, y) = DataReader().read_data('HCC')
    
    dy_pre = DynamicPreprocessing(['naming', 'basic-fold-change-scaler', 'fva'])   
    X_pre = dy_pre.fit_transform(X, y)

    DataWriter('hcc_averaging', gz=True).write_json_dataset(X_pre, y)


@cli.command()
@click.argument('top_num_reaction')
def most_correlated_reactions(top_num_reaction):
    (X, y) = DataReader().read_fva_solutions()
    vect = DictVectorizer(sparse=False)
    X = vect.fit_transform(X)
    vt = VarianceThreshold(0.1)
    X = vt.fit_transform(X)
    (F, pval) = f_classif(X, y)

    feature_names = np.array(vect.feature_names_)[vt.get_support()]
    top_n = sorted(
        zip(feature_names, F), key=lambda x: x[1],
        reverse=True)[:int(top_num_reaction)]
    model = DataReader().read_network_model()
    for n, v in top_n:
        print('name:', n[:-4])
        print('reaction:', model.reactions.get_by_id(n[:-4]).reaction)
        print('min-max:', n[-3:])
        print('F:', v)
        print('-' * 10)


@cli.command()
@click.argument('top_num_pathway')
@click.argument('num_of_reactions')
def most_correlated_pathway(top_num_pathway, num_of_reactions):
    (X, y) = DataReader().read_fva_solutions('fva_without.transports.txt')

    vect = [DictVectorizer(sparse=False)] * 3
    vt = VarianceThreshold(0.1)
    skb = SelectKBest(k=int(num_of_reactions))
    X = Pipeline([('vect1', vect[0]), ('vt',
                                       vt), ('inv_vec1', InverseDictVectorizer(
                                           vect[0], vt)), ('vect2', vect[1]),
                  ('skb', skb), ('inv_vec2', InverseDictVectorizer(
                      vect[1], skb)), ('pathway_scoring', PathwayFvaScaler()),
                  ('vect3', vect[2])]).fit_transform(X, y)

    (F, pval) = f_classif(X, y)

    top_n = sorted(
        zip(vect[2].feature_names_, F, pval), key=lambda x: x[1],
        reverse=True)[:int(top_num_pathway)]

    model = DataReader().read_network_model()
    X, y = DataReader().read_data('BC')
    bc = NamingService('recon').to(X)

    subsystem_metabolite = defaultdict(set)
    for r in model.reactions:
        subsystem_metabolite[r.subsystem].update(m.id for m in r.metabolites)

    subsystem_counts = defaultdict(float)
    for sample in bc:
        for s, v in subsystem_metabolite.items():
            subsystem_counts[s] += len(v.intersection(sample.keys()))

    subsystem_counts = {
        i: v / len(subsystem_counts)
        for i, v in subsystem_counts.items()
    }

    for n, v, p in top_n:
        print('name:', n[:-4])
        print('min-max:', n[-3:])
        print('metabolites:%s' % subsystem_counts[n[:-4]])
        print('F:', v)
        print('p:', p)
        print('-' * 10)
