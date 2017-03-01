import uuid

from flask import jsonify, request
from flask_swagger import swagger
from flask_jwt import jwt_required, current_identity

from .app import app
from .schemas import AnalysisInputSchema, UserSchema, AnalysisSchema
from .models import db, User, Analysis
from .tasks import save_analysis

__all__ = [
    'fva_analysis',
    'sign_up',
    'spec'
]


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Metabolitics API"
    return jsonify(swag)


@app.route('/analysis/fva', methods=['POST'])
@jwt_required()
def fva_analysis():
    """
    FVA analysis
    ---
    tags:
      - analysis
    parameters:
        -
          name: authorization
          in: header
          type: string
          required: true
        -
          name: name
          in: body
          type: string
          required: true
        -
          name: concentration_changes
          in: body
          required: true
    responses:
      200:
        description: Analysis info
      404:
        description: Analysis not found
      401:
        description: Analysis is not yours
    """
    (data, error) = AnalysisInputSchema().load(request.json)
    if error:
        return jsonify(error), 400
    print(data)
    analysis = Analysis(data['name'], str(uuid.uuid4()), current_identity)
    db.session.add(analysis)
    db.session.commit()
    save_analysis.delay(analysis.id, data['concentration_changes'])
    return ''


@app.route('/analysis/list')
@jwt_required()
def user_analysis():
    """
    List of analysis of user
    ---
    tags:
        - analysis
    parameters:
        -
          name: authorization
          in: header
          type: string
          required: true
    """
    return AnalysisSchema(many=True).jsonify(
        i for i in current_identity.analysis)


@app.route('/auth/sign-up', methods=['POST'])
def sign_up():
    """
    Create a new user
    ---
    tags:
      - users
    parameters:
      - in: body
        name: body
        schema:
          id: User
          required:
            - name
            - surname
            - email
            - affiliation
            - password
          properties:
            name:
                type: string
                description: name for user
            surname:
                type: string
                description: surname for user
            email:
                type: string
                description: email for user
            password:
                type: string
                description: password for user
            affiliation:
                type: string
                description: affiliation for user
    responses:
      201:
        description: User created
    """
    (data, error) = UserSchema().load(request.json)
    if error:
        return jsonify(error), 400
    if User.query.filter_by(email=data.email).first():
        return jsonify({'email': ['this email in use']}), 400
    db.session.add(data)
    db.session.commit()
    return ''


@app.route('/auth/info')
@jwt_required()
def auth_info():
    """
    Get user info
    ---
    tags:
      - users
    parameters:
        -
          name: authorization
          in: header
          type: string
          required: true
    responses:
      200:
        description: User info
    """
    return UserSchema().jsonify(current_identity)


@app.route('/analysis/detail/<id>')
@jwt_required()
def analysis_detail(id):
    """
    Get analysis detail from id
    ---
    tags:
      - analysis
    parameters:
        -
          name: authorization
          in: header
          type: string
          required: true
        -
          name: id
          in: path
          type: integer
          required: true
    responses:
      200:
        description: Analysis info
      404:
        description: Analysis not found
      401:
        description: Analysis is not yours
    """
    analysis = Analysis.query.get(id)
    if not analysis:
        return '', 404
    if analysis.user_id != current_identity.id:
        return '', 401
    return AnalysisSchema().jsonify(analysis)
