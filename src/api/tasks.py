import datetime
import pickle

from preprocessing import DynamicPreprocessing
from .app import celery
from .models import db, Analysis

pathway_scaler = DynamicPreprocessing(
    ['pathway-scoring', 'transport-elimination'])

with open('../models/api_model.p', 'rb') as f:
    reaction_scaler = pickle.load(f)


@celery.task()
def save_analysis(analysis_id, concentration_changes):
    analysis = Analysis.query.get(analysis_id)
    results_reaction = reaction_scaler.transform(concentration_changes)
    analysis.results_reaction = analysis.clean_name_tag(results_reaction)
    analysis.results_pathway = analysis.clean_name_tag(
        pathway_scaler.transform(results_reaction))
    analysis.status = True
    analysis.end_time = datetime.datetime.now()
    db.session.commit()
