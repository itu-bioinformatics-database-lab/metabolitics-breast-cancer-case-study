from flask import jsonify, request

from .app import app
from .schemas import AnalysisSchema, SignUpSchema
from .models import db, User
from .tasks import save_analysis

__all__ = [
    'fva_analysis'
]


@app.route('/analysis/fva', methods=['POST'])
def fva_analysis():
    (data, error) = AnalysisSchema().load(request.json)
    if error:
        return jsonify(error), 400
    save_analysis.delay(data['name'], data['concentration_changes'])
    return ''


@app.route('/auth/sign-up', methods=['POST'])
def sign_up():
    (data, error) = SignUpSchema().load(request.json)
    if error:
        return jsonify(error), 400
    if User.query.filter_by(email=data.email).first():
        return jsonify({'email': ['this email in use']}), 400
    db.session.add(data)
    db.session.commit()
    return ''
