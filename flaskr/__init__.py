import http
import os

from flask import Flask, jsonify, request
from webargs import fields
from webargs.flaskparser import use_args

from flaskr.data.common import transform_to_graph

from .data import Element, Scenario, get_model_data, get_observation_data


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

    @app.route('/graph', methods=['GET'])
    @use_args(
        {
            'station': fields.List(fields.Str, required=True),
        },
        error_status_code=http.HTTPStatus.BAD_REQUEST,
        location='query')
    def get_graph(args):
        element = Element.TEMP_AVG
        stations: list[str] = args['station']

        if 'scenario' in request.args:
            scenario = request.args.get('scenario', type=Scenario)
            models = request.args.getlist('model', type=str)
            if scenario is None or not models:
                return 'At least one of the following query parameters is missing: scenario, models.', 400

            data = get_model_data(
                app.open_resource, element, stations, models, scenario)
        else:
            data = get_observation_data(
                app.open_resource, element, stations)

        graph = transform_to_graph(data, element)

        return jsonify(graph.to_dict(orient='records'))

    return app
