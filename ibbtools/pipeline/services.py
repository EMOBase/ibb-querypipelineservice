import requests

class DownstreamServiceError(Exception):
    pass


class HttpService:
    def __init__(self, base_url, timeout=30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def get(self, path, **params):
        url = self.base_url + path

        try:
            r = requests.get(url, params=params or None, timeout=self.timeout)
        except requests.RequestException as e:
            raise DownstreamServiceError(
                    f'Request failed for {url}: {e}') from e

        if not r.ok:
            raise DownstreamServiceError('Request failed with status'
                f' {r.status_code}: {r.url}')

        try:
            data = r.json()
        except requests.exceptions.JSONDecodeError:
            raise DownstreamServiceError('Invalid json')
        return data


    def get_data(self, path, **params):
        data = self.get(path, **params)
        # The genomics service wraps successful responses as
        # {"data": ..., "requestId": ...}; the legacy services returned the
        # payload directly.
        if isinstance(data, dict) and 'data' in data:
            return data['data']
        return data

    def get_list(self, path, **params):
        list_ = self.get_data(path, **params)
        if not isinstance(list_, list):
            raise DownstreamServiceError('Not a list')
        return list_

    def get_object(self, path, **params):
        object_ = self.get_data(path, **params)
        if not isinstance(object_, dict):
            raise DownstreamServiceError('Not an object')
        return object_


class GenomicsService(HttpService):
    def __init__(self, base_url, version=''):
        super().__init__(base_url)
        self.version = version

    def _params(self, **params):
        if self.version:
            params['version'] = self.version
        return params


class GeneInfoService(GenomicsService):
    def __init__(self, base_url, species, version=''):
        super().__init__(base_url, version=version)
        self.species = species

    def get_drosophila_genes(self, id_list=None, symbol=None, cg=None):
        path = f'/genes/{self.species}'

        if id_list:
            genes = self.get_list(path, **self._params(ids=','.join(id_list)))
        elif symbol:
            genes = self.get_list(path, **self._params(symbol=symbol))
        elif cg:
            genes = self.get_list(path, **self._params(annotationId=cg))
        else:
            return []

        return _dedupe_by_id(genes)


class OrthologyService(GenomicsService):
    def __init__(self, base_url, main_species, reference_species='Dmel',
            source='all', version=''):
        super().__init__(base_url, version=version)
        self.main_species = main_species
        self.reference_species = reference_species
        self.source = source

    def _get(self, species, id_list):
        params = self._params(genes=','.join(id_list), source=self.source)
        return self.get_list(f'/orthology/{species}', **params)

    def get_drosophila_orthologs(self, id_list):
        return self._get(self.reference_species, id_list)


    def get_tribolium_orthologs(self, id_list):
        return self._get(self.main_species, id_list)


class GeneSilencingService(GenomicsService):
    def __init__(self, base_url, species, version=''):
        super().__init__(base_url, version=version)
        self.species = species

    def get_silencing_fragments(self, tc_id_list=None, ib_id_list=None):
        path = f'/silencingseqs/{self.species}'
        if tc_id_list:
            return self.get_list(path,
                **self._params(geneIds=','.join(tc_id_list)))
        elif ib_id_list:
            return self.get_list(path, **self._params(ids=','.join(ib_id_list)))
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


def _dedupe_by_id(items):
    """Merge entries that refer to the same gene.

    A genomics Database Version can hold several assemblies of one species, so
    /genes/{species} may return the same gene once per assembly. Keep the first
    entry, then fill any missing gene fields from the later ones.
    """
    by_id = {}
    order = []
    for item in items:
        item_id = item.get('id')
        if item_id not in by_id:
            by_id[item_id] = dict(item)
            order.append(item_id)
            continue
        for key, value in item.items():
            if key in ('id', 'assemblyVersionId', 'assemblyKey'):
                continue
            if not by_id[item_id].get(key) and value:
                by_id[item_id][key] = value
    return [by_id[item_id] for item_id in order]
