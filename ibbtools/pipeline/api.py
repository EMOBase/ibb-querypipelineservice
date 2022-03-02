import json
import os
import io

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from marshmallow import ValidationError

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from ibbtools.pipeline.schema import PipelineSchema, StepSchema
from ibbtools.pipeline.repo import Step, StepRepo, StepNotFoundError
from ibbtools.pipeline.pipeline import Pipeline, InvalidPipelineError
from ibbtools.pipeline.default_steps import get_default_steps


def create_app(test_config=None, available_steps=None):
    app = Flask(__name__)
    config_app(app, test_config)

    repo = StepRepo()
    if available_steps is None:
        repo.add_all(get_default_steps())
    else:
        repo.add_all(available_steps)


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
                        application/json:
                            schema:
                                type: array
                                items:
                                    schema: StepSchema
        """
        steps = repo.get_all()
        schema = StepSchema(many=True)
        return jsonify(schema.dump(steps))


    @app.route('/pipelines', methods=['POST'])
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
                        application/json: {}
        """

        try:
            steps = json.loads(request.form.get('steps'))
            steps = StepSchema(many=True).load(steps)
            steps = [repo.get(s.input, s.output) for s in steps]
        except json.decoder.JSONDecodeError:
            return jsonify(error='Invalid json'), 400
        except ValidationError as e:
            return jsonify(error='Validation error'), 400
        except StepNotFoundError as e:
            return jsonify(error=str(e)), 400

        file_ = request.files.get('file')
        if file_ and file_.filename:
            data = io.TextIOWrapper(file_, encoding='utf-8').read()
        else:
            data = request.form.get('data', '')
        data = data.strip().splitlines()
        data = [d.strip() for d in data]

        try:
            pipeline = Pipeline(steps)
            result = pipeline.execute(data)
        except InvalidPipelineError as e:
            return jsonify(error=str(e)), 400

        return Response(result.to_csv(), mimetype='text/csv')


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
            SERVER=os.environ.get('SERVER', default='0.0.0.0:5000'),
    )

    if test_config:
        app.config.from_mapping(test_config)


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=True)
