import requests

class DownstreamServiceError(Exception):
    pass


class HttpService:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, path, **params):
        url = self.base_url + path
        if params:
            url += '?' + '&'.join(f'{k}={v}' for k, v in params.items())

        r = requests.get(url)
        if not r.ok:
            raise DownstreamServiceError('Request failed with status'
                f' {r.status_code}: {url}')

        try:
            data = r.json()
        except requests.exceptions.JSONDecodeError:
            raise DownstreamServiceError('Invalid json')
        return data


    def get_list(self, path, **params):
        list_ = self.get(path, **params)
        if not isinstance(list_, list):
            raise DownstreamServiceError('Not a list')
        return list_

    def get_object(self, path, **params):
        object_ = self.get(path, **params)
        if not isinstance(object_, dict):
            raise DownstreamServiceError('Not an object')
        return object_



class GeneInfoService(HttpService):
    def get_drosophila_genes(self, id_list=None, symbol=None, cg=None):
        path = '/drosophila/genes'

        if id_list:
            return self.get_list(path, ids=','.join(id_list))
        elif symbol:
            return self.get_list(path, symbol=symbol)
        elif cg:
            return self.get_list(path, annotationId=cg)
        else:
            return []


class OrthologyService(HttpService):
    def get_drosophila_orthologs(self, id_list):
        path = '/datasources/orthofinder/drosophila/genes'
        return self.get_list(path, geneIds=','.join(id_list))


    def get_tribolium_orthologs(self, id_list):
        path = '/datasources/orthofinder/tribolium/genes'
        return self.get_list(path, geneIds=','.join(id_list))


class GeneSilencingService(HttpService):
    def get_silencing_fragments(self, tc_id_list=None, ib_id_list=None):
        path = '/silencingseqs'
        if tc_id_list:
            return self.get_list(path, geneIds=','.join(tc_id_list))
        elif ib_id_list:
            return self.get_list(path, ids=','.join(ib_id_list))
        else:
            return []


# class GeneOntologyService(HttpService):
#     def get_go_terms(self, go_id_list):
#         path = '/GO'
#         return self.get_list(path, ids=','.join(go_id_list))

#     def get_annotations(self, gene_id_list=None, go_id_list=None):
#         path = '/annotation'
#         if gene_id_list:
#             return self.get_list(path, geneId=','.join(gene_id_list))
#         elif go_id_list:
#             return self.get_list(path, termId=','.join(go_id_list))
#         else:
#             return []


class PhenotypeService(HttpService):
    def get_lethality_values(self, ib_id):
        path = '/lethality/' + ib_id
        return self.get_object(path)
