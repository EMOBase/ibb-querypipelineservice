from ibbtools.pipeline.repo import Step
from ibbtools.pipeline.services import geneinfo_service

dict_steps = {
    'tc_id': {
        'tc_symbol': {
            'name': 'TC -> TC symbol',
            'category': 'Gene Alias',
            'description': 'Convert Tribolium gene identifiers in TCxxxxxx format to their corresponding symbol',
        },
        'tc_name': {
            'name': 'TC -> TC name',
            'category': 'Gene Alias',
            'description': 'Convert Tribolium gene identifiers in TCxxxxxx format to their corresponding name',
        },
        'dm_id': {
            'name': 'TC -> FBgn',
            'category': 'Orthology',
            'description': 'Get Drosophila orthologs for Tribolium genes',
        },
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
        'tc_id': {
            'name': 'FBgn -> TC',
            'category': 'Orthology',
            'description': 'Get Tribolium orthologs for Drosophila genes',
        },
        'go_id': {
            'name': 'FBgn -> GO',
            'category': 'Gene Ontology Annotation',
            'description': 'Get GO ID for Drosophila genes',
        },
        'cg_id': {
            'name': 'FBgn -> CG',
            'category': 'Gene Alias',
            'description': 'Convert Drosophila gene identifiers in FBgnxxxxxxx format to CGxxxx format',
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
    'tc_symbol': {
        'tc_id': {
            'name': 'TC symbol -> TC id',
            'category': 'Gene Alias',
            'description': 'Convert Tribolium symbols to their gene identifiers in TCxxxxxx format',
        },
    },
    'dm_symbol': {
        'dm_id': {
            'name': 'FB symbol -> FBgn',
            'category': 'Gene Alias',
            'description': 'Convert Drosophila symbols to their gene identifiers in FBgnxxxxxxx format',
        },
    },
    'cg_id': {
        'dm_id': {
            'name': 'CG -> FBgn',
            'category': 'Gene Alias',
            'description': 'Convert Drosophila gene identifiers in CGxxxx format to FBgnxxxxxxx format',
        },
    },
}

# Input Output
TC_ID = 'TC ID'
TC_SYMBOL = 'TC symbol'
TC_NAME = 'TC name'

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


def func__dm_id__dm_symbol(dm_id_list):
    genes = geneinfo_service.get_drosophila_genes(dm_id_list)
    return {g['id']: [g.get('symbol')] for g in genes}


step__dm_id__dm_symbol = Step(DM_ID, DM_SYMBOL,
        category=CAT_GENE_ALIAS,
        convert_func=func__dm_id__dm_symbol,
        description='Convert Drosophila gene identifiers in FBgnxxxxxxx'
        ' format to their corresponding symbol')


def func__dm_id__dm_name(dm_id_list):
    genes = geneinfo_service.get_drosophila_genes(dm_id_list)
    return {g['id']: [g.get('fullname')] for g in genes}


step__dm_id__dm_name = Step(DM_ID, DM_NAME,
        category=CAT_GENE_ALIAS,
        convert_func=func__dm_id__dm_name,
        description='Convert Drosophila gene identifiers in FBgnxxxxxxx'
        ' format to their corresponding name')



def get_default_steps():
    return [
        step__dm_id__dm_symbol,
        step__dm_id__dm_name,
    ]
