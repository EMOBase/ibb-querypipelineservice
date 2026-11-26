from unittest.mock import patch

from ibbtools.pipeline import services


class FakeResponse:
    def __init__(self, data, status_code=200, url='http://genomics'):
        self._data = data
        self.status_code = status_code
        self.ok = status_code < 400
        self.url = url

    def json(self):
        return self._data


def test_get_list_unwraps_genomics_envelope():
    response = FakeResponse(
            {'data': [{'id': 'FBgn0000001'}], 'requestId': 'req-1'})
    with patch('ibbtools.pipeline.services.requests.get',
            return_value=response) as get:
        service = services.HttpService('http://genomics:8080/')
        assert service.get_list('/genes/Dmel', ids='FBgn0000001') == [
            {'id': 'FBgn0000001'}]
        get.assert_called_once_with(
            'http://genomics:8080/genes/Dmel',
            params={'ids': 'FBgn0000001'},
            timeout=30)


def test_get_list_accepts_bare_list():
    with patch('ibbtools.pipeline.services.requests.get',
            return_value=FakeResponse([{'id': 'x'}])):
        service = services.HttpService('http://genomics:8080')
        assert service.get_list('/genes/Dmel') == [{'id': 'x'}]


def test_gene_info_service_uses_species_and_version():
    response = FakeResponse({'data': [{'id': 'FBgn0000001'}]})
    with patch('ibbtools.pipeline.services.requests.get',
            return_value=response) as get:
        service = services.GeneInfoService(
            'http://genomics:8080', species='Dmel', version='v1')
        service.get_drosophila_genes(['FBgn0000001'])
        get.assert_called_once_with(
            'http://genomics:8080/genes/Dmel',
            params={'ids': 'FBgn0000001', 'version': 'v1'},
            timeout=30)


def test_gene_info_service_omits_empty_version():
    response = FakeResponse({'data': [{'id': 'FBgn0000001'}]})
    with patch('ibbtools.pipeline.services.requests.get',
            return_value=response) as get:
        service = services.GeneInfoService(
            'http://genomics:8080', species='Dmel')
        service.get_drosophila_genes(['FBgn0000001'])
        get.assert_called_once_with(
            'http://genomics:8080/genes/Dmel',
            params={'ids': 'FBgn0000001'},
            timeout=30)


def test_gene_info_service_dedupes_by_id():
    response = FakeResponse({'data': [
        {'id': 'FBgn0000001', 'assemblyKey': 'a'},
        {'id': 'FBgn0000001', 'assemblyKey': 'b', 'symbol': 'sym1'},
    ]})
    with patch('ibbtools.pipeline.services.requests.get',
            return_value=response):
        service = services.GeneInfoService(
            'http://genomics:8080', species='Dmel')
        assert service.get_drosophila_genes(['FBgn0000001']) == [
            {'id': 'FBgn0000001', 'assemblyKey': 'a', 'symbol': 'sym1'}]


def test_orthology_service_uses_genomics_paths():
    response = FakeResponse({'data': []})
    with patch('ibbtools.pipeline.services.requests.get',
            return_value=response) as get:
        service = services.OrthologyService(
            'http://genomics:8080',
            main_species='Tcas',
            reference_species='Dmel',
            source='all')
        service.get_drosophila_orthologs(['FBgn0000001'])
        service.get_tribolium_orthologs(['TC000001'])

        calls = get.call_args_list
        assert calls[0].args[0] == 'http://genomics:8080/orthology/Dmel'
        assert calls[0].kwargs['params'] == {
            'genes': 'FBgn0000001', 'source': 'all'}
        assert calls[1].args[0] == 'http://genomics:8080/orthology/Tcas'
        assert calls[1].kwargs['params'] == {
            'genes': 'TC000001', 'source': 'all'}


def test_silencing_service_uses_species_path():
    response = FakeResponse({'data': []})
    with patch('ibbtools.pipeline.services.requests.get',
            return_value=response) as get:
        service = services.GeneSilencingService(
            'http://genomics:8080', species='Tcas')
        service.get_silencing_fragments(tc_id_list=['TC000001'])
        get.assert_called_once_with(
            'http://genomics:8080/silencingseqs/Tcas',
            params={'geneIds': 'TC000001'},
            timeout=30)
