import requests

class HttpService:
    def __init__(self, base_url):
        self.base_url = base_url


class GeneInfoService(HttpService):
    def __init__(self, *args):
        super().__init__(*args)


    def get_drosophila_genes(self, id_list=None, symbol=None, cg=None):
        url = self.base_url + '/drosophila/genes'

        if id_list:
            url += '?ids=' + ','.join(id_list)
        elif symbol:
            url += '?symbol=' + symbol
        elif cg:
            url += '?annotationId=' + cg

        return requests.get(url).json()


class OrthologyService(HttpService):
    def __init__(self, *args):
        super().__init__(*args)


    def get_drosophila_orthologs(self, id_list):
        url = self.base_url + '/datasources/Legacy/drosophila/genes'
        url += '?geneIds=' + ','.join(id_list)
        return requests.get(url).json()


    def get_tribolium_orthologs(self, id_list):
        url = self.base_url + '/datasources/Legacy/tribolium/genes'
        url += '?geneIds=' + ','.join(id_list)
        return requests.get(url).json()
