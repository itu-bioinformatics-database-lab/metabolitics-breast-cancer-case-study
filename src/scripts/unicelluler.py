import math
from functools import reduce

from functional import seq
import pandas as pd
import cobra as cb
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

from services import DataWriter
from preprocessing import FVAScaler, NameMatching, DynamicPreprocessing, ReactionDiffScaler
from .cli import cli


@cli.command()
def generate_unicelluler_network():
    df_flux = pd.DataFrame.from_csv(
        '../dataset/unicelluler/unicelluler_flux.csv')
    df_metabolite_names = pd.DataFrame.from_csv(
        '../dataset/unicelluler/unicelluler_metabolite_names.csv')

    model = cb.Model('unicelluler')

    model.add_metabolites(
        cb.Metabolite(id=row['id'], name=row['name'])
        for _, row in df_metabolite_names.iterrows())

    for i in df_flux.index:
        r = cb.Reaction(i.replace(' ', ''))
        model.add_reaction(r)

        black_list = ['(Cell synthesis)', '(Evolution)', 'Exch. (', ')']
        r.reaction = reduce(lambda x, y: x.replace(y, ''), black_list,
                            i.replace('->', '-->'))

    cb.io.save_json_model(model, '../outputs/unicelluler.json')


@cli.command()
def name_matching_unicelluler():
    df_metabolite_names = pd.DataFrame.from_csv(
        '../dataset/unicelluler/unicelluler_metabolite_names.csv')
    df_metabolites = pd.DataFrame.from_csv(
        '../dataset/unicelluler/unicelluler_metabolites.csv')

    network_names = set(df_metabolite_names['name'])
    dataset_names = set(map(lambda x: x.lower().strip(), df_metabolites.index))

    print('%d of %d matcthed correclty' %
          (len(network_names.intersection(dataset_names)), len(network_names)))
    print('Following metabolites do not mapped:')
    for i in network_names - dataset_names:
        print('\t', '-', i)

    name_id_mapping = df_metabolite_names.set_index('name').to_dict()['id']
    name_id_mapping = {k: [v] for k, v in name_id_mapping.items()}
    DataWriter('unicelluler-mapping').write_json(name_id_mapping)
    print()
    print('Unicelluler mapping file created')


@cli.command()
def analysis_unicelluler():
    df_metabolites = pd.DataFrame.from_csv(
        '../dataset/unicelluler/unicelluler_metabolites.csv')

    y, X = list(zip(*df_metabolites.to_dict().items()))
    X = [{k: v for k, v in x.items() if not math.isnan(v)} for x in X]
    y = ['h' if i.startswith('RF') else i for i in y]

    # Features which are not owned by healthy samples is eliminated 
    healthy_features = seq(X).zip(y).filter(lambda x: x[1] == 'h').map(
        lambda x: x[0].keys()).flatten().to_set()
    X = [{k: v for k, v in x.items() if k in healthy_features} for x in X]

    # TOTHINK: Low featured sample can be elimated in here 

    dataset_name = 'unicelluler'
    vect = DictVectorizer(sparse=False)
    pipe = Pipeline([
        # unicelluler analysis pipeline
        ('naming', NameMatching(dataset_name)),
        ('scaler', DynamicPreprocessing(['metabolic-standard'])),
        ('vect', vect),
        ('fva', FVAScaler(vectorizer=vect, dataset_name=dataset_name)),
        ('flux-diff', ReactionDiffScaler(dataset_name=dataset_name))
    ])

    X_t = pipe.fit_transform(X, y)
    DataWriter('unicelluler_analysis').write_json_dataset(X, y)
