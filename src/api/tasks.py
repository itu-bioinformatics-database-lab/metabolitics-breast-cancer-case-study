import datetime
import pickle

from preprocessing import DynamicPreprocessing
from .app import celery
from .models import db, Analysis

pathway_scaler = DynamicPreprocessing(['pathway-scoring'])

with open('../models/api_model.p', 'rb') as f:
    reaction_scaler = pickle.load(f)


@celery.task()
def save_analysis(analysis_id, concentration_changes):
    reaction_scores = reaction_scaler.transform(concentration_changes)
    pathway_scores = pathway_scaler.transform(reaction_scores)
    analysis = Analysis.query.get(analysis_id)
    analysis.save_results(reaction_scores, pathway_scores)
    analysis.status = True
    analysis.end_time = datetime.datetime.now()
    db.session.commit()
