import mimetypes
import os

from flask import Flask, Response, request

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

    @app.route('/temperature', methods=['GET'])
    def temperature():
        stations = request.args.getlist('station', type=str)
        if not stations:
            return 'Query parameter for "station" is missing.', 400

        if 'scenario' in request.args:
            scenario = request.args.get('scenario', type=Scenario)
            models = request.args.getlist('model', type=str)
            if scenario is None or not models:
                return 'At least one of the following query parameters is missing: scenario, models.', 400

            data = get_model_data(
                app.open_resource,
                Element.TEMP_AVG, stations, models, scenario)
        else:
            data = get_observation_data(
                app.open_resource,
                Element.TEMP_AVG, stations)

        return Response(data.to_csv(None), mimetype=mimetypes.types_map['.csv'])

    return app
