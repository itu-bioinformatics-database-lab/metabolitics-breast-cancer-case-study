import json

from preprocessing import FVAScaler
from .app import celery

scaler = FVAScaler()


@celery.task()
def add_together(a, b):
    with open('a.txt', 'a') as f:
        f.write('%d + %d = %d \n' % (a, b, a + b))


@celery.task()
def save_analysis(filename, concentration_changes):
    result = scaler._sample_transformation(concentration_changes)
    with open('../db/analysis-result/%s.json' % filename, 'w') as f:
        json.dump(result, f)
