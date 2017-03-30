from collections import defaultdict

from .cli import cli
from preprocessing import DynamicPreprocessing
from services import DataReader

import rpy2.robjects as robj
from rpy2.robjects.packages import importr
import pandas as pd


@cli.command()
def pathifier():
    model = DataReader().read_network_model()
    X, y = DataReader().read_data('BC')
    pre = DynamicPreprocessing(['metabolic-standard'])

    X = pre.fit_transform(X, y)

    df = pd.DataFrame(X)
    metabolite_fold_changes = robj.r.matrix(
        robj.FloatVector(df.as_matrix().T.ravel().tolist()),
        nrow=df.shape[1])
    all_metabolite_ids = robj.StrVector(list(df))

    subsystem_metabolite = defaultdict(set)
    for r in model.reactions:
        subsystem_metabolite[r.subsystem].update(
            m.id for m in r.metabolites if m.id in df)

    pathway_names, pathway_metabolites = zip(*filter(
        lambda x: x[1], subsystem_metabolite.items()))

    pathway_metabolites = robj.r['list'](*map(
        lambda x: robj.StrVector(list(x)), pathway_metabolites))

    pathway_names = robj.StrVector(list(pathway_names))
    is_healthy = robj.BoolVector(list(map(lambda x: x == 'h', y)))

    pathifier = importr("pathifier")

    result = pathifier.quantify_pathways_deregulation(metabolite_fold_changes,
                                                      all_metabolite_ids,
                                                      pathway_metabolites,
                                                      pathway_names,
                                                      is_healthy, attempts=100,
                                                      min_exp=0, min_std=0)

    regScores = dict()
    for pathway, scores in dict(result.items())['scores'].items():
        regScores[pathway] = list(scores[:])

    regScores
