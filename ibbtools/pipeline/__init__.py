import json
import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

import ibbtools.pipeline.service as service
from ibbtools.pipeline.schema import PipelineSchema


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    config_app(app, test_config)


    @app.route('/steps', methods=['GET'])
    def get_steps():
        """
        ---
        get:
            description: Returns all available steps

            responses:
                200:
                    description: Pipeline steps successfully returned
                    content:
                        application/json: {}
        """
        steps = list(service.get_steps())
        return jsonify(steps)


    @app.route('/pipeline', methods=['POST'])
    def post_pipeline():
        """
        ---
        post:
            description: Execute a pipeline
            requestBody:
                content:
                    multipart/form-data:
                        schema: PipelineSchema
            responses:
                200:
                    description: Successfully executed
                    content:
                        application/json: {}
                        text/csv: {}
                400:
                    description: Bad request
                    content:
                        text/plain: {}
        """
        steps = json.loads(request.form.get('steps', '[]'))
        data = json.loads(request.form.get('data', '[]'))
        file_ = request.files.get('file')
        if file_ and file_.filename:
            data = [d.strip() for d in file_]

        try:
            result = service.execute(steps, data)
        except service.InvalidPipelineError as e:
            return str(e), 400

        return jsonify(result)


    @app.route('/q/openapi', methods=['GET'])
    def get_openapi():
        spec = APISpec(
                title='iBB Pipeline API',
                version=app.config['VERSION'],
                openapi_version='3.0.2',
                plugins=[FlaskPlugin(), MarshmallowPlugin()],
        )

        with app.test_request_context():
            (spec
                    .path(view=get_steps)
                    .path(view=post_pipeline)
            )

        return spec.to_yaml()

    return app


def config_app(app, test_config):
    CORS(app)

    app.config.from_mapping(
            SECRET_KEY='dev',
            VERSION='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)


if __name__ == '__main__':
    create_app().run(debug=True)
