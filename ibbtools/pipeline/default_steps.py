from flask import current_app as app
from ibbtools.pipeline.repo import Step
import ibbtools.pipeline.services as services


dict_steps = {
    'tc_id': {
        'go_id': {
            'name': 'TC -> GO ID',
            'category': 'Gene Ontology Annotation',
            'description': 'Get GO ID for Tribolium genes',
        },
        'ib_id': {
            'name': 'TC -> iB',
            'category': 'Gene Function Experiment',
            'description': 'Get iB numbers for Tribolium genes'
        },
    },
    'dm_id': {
        'go_id': {
            'name': 'FBgn -> GO',
            'category': 'Gene Ontology Annotation',
            'description': 'Get GO ID for Drosophila genes',
        },
    },
    'go_id': {
        'go_aspect': {
            'name': 'GO ID -> GO aspect',
            'category': 'Gene Ontology Annotation',
            'description': 'Convert GO IDs to one of the three GO aspects',
        },
        'go_term': {
            'name': 'GO ID -> GO term',
            'category': 'Gene Ontology Annotation',
            'description': 'Convert GO IDs to theirs corresponding name',
        },
        'tc_id': {
            'name': 'GO ID -> TC',
            'category': 'Gene Ontology Annotation',
            'description': 'Get Tribolium genes for GO IDs',
        },
        'dm_id': {
            'name': 'GO ID -> FBgn',
            'category': 'Gene Ontology Annotation',
            'description': 'Get Drosophila genes for GO IDs',
        },
    },
    'ib_id': {
        'tc_id': {
            'name': 'iB -> TC',
            'category': 'Gene Function Experiment',
            'description': 'Get Tribolium genes silenced by the iB fragments'
        },
        'larval_lethality_11': {
            'name': 'iB -> larval lethality day 11',
            'category': 'Gene Function Experiment',
            'description': 'Get lethality on day 11 in iBeelte larval experiments',
        },
        'larval_lethality_22': {
            'name': 'iB -> larval lethality day 22',
            'category': 'Gene Function Experiment',
            'description': 'Get lethality on day 22 in iBeelte larval experiments',
        },
        'pupal_lethality_11': {
            'name': 'iB -> pupal lethality day 11',
            'category': 'Gene Function Experiment',
            'description': 'Get lethality on day 11 in iBeelte pupal experiments',
        },
    },
}

# Input Output
TC_ID = 'TC'

DM_ID = 'FBgn'
DM_SYMBOL = 'FB symbol'
DM_NAME = 'FB name'
DM_CG = 'CG'

GO_ID = 'GO ID'
GO_ASPECT = 'GO aspect'
GO_TERM = 'GO term'

IB_ID = 'iB'

LETHALITY_LARVAL_11 = 'larval lethality day 11'
LETHALITY_LARVAL_22 = 'larval lethality day 22'
LETHALITY_PUPAL_11 = 'pupal lethality day 11'

# Category
CAT_GENE_ALIAS = 'Gene Alias'
CAT_ORTHOLOGY = 'Orthology'
CAT_GO_ANNOTATION = 'Gene Ontology Annotation'
CAT_EXPERIMENT = 'Gene Function Experiment'


def get_default_steps():
    geneinfo_service = services.GeneInfoService(
            app.config['GENEINFO_SERVICE_BASE_URL'])

    orthology_service = services.OrthologyService(
            app.config['ORTHOLOGY_SERVICE_BASE_URL'])


    def func__dm_id__dm_symbol(dm_id_list):
        genes = geneinfo_service.get_drosophila_genes(dm_id_list)
        return {gene['id']: [gene.get('symbol')] for gene in genes}

    step__dm_id__dm_symbol = Step(DM_ID, DM_SYMBOL,
            category=CAT_GENE_ALIAS,
            convert_func=func__dm_id__dm_symbol,
            description='Convert Drosophila gene identifiers in FBgnxxxxxxx'
            ' format to their corresponding symbol')


    def func__dm_id__dm_name(dm_id_list):
        genes = geneinfo_service.get_drosophila_genes(dm_id_list)
        return {gene['id']: [gene.get('fullname')] for gene in genes}


    step__dm_id__dm_name = Step(DM_ID, DM_NAME,
            category=CAT_GENE_ALIAS,
            convert_func=func__dm_id__dm_name,
            description='Convert Drosophila gene identifiers in FBgnxxxxxxx'
            ' format to their corresponding name')


    def func__dm_id__dm_cg(dm_id_list):
        genes = geneinfo_service.get_drosophila_genes(dm_id_list)
        return {gene['id']: [gene.get('annotationId')] for gene in genes}

    step__dm_id__dm_cg = Step(DM_ID, DM_CG,
            category=CAT_GENE_ALIAS,
            convert_func=func__dm_id__dm_cg,
            description='Convert Drosophila gene identifiers in FBgnxxxxxxx'
            ' format to CGxxxx format')


    def func__dm_symbol__dm_id(dm_symbol_list):
        mapping = {}
        for symbol in dm_symbol_list:
            genes = geneinfo_service.get_drosophila_genes(symbol=symbol)
            gene_ids = [gene['id'] for gene in genes]
            mapping[symbol] = gene_ids

        return mapping

    step__dm_symbol__dm_id = Step(DM_SYMBOL, DM_ID,
            category=CAT_GENE_ALIAS,
            convert_func=func__dm_symbol__dm_id,
            description='Convert Drosophila symbols to their gene identifiers'
            ' in FBgnxxxxxxx format')

    def func__dm_cg__dm_id(dm_cg_list):
        mapping = {}
        for cg in dm_cg_list:
            genes = geneinfo_service.get_drosophila_genes(cg=cg)
            gene_ids = [gene['id'] for gene in genes]
            mapping[cg] = gene_ids

        return mapping


    step__dm_cg__dm_id = Step(DM_CG, DM_ID,
            category=CAT_GENE_ALIAS,
            convert_func=func__dm_cg__dm_id,
            description='Convert Drosophila gene identifiers in CGxxxx format'
            ' to FBgnxxxxxxx format')

    def func__tc_id__dm_id(tc_id_list):
        orthologs = orthology_service.get_tribolium_orthologs(tc_id_list)
        mapping = {o['gene']: o.get('orthologs', []) for o in orthologs}
        for k in mapping:
            mapping[k] = [o['gene'] for o in mapping[k]]
        return mapping

    step__tc_id__dm_id = Step(TC_ID, DM_ID,
            category=CAT_ORTHOLOGY,
            convert_func=func__tc_id__dm_id,
            description='Get Drosophila orthologs for Tribolium genes')


    def func__dm_id__tc_id(dm_id_list):
        orthologs = orthology_service.get_drosophila_orthologs(dm_id_list)
        mapping = {o['gene']: o.get('orthologs', []) for o in orthologs}
        for k in mapping:
            mapping[k] = [o['gene'] for o in mapping[k]]
        return mapping

    step__dm_id__tc_id = Step(DM_ID, TC_ID,
            category=CAT_ORTHOLOGY,
            convert_func=func__dm_id__tc_id,
            description='Get Tribolium orthologs for Drosophila genes')

    return [
        step__dm_id__dm_symbol,
        step__dm_id__dm_name,
        step__dm_id__dm_cg,
        step__dm_symbol__dm_id,
        step__dm_cg__dm_id,
        step__dm_id__tc_id,
        step__tc_id__dm_id,
    ]
