import pytest

from ibbtools.pipeline import create_app

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client


def test_get_steps_success(client):
    rv = client.get('/steps')

    json_data = rv.get_json()
    assert isinstance(json_data, list)

    assert len(json_data) > 0

    for step in json_data:
        assert 'input' in step
        assert 'output' in step
        assert 'name' in step
        assert 'category' in step
        assert 'description' in step


    assert rv.status_code == 200
