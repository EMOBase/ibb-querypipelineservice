import pytest
import io
import json

from ibbtools.pipeline import create_app
import ibbtools.pipeline.service as service


@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def mock_service_get_convert_func(monkeypatch):
    def get_convert_func(key_input, key_output):
        return lambda list_: {k: [k] for k in list_}

    monkeypatch.setattr(service, 'get_convert_func', get_convert_func)


def test_get_steps_success(client):
    rv = client.get('/steps')
    assert rv.status_code == 200

    json_data = rv.get_json()
    assert isinstance(json_data, list)


def __make_pipeline(steps='_default', data='_default', mode='inline'):
    """ Utility to make pipeline for POST /pipelines request.

    Should create a valid pipeline if no argument is provided
    """

    if steps == '_default':
        steps = json.dumps([
            {'input': 'a', 'output': 'b'},
            {'input': 'b', 'output': 'b'},
        ])

    if data == '_default':
        data == __make_data()

    pipeline = {}

    if steps is not None:
        pipeline['steps'] = steps


    if data is not None:
        if mode == 'inline':
            pipeline['data'] = data
        elif mode == 'file':
            pipeline['file'] = (io.BytesIO(data.encode()), 'file.txt')

    return pipeline


def __make_data(data=None, sep='\n', extra_newline=False):
    if data is None:
        data = [
            'FBgn0020412',
            'FBgn0262866',
            'FBgn0052528',
        ]

    res = sep.join(data)
    if extra_newline:
        res += sep
    return res


@pytest.mark.parametrize('mode', ['inline', 'file'])
@pytest.mark.parametrize('sep', ['\n', '\r\n'])
@pytest.mark.parametrize('extra_newline', [True, False])
def test_post_pipelines_success(client, mode, sep, extra_newline):

    data = __make_data(sep=sep, extra_newline=extra_newline)
    pipeline = __make_pipeline(data=data, mode=mode)
    rv = client.post('/pipelines',
            data=pipeline,
            content_type='multipart/form-data')

    assert rv.status_code == 200


@pytest.mark.parametrize('mode', ['inline', 'file'])
@pytest.mark.parametrize('data', [None, ''])
def test_post_pipelines_no_data(client, data, mode):
    pipeline = __make_pipeline(data=data)
    rv = client.post('/pipelines',
            data=pipeline,
            content_type='multipart/form-data')

    assert rv.data.decode() == 'No data provided'
    assert rv.status_code == 400


@pytest.mark.parametrize('step_str', ['abcd', '', '{}', '[]'])
def test_post_pipelines_invalid_steps(client, step_str):
    rv = client.post('/pipelines',
            data=__make_pipeline(steps=step_str),
            content_type='multipart/form-data')

    assert rv.data.decode() == 'Invalid steps'
    assert rv.status_code == 400
