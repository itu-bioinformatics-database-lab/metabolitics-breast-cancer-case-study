import pickle

from services import DataReader, DataWriter, NamingService
from .cli import cli
from preprocessing import DynamicPreprocessing
from client import MetaboliticsApiClient


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
    naming = NamingService('recon')

    y, X = list(zip(*DataReader().read_hmdb_diseases().items()))

    dyn_pre = DynamicPreprocessing(['fva'])

    X_t = dyn_pre.fit_transform(X, y)
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
