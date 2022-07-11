import mimetypes
import os

from flask import Flask, Response, request

from .data import Element, Scenario, get_model_data


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
        station = request.args.get('station', type=str)
        model = request.args.get('model', type=str)
        match request.args.get('scenario', type=str):
            case 'rcp45':
                scenario = Scenario.RCP45
            case 'rcp85':
                scenario = Scenario.RCP85
            case None:
                return 'No scenario', 400
            case unmatched:
                return f'Bad scenario: {unmatched}', 400

        data = get_model_data(
            app.open_resource,
            Element.TEMP_AVG, (station, ), (model, ), scenario)

        return Response(data.to_csv(None), mimetype=mimetypes.types_map['.csv'])

    return app
