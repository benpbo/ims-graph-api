import http
import os
from typing import Any

from flask import Flask, Response, jsonify
from marshmallow_enum import EnumField
from pandas import DataFrame
from webargs import fields
from webargs.flaskparser import use_args

from flaskr.data.common import transform_to_graph

from .data import Element, Scenario, get_model_data, get_observation_data

OBSERVATIONS_GRAPH_ARGS = {
    'station': fields.List(fields.Str, required=True),
}

MODELS_GRAPH_ARGS = {
    **OBSERVATIONS_GRAPH_ARGS,
    'scenario': EnumField(Scenario, required=True),
    'model': fields.List(fields.Str, required=True),
}


def create_response(data: DataFrame, element: Element) -> Response:
    graph = transform_to_graph(data, element)
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

    @app.route('/graph/observations', methods=['GET'])
    @use_args(
        OBSERVATIONS_GRAPH_ARGS,
        error_status_code=http.HTTPStatus.BAD_REQUEST,
        location='query')
    def get_observations_graph(args: dict[str, Any]):
        element = Element.TEMP_AVG
        data = get_observation_data(
            app.open_resource,
            element,
            args['station'])

        return create_response(data, element)

    @app.route('/graph/models', methods=['GET'])
    @use_args(
        MODELS_GRAPH_ARGS,
        error_status_code=http.HTTPStatus.BAD_REQUEST,
        location='query')
    def get_models_graph(args: dict[str, Any]):
        element = Element.TEMP_AVG
        data = get_model_data(
            app.open_resource,
            element,
            args['station'],
            args['model'],
            args['scenario'])

        return create_response(data, element)

    return app
