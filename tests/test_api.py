import pytest
import io
import json

from ibbtools.pipeline import create_app

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client


def test_get_steps(client):
    rv = client.get('/steps')
    assert rv.status_code == 200

    json_data = rv.get_json()
    assert isinstance(json_data, list)


def test_post_pipelines_with_uploaded_file(client):
    steps = [
        {'input': 'a', 'output': 'b'},
        {'input': 'b', 'output': 'b'},
    ]
    file_ = (io.BytesIO(b'FBgn0020412\nFBgn0262866\nFBgn0052528'), 'fbgn.txt')

    pipeline = {
        'steps': json.dumps(steps),
        'file': file_,
    }

    rv = client.post('/pipelines', data=pipeline, content_type='multipart/form-data')
    assert rv.status_code == 200


def test_post_pipelines_with_inline_data(client):
    steps = [
        {'input': 'a', 'output': 'b'},
        {'input': 'b', 'output': 'b'},
    ]

    pipeline = {
        'steps': json.dumps(steps),
        'data': 'FBgn0020412\nFBgn0262866\nFBgn0052528',
    }

    rv = client.post('/pipelines', data=pipeline, content_type='multipart/form-data')
    assert rv.status_code == 200
