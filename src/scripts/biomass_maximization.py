from cameo import fba

from services import DataReader, DataWriter
from analysis import BasePathwayModel
from preprocessing import DynamicPreprocessing

from .cli import cli


@cli.command()
def biomass_maximization():

    X, y = DataReader().read_data('BC')
    pipe = DynamicPreprocessing(['naming', 'metabolic-standard'])

    X_t = pipe.fit_transform(X, y)

    model = BasePathwayModel.create_for()

    X_results = list()

    for i, x in enumerate(X_t):
        m = model.copy()
        m.objective.direction = 'max'
        m.set_objective_coefficients(x)
        m.fix_objective_as_constraint()
        m.clean_objective()
        r = m.reactions.get_by_id('biomass_reaction')
        r.objective_coefficient = 1

        X_results.append(dict(fba(m).data_frame.itertuples()))

    DataWriter('biomass_maximization_fba_results') \
        .write_json_dataset(X_results, y)
