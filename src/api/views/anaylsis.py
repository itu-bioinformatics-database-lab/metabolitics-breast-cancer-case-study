from functools import reduce

from flask import jsonify, request
from flask_jwt import jwt_required, current_identity
from sqlalchemy import and_
from sqlalchemy.types import Float

from services import similarty_dict
from visualization import HeatmapVisualization

from ..app import app
from ..schemas import *
from ..models import db, User, Analysis
from ..tasks import save_analysis


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
        - in: body
          name: body
          schema:
            id: AnalysisInput
            required:
              - name
              - concentration_changes
            properties:
              name:
                  type: string
                  description: name of analysis
              concentration_changes:
                  type: object
                  description: concentration changes of metabolitics
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

    analysis = Analysis(
        data['name'],
        current_identity,
        type='public' if data['public'] else 'private')
    db.session.add(analysis)
    db.session.commit()

    analysis_id = analysis.id
    save_analysis.delay(analysis_id, data['concentration_changes'])

    return jsonify({'id': analysis_id})


@app.route('/analysis/set')
def user_analysis_set():
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
    analyses = list(Analysis.get_multiple(request.args.values()))
    if len(analyses) != len(request.args):
        return '', 401
    X = [i.results_pathway for i in analyses]
    y = [i.name for i in analyses]
    return AnalysisSchema(many=True).jsonify(analyses)


@app.route('/analysis/visualization')
def analysis_visualization():
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
    analyses = list(Analysis.get_multiple(request.args.values()))
    if len(analyses) != len(request.args):
        return '', 401
    X = [i.results_pathway[0] for i in analyses]
    y = [i.name for i in analyses]
    return jsonify(HeatmapVisualization(X, y).clustered_data())


@app.route('/analysis/<type>')
def disease_analysis(type: str):
    """
    List of disease analysis avaliable in db
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
        Analysis.query.filter_by(type=type).with_entities(
            Analysis.id, Analysis.name, Analysis.status))


@app.route('/analysis/detail/<id>')
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
    if not analysis.authenticated():
        return '', 401
    return AnalysisSchema().jsonify(analysis)


@app.route('/analysis/most-similar-diseases/<id>')
def most_similar_diseases(id: int):
    """
    Calculates most similar disease for given disease id
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
        description: Most similar diseases
      404:
        description: Analysis not found
      401:
        description: Analysis is not yours
    """
    analysis = Analysis.query.get(id)
    if not analysis:
        return '', 404
    if analysis.authenticated():
        return '', 401

    row_disease_analyses = Analysis.query.filter_by(
        type='disease').with_entities(Analysis.name,
                                      Analysis.results_pathway).all()

    names, disease_analyses = zip(*[(i[0], i[1][0])
                                    for i in row_disease_analyses])

    sims = similarty_dict(analysis.results_pathway[0], list(disease_analyses))
    top_5 = sorted(zip(names, sims), key=lambda x: x[1], reverse=True)[:5]

    return jsonify(dict(top_5))


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
        current_identity.analysis.filter_by(type='private').with_entities(
            Analysis.id, Analysis.name, Analysis.status))


@app.route('/analysis/search/<query>')
def search_analysis(query: str):
    """
    Search query in db
    ---
    tags:
        - analysis
    parameters:
        -
          name: query
          in: url
          type: string
          required: true
    """
    return AnalysisSchema(many=True).jsonify(
        Analysis.query.filter(Analysis.name.ilike('%' + query + '%'))
        .with_entities(Analysis.id, Analysis.name, Analysis.status))


@app.route('/analysis/search-by-change', methods=['POST'])
def search_analysis_by_change():
    """
    Search query in db
    ---
    tags:
        - analysis
    parameters:
        -
          name: query
          in: url
          type: string
          required: true
    """
    (data, error) = PathwayChangesScheme().load(request.json, many=True)
    if error:
        return jsonify(error), 400

    return AnalysisSchema(many=True).jsonify(
        Analysis.query.filter_by_change_many(data)
        .filter_by_change_amount_many(data)
        .with_entities(Analysis.id, Analysis.name, Analysis.status))
