from collections import defaultdict

import click
import pandas as pd
import rpy2.robjects as robj
from rpy2.robjects.packages import importr
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from .cli import cli
from services import DataReader, DataWriter
from preprocessing import DynamicPreprocessing, InverseDictVectorizer
from noise import SelectNotKBest


@cli.command()
@click.argument('disease_name')
def pathifier(disease_name):
    model = DataReader().read_network_model()
    X, y = DataReader().read_data(disease_name)

    for i in range(0, 100, 10):
        vect = DictVectorizer(sparse=False)
        selector = SelectNotKBest(k=i)

        pre = Pipeline([
            # pipe for compare model with eliminating some features
            ('metabolic',
             DynamicPreprocessing(['naming', 'basic-fold-change-scaler'])),
            ('vect', vect),
            ('selector', selector),
            ('inv_vect', InverseDictVectorizer(vect, selector))
        ])

        X_pre = pre.fit_transform(X, y)
        df = pd.DataFrame(X_pre)

        metabolite_fold_changes = robj.r.matrix(
            robj.FloatVector(df.as_matrix().T.ravel().tolist()),
            nrow=df.shape[1])

        all_metabolite_ids = robj.StrVector(list(df))

        subsystem_metabolite = defaultdict(set)
        for r in model.reactions:
            if r.subsystem and not (r.subsystem.startswith('Transport') or
                                    r.subsystem.startswith('Exchange')):
                subsystem_metabolite[r.subsystem] \
                    .update(m.id for m in r.metabolites if m.id in df)

        pathway_names, pathway_metabolites = zip(*filter(
            lambda x: x[1], subsystem_metabolite.items()))

        pathway_metabolites = robj.r['list'](*map(
            lambda x: robj.StrVector(list(x)), pathway_metabolites))

        pathway_names = robj.StrVector(list(pathway_names))
        is_healthy = robj.BoolVector(list(map(lambda x: x == 'h', y)))

        pathifier = importr("pathifier")

        result = pathifier.quantify_pathways_deregulation(
            metabolite_fold_changes,
            all_metabolite_ids,
            pathway_metabolites,
            pathway_names,
            is_healthy,
            attempts=100,
            min_exp=-10,
            min_std=0)

        regScores = dict()
        for pathway, scores in dict(result.items())['scores'].items():
            regScores[pathway] = list(scores[:])

        X_regs = list(pd.DataFrame(regScores).T.to_dict().values())

        DataWriter('bc_pathifier_analysis#k=%s' % i, gz=True) \
            .write_json_dataset(X_regs, y)
