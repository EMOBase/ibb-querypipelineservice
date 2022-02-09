import json
import os

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

import ibbtools.pipeline.service as service
from ibbtools.pipeline.schema import PipelineSchema


def create_app(test_config=None):
    app = Flask(__name__)
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
                        text/csv: {}
                400:
                    description: Bad request
                    content:
                        text/plain: {}
        """
        try:
            steps = json.loads(request.form.get('steps', '[]'))
        except Exception:
            return 'Invalid json', 400

        file_ = request.files.get('file')

        if file_ and file_.filename:
            data = [d.strip() for d in file_]
        else:
            data = request.form.get('data')
            if data:
                data = data.strip().split('\n')
            else:
                return 'No data provided', 400

        try:
            result = service.execute(steps, data)
        except service.InvalidPipelineError as e:
            return str(e), 400

        return Response(result, mimetype='text/csv')


    @app.route('/q/openapi', methods=['GET'])
    def get_openapi():
        spec = APISpec(
                title='iBB Pipeline API',
                version=app.config['VERSION'],
                servers=[{'url': app.config['SERVER']}],
                openapi_version='3.0.2',
                plugins=[FlaskPlugin(), MarshmallowPlugin()],
        )

        with app.test_request_context():
            (spec
                    .path(view=get_steps)
                    .path(view=post_pipeline)
            )

        return Response(spec.to_yaml(), mimetype='text/yaml')

    return app


def config_app(app, test_config=None):
    CORS(app)

    app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', default='dev'),
            VERSION=os.environ.get('VERSION', default='latest'),
            SERVER=os.environ.get('SERVER', default='0.0.0.0:8080'),
    )

    if test_config:
        app.config.from_mapping(test_config)


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=8080, debug=True)
