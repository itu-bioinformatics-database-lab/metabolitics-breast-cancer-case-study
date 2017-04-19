import datetime
import pickle

from preprocessing import DynamicPreprocessing
from .app import celery
from .models import db, Analysis


reaction_scaler = DynamicPreprocessing(['fva'])
with open('../models/api_model.p', 'rb') as f:
    pathway_scaler = pickle.load(f)


@celery.task()
def save_analysis(analysis_id, concentration_changes):
    reaction_scores = reaction_scaler.fit_transform(
        concentration_changes, None)
    pathway_scores = pathway_scaler.transform(reaction_scores)
    analysis = Analysis.query.get(analysis_id)
    analysis.save_results(reaction_scores, pathway_scores)
    analysis.status = True
    analysis.end_time = datetime.datetime.now()
    db.session.commit()
