import json
import os
import io

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

from marshmallow import ValidationError

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

import ibbtools.pipeline.config

from ibbtools.pipeline.schema import PipelineSchema, StepSchema
from ibbtools.pipeline.repo import Step, StepRepo, StepNotFoundError
from ibbtools.pipeline.pipeline import Pipeline, InvalidPipelineError
from ibbtools.pipeline.default_steps import get_default_steps


def create_app(test_config=None, available_steps=None):
    app = Flask(__name__)
    config_app(app, test_config)

    def make_repo(version=None):
        repo = StepRepo()
        if available_steps is None:
            repo.add_all(get_default_steps(version=version))
        else:
            repo.add_all(available_steps)
        return repo

    with app.app_context():
        repo = make_repo()


    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return e.description, 400


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
                        text/plain: {}
        """


        version = request.form.get('version') or request.args.get('version')
        request_repo = make_repo(version)

        steps = __preprocess_steps(request, request_repo)
        data = __preprocess_data(request)

        try:
            pipeline = Pipeline(steps)
            result = pipeline.execute(data)
        except InvalidPipelineError as e:
            raise BadRequest(str(e))

        return Response(result.to_csv(), mimetype='text/csv')


    @app.route('/q/openapi', methods=['GET'])
    def get_openapi():
        spec = APISpec(
                title='iBB Pipeline API',
                version=app.config['VERSION'],
                servers=[{'url': app.config['PUBLIC_SERVER']}],
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

    app.config.from_object('ibbtools.pipeline.config')

    if test_config:
        app.config.from_mapping(test_config)


def __preprocess_steps(request, repo):
    try:
        steps = json.loads(request.form.get('steps'))
        steps = StepSchema(many=True).load(steps)
        steps = [repo.get(s.input, s.output) for s in steps]
    except json.decoder.JSONDecodeError:
        raise BadRequest('Invalid json')
    except ValidationError as e:
        raise BadRequest('Validation error')
    except StepNotFoundError as e:
        raise BadRequest(str(e))

    if not steps:
        raise BadRequest('No steps')
    return steps


def __preprocess_data(request):
    comment_prefixes = set(['#', '!'])

    file_ = request.files.get('file')
    if file_ and file_.filename:
        data = io.TextIOWrapper(file_, encoding='utf-8').read()
    else:
        data = request.form.get('data', '')
    data = data.strip().splitlines()
    data = [d.strip() for d in data]
    data = [d for d in data if d and d[0] not in comment_prefixes]

    if not data:
        raise BadRequest('No data')
    return data


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=True)
