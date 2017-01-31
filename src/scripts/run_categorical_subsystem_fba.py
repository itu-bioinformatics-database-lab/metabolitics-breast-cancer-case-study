from sklearn.feature_extraction import DictVectorizer

from analysis import CategoricalSubsystemFBA
from services import DataReader, NamingService
from preprocessing import MetabolicChangeScaler


def run_categorical_subsystem_fba():
    model = DataReader().read_network_model('recon-model')

    (X, y) = DataReader().read_all()

    vect = DictVectorizer(sparse=False)
    X = vect.fit_transform(X, y)
    X = MetabolicChangeScaler().fit_transform(X, y)
    X = vect.inverse_transform(X)

    measured_metabolites = NamingService('recon').to(X[0])

    analysis = CategoricalSubsystemFBA(model)

    analysis.analyze_and_save_to_file(
        measured_metabolites, 'recon-model.icategorical_subsystem_fba.txt')
