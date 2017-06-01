from services import DataReader, DataWriter, NamingService
from .cli import cli
from preprocessing import DynamicPreprocessing


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
                    k: (v if v >= 1 else -v**-1)
                    for k, v in named_measurements.items()
                }
    DataWriter().write_json(nor_data, 'normalization_hmdb.json')


@cli.command()
def hmdb_disease_analysis():
    y_hmdb, X_hmdb = list(zip(*DataReader().read_hmdb_diseases().items()))
    X_bch, y_bch = DataReader().read_healthy('BC')
    X, y = X_hmdb + X_bch, y_hmdb + y_bch

    dyn_pre = DynamicPreprocessing(
        ['fva', 'flux-diff', 'pathway-scoring', 'transport-elimination'])

    X_t = dyn_pre.fit_transform(X, y)
    DataWriter().write_json(dict(zip(y, X_t)), 'hmdb_disease_analysis.json')
