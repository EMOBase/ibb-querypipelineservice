import requests

class HttpService:
    def __init__(self, base_url):
        self.base_url = base_url


class GeneInfoService(HttpService):
    def __init__(self, *args):
        super().__init__(*args)


    def get_drosophila_genes(self, id_list):
        r = requests.get(self.base_url +
            '/drosophila/genes?ids=' +
            ','.join(id_list))
        return r.json()


geneinfo_service = GeneInfoService('http://ibb-test.vm19002.virt.gwdg.de/ibb/api/geneinfo/v1')
