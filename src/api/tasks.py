import datetime
import pickle

from preprocessing import DynamicPreprocessing
from .app import celery
from .models import db, Analysis


@celery.task()
def save_analysis(analysis_id, concentration_changes):

    with open('../models/api_model.p', 'rb') as f:
        reaction_scaler = pickle.load(f)

    pathway_scaler = DynamicPreprocessing(
        ['pathway-scoring', 'transport-elimination'])

    results_reaction = reaction_scaler.transform(concentration_changes)
    results_pathway = pathway_scaler.transform(results_reaction)

    analysis = Analysis.query.get(analysis_id)
    analysis.results_reaction = analysis.clean_name_tag(results_reaction)
    analysis.results_pathway = analysis.clean_name_tag(results_pathway)
    analysis.status = True
    analysis.end_time = datetime.datetime.now()
    db.session.commit()
