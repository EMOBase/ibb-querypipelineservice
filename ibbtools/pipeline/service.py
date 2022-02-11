import os
import io
import csv


def step_tc_id__tc_name(list_tc_id):
    pass


def step_tc_id__tc_symbol(list_tc_id):
    pass



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


def get_convert_func(key_input, key_output):
    return lambda list_: {k: [k] for k in list_}
    # return dict_steps[key_input][key_output].get('func', globals()[f'step_{key_input}__{key_output}'])


def get_steps():
    for key_input in dict_steps:
        for key_output in dict_steps[key_input]:
            step = dict_steps[key_input][key_output]

            try:
                get_convert_func(key_input, key_output)
            except KeyError:
                continue

            yield {
                'input': key_input,
                'output': key_output,
                'name': step.get('name', f'{key_input} -> {key_output}'),
                'options': step.get('options', []),
                'description': step.get('description'),
                'category': step.get('category'),
            }


def execute(steps, initial_input):
    headers, mappings, input_labels = [], [], []
    inputs = [set(initial_input)]

    for step in steps:
        try:
            key_input = step['input']
            key_output = step['output']
        except KeyError:
            raise InvalidPipelineError('Malformated json for steps')

        input_labels.append(key_input)
        headers.append(key_input)

        try:
            func = get_convert_func(key_input, key_output)
        except KeyError:
            raise InvalidPipelineError(f'No such step: {key_input} -> {key_output}')


        try:
            # Find last occurence of key_input
            input_idx = len(input_labels) - 1 - input_labels[::-1].index(key_input)
        except IndexError:
            raise InvalidPipelineError(f'"{key_input}" must exist in previous steps' )


        input_ = inputs[input_idx]
        output = func(input_)

        # input -> output = [i] -> { i: [o] }
        uniq_values = set(v for values in output.values() for v in values)

        inputs.append(uniq_values)
        mappings.append(output)

    headers.append(key_output)

    # Convert to csv format
    result = io.StringIO()
    writer = csv.writer(result)
    writer.writerow(headers)
    writer.writerows(generate_row(initial_input, mappings))

    return result.getvalue()


def generate_row(keys, mappings, i=0, current_row=[]):
    """
    Backtracking algorithm to generate rows from mappings a -> [b], b -> [c] ...
    The value `None` should not be the key in any mapping

    For example:
        Input:  keys = [1, 2]
                mappings = [ {1:[3,4,9]},    {3:[5,6], 4:[7,8]} ]

        Output:
                1 3 5
                1 3 6
                1 4 7
                1 4 8
                1 9 None
                2 None None
    """
    for key in keys:
        current_row.append(key)
        if i == len(mappings):
            yield current_row.copy()
        else:
            values = mappings[i].get(key, [None])
            yield from generate_row(values, mappings, i+1, current_row)
        current_row.pop()


class InvalidPipelineError(Exception):
    pass
