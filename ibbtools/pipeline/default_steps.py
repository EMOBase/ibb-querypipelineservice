from ibbtools.pipeline.repo import Step

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


def func__tc_id__tc_symbol(tc_id_list):
    pass

step__tc_id__tc_symbol = Step(TC_ID, TC_SYMBOL,
        category=CAT_GENE_ALIAS,
        convert_func=func__tc_id__tc_symbol,
        description='Convert Tribolium gene identifiers in TCxxxxxx format'
        'to their corresponding symbol')


def get_default_steps():
    return [
        step__tc_id__tc_symbol,
    ]
