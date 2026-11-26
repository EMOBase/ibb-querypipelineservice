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


def test_default_steps_keep_tcas_labels(client):
    steps = client.get('/steps').get_json()
    names = {step['name'] for step in steps}
    by_name = {step['name']: step for step in steps}

    assert 'FBgn -> TC' in names
    assert 'TC -> iB' in names
    assert 'iB -> larval lethality day 11' in names
    assert by_name['TC -> iB']['requires'] == 'dsrna'
    assert by_name['iB -> TC']['requires'] == 'dsrna'
    assert by_name['iB -> larval lethality day 11']['requires'] == 'dsrna'
    assert by_name['FBgn -> TC'].get('requires') is None


def test_steps_use_configured_main_species_labels():
    app = create_app({
        'TESTING': True,
        'MAIN_SPECIES': 'Ptep',
        'MAIN_GENE_LABEL': 'Ptep',
        'MAIN_SPECIES_GENE_PATTERN': r'^Ptep\d+$',
        'DSRNA_LABEL': 'dsRNA',
        'LETHALITY_STEPS_ENABLED': 'false',
    })

    with app.test_client() as client:
        steps = client.get('/steps').get_json()

    names = {step['name'] for step in steps}
    by_name = {step['name']: step for step in steps}

    assert 'FBgn -> Ptep' in names
    assert 'Ptep -> FBgn' in names
    assert 'Ptep -> dsRNA' in names
    assert 'dsRNA -> Ptep' in names
    assert not any('lethality' in name for name in names)

    assert by_name['Ptep -> dsRNA']['requires'] == 'dsrna'
    assert by_name['dsRNA -> Ptep']['requires'] == 'dsrna'
    assert by_name['FBgn -> Ptep'].get('requires') is None

    # The reference side stays Dmel/FlyBase.
    assert 'FBgn -> FB symbol' in names
    assert 'FBgn -> CG' in names
