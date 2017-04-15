import json
import datetime
import pickle

from .app import celery
from .models import db, Analysis

with open('../models/api_model.p', 'rb') as f:
    scaler = pickle.load(f)


@celery.task()
def save_analysis(analysis_id, concentration_changes):
    result = scaler.transform(concentration_changes)
    analysis = Analysis.query.get(analysis_id)
    with open('../db/analysis-result/%s.json' % analysis.filename, 'w') as f:
        json.dump(result, f)
    analysis.status = True
    analysis.end_time = datetime.datetime.now()
    db.session.commit()
