import http
import os
from typing import Any

from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow_enum import EnumField
from pandas import DataFrame
from webargs import fields
from webargs.flaskparser import use_args

from flaskr.data.filters import PredictionFilter, ObservationFilter

from .data import (Element, Scenario, get_data,
                   transform_to_graph)

OBSERVATIONS_GRAPH_ARGS = {
    'element': EnumField(Element, required=True),
    'station': fields.List(fields.Str, required=True),
}

PREDICTION_GRAPH_ARGS = {
    **OBSERVATIONS_GRAPH_ARGS,
    'scenario': EnumField(Scenario, required=True),
    'model': fields.List(fields.Str, required=True),
}


def create_response(data: DataFrame, element: Element) -> Response:
    graph = transform_to_graph(data, element)
    graph = graph.dropna()

    return jsonify(graph.to_dict(orient='records'))


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db = SQLAlchemy(app)

    class Observation(db.Model):
        __tablename__ = 'observation'

        id = db.Column(
            'id', db.Integer, db.Identity(always=True),
            primary_key=True)
        year = db.Column('year', db.SmallInteger, nullable=False)
        month = db.Column('month', db.SmallInteger, nullable=False)
        day = db.Column('day', db.SmallInteger, nullable=False)
        station = db.Column('station', db.String, nullable=False)
        tmin = db.Column('tmin', db.Numeric(4, 2))
        tmax = db.Column('tmax', db.Numeric(4, 2))
        pr = db.Column('pr', db.Numeric(5, 2))

    class Prediction(db.Model):
        __tablename__ = 'prediction'

        id = db.Column(
            'id', db.Integer, db.Identity(always=True),
            primary_key=True)
        year = db.Column('year', db.SmallInteger, nullable=False)
        month = db.Column('month', db.SmallInteger, nullable=False)
        day = db.Column('day', db.SmallInteger, nullable=False)
        station = db.Column('station', db.String, nullable=False)
        model = db.Column('model', db.String, nullable=False)
        scenario = db.Column('scenario', db.Enum(Scenario), nullable=False)
        tmin = db.Column('tmin', db.Numeric(32, 30))
        tmax = db.Column('tmax', db.Numeric(32, 30))
        pr = db.Column('pr', db.Numeric(32, 28))

    @app.route('/graph/observations', methods=['GET'])
    @use_args(
        OBSERVATIONS_GRAPH_ARGS,
        error_status_code=http.HTTPStatus.BAD_REQUEST,
        location='query')
    def get_observations_graph(args: dict[str, Any]):
        element = args['element']
        data = get_data(
            Observation,
            Observation.query,
            ObservationFilter(args['station'], element),
        )

        return create_response(data, element)

    @app.route('/graph/predictions', methods=['GET'])
    @use_args(
        PREDICTION_GRAPH_ARGS,
        error_status_code=http.HTTPStatus.BAD_REQUEST,
        location='query')
    def get_predictions_graph(args: dict[str, Any]):
        data = get_data(
            Prediction,
            Prediction.query,
            PredictionFilter(
                args['station'],
                args['model'],
                args['scenario']),
        )

        return create_response(data, args['element'])

    return app
