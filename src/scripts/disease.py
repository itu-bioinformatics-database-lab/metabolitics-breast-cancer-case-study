import pickle
import datetime

from .cli import cli
import pandas as pd

from services import DataReader, DataWriter, NamingService, filter_by_label
from preprocessing import DynamicPreprocessing
from client import MetaboliticsApiClient
from api.models import db, Analysis


@cli.command()
def hmdb_disease_normalization():
    dataset = DataReader().read_hmdb_diseases()
    naming = NamingService('hmdb')
    nor_data = dict()

    for dis, categories in dataset.items():
        for cat, measurements in categories.items():
            named_measurements = naming.to(dict(measurements))
            if len(named_measurements) >= 10:
                nor_data['%s %s' % (dis, cat)] = {
                    k: round(
                        min(v - 1, 100) if v >= 1 else max(1 - v**-1, -100), 3)
                    for k, v in named_measurements.items()
                }
    DataWriter('normalization_hmdb').write_json(nor_data)


@cli.command()
def hmdb_disease_analysis():
    y, X = list(zip(*DataReader().read_hmdb_diseases().items()))
    X_t = DynamicPreprocessing(['fva']).fit_transform(X, y)
    DataWriter('hmdb_disease_analysis').write_json(dict(zip(y, X_t)))


@cli.command()
def hmdb_disease_analysis_pathway_level():
    X, y = DataReader().read_solution('hmdb_disease_analysis')

    with open('../models/api_model.p', 'rb') as f:
        reaction_scaler = pickle.load(f)

    dyn_pre = DynamicPreprocessing(
        ['pathway-scoring', 'transport-elimination'])

    X_t = reaction_scaler._model.named_steps['flux-diff'].transform(X)
    X_t = dyn_pre.fit_transform(X_t, y)
    DataWriter('hmdb_disease_analysis_pathway_level').write_json(
        dict(zip(y, X_t)))


@cli.command()
def hmdb_disease_analysis_on_server():
    client = MetaboliticsApiClient()
    client.login('email', 'password')

    hmdb_data = DataReader().read_hmdb_diseases()

    for name, measurements in hmdb_data.items():
        print(client.analyze(name, measurements))


@cli.command()
def save_to_server():
    X_hcc, y_hcc = DataReader().read_analyze_solution(
        'bc_averaging_disease_analysis#k=0')

    df_without_h = lambda X, y: pd.DataFrame.from_records(
        filter_by_label(X, y, 'h', reverse=True)[0])

    df_reaction = df_without_h(X_hcc, y_hcc)

    reaction_mean = df_reaction[list(
        filter(lambda x: not x.endswith('ave'),
               df_reaction.columns))].mean().to_dict()

    pathway_scaler = DynamicPreprocessing(
        ['pathway-scoring', 'transport-elimination'])

    pathways_mean = df_without_h(
        pathway_scaler.fit_transform(X_hcc, y_hcc), y_hcc).mean().to_dict()

    analysis = Analysis('Breast Cancer', None)
    analysis.status = True
    analysis.type = 'disease'
    analysis.start_time = datetime.datetime.now()
    analysis.end_time = datetime.datetime.now()
    analysis.results_reaction = analysis.clean_name_tag([reaction_mean])
    analysis.results_pathway = analysis.clean_name_tag([pathways_mean])
    db.session.add(analysis)
    db.session.commit()


@cli.command()
def save_hmdb_to_server():

    hmdb = DataReader().read_solution('hmdb_averaging_disease_analysis')

    df = pd.DataFrame.from_records(list(hmdb[0]))

    hmdb[0] = df[list(filter(lambda x: not x.endswith('ave'),
                             df.columns))].T.to_dict().values()

    pathway_scaler = DynamicPreprocessing(
        ['pathway-scoring', 'transport-elimination'])

    for x, l in zip(*hmdb):
        if 'Saliva' not in l:
            analysis = Analysis(l.title(), None)
            analysis.status = True
            analysis.type = 'disease'
            analysis.start_time = datetime.datetime.now()
            analysis.end_time = datetime.datetime.now()
            analysis.results_reaction = analysis.clean_name_tag([x])
            analysis.results_pathway = analysis.clean_name_tag(
                pathway_scaler.fit_transform([x], [l]))
            db.session.add(analysis)
            db.session.commit()


@cli.command()
def average_metabolite_data():
    scaler = DynamicPreprocessing(['naming'])
    X, y = DataReader().read_data('HCC')

    df = pd.DataFrame.from_records(
        filter_by_label(scaler.fit_transform(X, y), y, 'h', reverse=True)[0])

    DataWriter('hcc_metabolite_concentration_changes').write_json(
        df.mean().to_dict())
