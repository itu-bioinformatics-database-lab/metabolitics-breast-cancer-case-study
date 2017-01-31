from sklearn.feature_extraction import DictVectorizer

from analysis import FGSubsystemFBA
from services import DataReader, NamingService
from preprocessing import MetabolicChangeScaler


def run_fg_subsystem_fba():
    model = DataReader().read_network_model('recon-model')

    (X, y) = DataReader().read_all()

    vect = DictVectorizer(sparse=False)
    X = vect.fit_transform(X, y)
    X = MetabolicChangeScaler().fit_transform(X, y)

    # ecolin_measured_metabolites = {'etoh_e': 1, 'gln__L_c': 1}

    X = vect.inverse_transform(X)
    measured_metabolites = NamingService('recon').to(X[0])

    analysis = FGSubsystemFBA(model)

    analysis.analyze_and_save_to_file(
        measured_metabolites, 'recon-model.fg_subsystem_fba.txt')
