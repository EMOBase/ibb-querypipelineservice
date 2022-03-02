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
        'dm_symbol': {
            'name': 'FBgn -> FB symbol',
            'category': 'Gene Alias',
            'description': 'Convert Drosophila gene identifiers in FBgnxxxxxxx format to their corresponding symbol',
        },
        'dm_name': {
            'name': 'FBgn -> FB name',
            'category': 'Gene Alias',
            'description': 'Convert Drosophila gene identifiers in FBgnxxxxxxx format to their corresponding name',
        },
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
