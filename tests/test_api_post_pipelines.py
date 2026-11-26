import pytest
import io
import json
import csv

import ibbtools.pipeline.default_steps as default_steps

from ibbtools.pipeline import create_app
from ibbtools.pipeline.repo import Step


@pytest.fixture
def client():
    fake_convert_func = lambda list_: {k: [k] for k in list_}
    steps = [
        Step('a', 'b', convert_func=fake_convert_func),
        Step('a', 'c', convert_func=fake_convert_func),
        Step('b', 'd', convert_func=fake_convert_func),
    ]
    app = create_app({'TESTING': True}, available_steps=steps)
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize('mode', ['inline', 'file'])
@pytest.mark.parametrize('sep', ['\n', '\r\n'])
@pytest.mark.parametrize('extra_newline', [True, False])
def test_post_pipelines_success(client, mode, sep, extra_newline):

    data = __make_data(['1', '#ignore', '!ignore', '2', ''],
            sep=sep, extra_newline=extra_newline)

    pipeline = __make_pipeline(json.dumps([
            {'input': 'a', 'output': 'b'},
            {'input': 'a', 'output': 'c'},
            {'input': 'b', 'output': 'd'},
        ]), data=data, mode=mode)

    rv = client.post('/pipelines',
            data=pipeline,
            content_type='multipart/form-data')

    csv_data = rv.data.decode()
    csv_reader = csv.reader(io.StringIO(csv_data))

    expected_rows = [
        ['a', 'a -> b', 'a -> c', 'b -> d'],
        ['1', '1', '1', '1'],
        ['2', '2', '2', '2'],
    ]

    for i, row in enumerate(csv_reader):
        assert row == expected_rows[i]

    assert rv.status_code == 200


@pytest.mark.parametrize('mode', ['inline', 'file'])
@pytest.mark.parametrize('data', [None, ''])
def test_post_pipelines_no_data(client, data, mode):
    pipeline = __make_pipeline(data=data)
    rv = client.post('/pipelines',
            data=pipeline,
            content_type='multipart/form-data')

    assert rv.data.decode() == 'No data'
    assert rv.status_code == 400


@pytest.mark.parametrize('step_str,message', [
    ('abcd', 'Invalid json'),
    ('', 'Invalid json'),
    ('{}', 'Validation error'),
    ('[{"input": "a"}]', 'Validation error'),
    ('[{"output": "b"}]', 'Validation error'),
    ('[]', 'No steps'),
    ('[{"input": "no_such_input", "output": "b"}]', 'No such step'),
    ('[{"input": "a", "output": "no_such_output"}]', 'No such step'),
    ('[{"input": "a", "output": "c"}, {"input": "b", "output": "d"}]', 'must exist'),
])
def test_post_pipelines_invalid_steps(client, step_str, message):
    rv = client.post('/pipelines',
            data=__make_pipeline(steps=step_str),
            content_type='multipart/form-data')

    assert message in rv.data.decode()
    assert rv.status_code == 400


def test_post_pipeline_passes_version(monkeypatch):
    seen_versions = []

    def fake_get_default_steps(version=None):
        seen_versions.append(version)
        return [Step('a', 'b',
            convert_func=lambda values: {v: [v] for v in values})]

    monkeypatch.setattr(
        'ibbtools.pipeline.api.get_default_steps', fake_get_default_steps)

    app = create_app({'TESTING': True})
    with app.test_client() as client:
        rv = client.post('/pipelines',
            data=__make_pipeline(
                steps=json.dumps([{'input': 'a', 'output': 'b'}]),
                data='1', version='v9'),
            content_type='multipart/form-data')

    assert rv.status_code == 200
    assert seen_versions[-1] == 'v9'


def test_post_pipeline_ignores_version_query_param(monkeypatch):
    seen_versions = []

    def fake_get_default_steps(version=None):
        seen_versions.append(version)
        return [Step('a', 'b',
            convert_func=lambda values: {v: [v] for v in values})]

    monkeypatch.setattr(
        'ibbtools.pipeline.api.get_default_steps', fake_get_default_steps)

    app = create_app({'TESTING': True})
    with app.test_client() as client:
        rv = client.post('/pipelines?version=from-query',
            data=__make_pipeline(
                steps=json.dumps([{'input': 'a', 'output': 'b'}]),
                data='1'),
            content_type='multipart/form-data')

    assert rv.status_code == 200
    assert seen_versions[-1] is None


def __make_pipeline(steps='_default', data='_default', mode='inline',
        version=None):
    """ Utility to make pipeline for POST /pipelines request.

    Should create a valid pipeline if no argument is provided
    """

    if steps == '_default':
        steps = json.dumps([
            {'input': 'a', 'output': 'b'},
            {'input': 'a', 'output': 'c'},
            {'input': 'b', 'output': 'd'},
        ])

    if data == '_default':
        data == __make_data()

    pipeline = {}

    if steps is not None:
        pipeline['steps'] = steps

    if version is not None:
        pipeline['version'] = version


    if data is not None:
        if mode == 'inline':
            pipeline['data'] = data
        elif mode == 'file':
            pipeline['file'] = (io.BytesIO(data.encode()), 'file.txt')

    return pipeline


def __make_data(data=None, sep='\n', extra_newline=False):
    if data is None:
        data = ['1', '2', '3']

    res = sep.join(data)
    if extra_newline:
        res += sep
    return res
