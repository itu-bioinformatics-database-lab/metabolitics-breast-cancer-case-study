import json

from preprocessing import FVAScaler
from .app import celery
from .models import db, Analysis

scaler = FVAScaler()


@celery.task()
def save_analysis(analysis_id, concentration_changes):
    result = scaler._sample_transformation(concentration_changes)
    analysis = Analysis.query.get(analysis_id)
    with open('../db/analysis-result/%s.json' % analysis.file, 'w') as f:
        json.dump(result, f)
    analysis.status = True
    db.session.commit()
