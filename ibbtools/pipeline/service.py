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
            'description': 'Convert Tribolium gene in TCxxxxxx format to its corresponding gene symbol',
        },
        'tc_name': {
            'name': 'TC -> TC name',
        },
        'dm_id': {
            'name': 'TC -> FBgn',
        },
        'go_id': {
            'name': 'TC -> GO ID',
        },
        'ib_id': {
            'name': 'TC -> iB',
        },
    },
    'dm_id': {
        'dm_symbol': {
            'name': 'FBgn -> FB symbol',
        },
        'dm_name': {
            'name': 'FBgn -> FB name',
        },
        'tc_id': {
            'name': 'FBgn -> TC',
        },
        'go_id': {
            'name': 'FBgn -> GO',
        },
        'cg_id': {
            'name': 'FBgn -> CG',
        },
    },
    'go_id': {
        'go_aspect': {
            'name': 'GO ID -> GO aspect',
        },
        'go_term': {
            'name': 'GO ID -> GO term',
        },
        'tc_id': {
            'name': 'GO ID -> TC',
        },
        'dm_id': {
            'name': 'GO ID -> FBgn',
        },
    },
    'ib_id': {
        'tc_id': {
            'name': 'iB -> TC',
        },
        'larval_lethality_11': {
            'name': 'iB -> larval lethality day 11',
        },
        'larval_lethality_22': {
            'name': 'iB -> larval lethality day 22',
        },
        'pupal_lethality_11': {
            'name': 'iB -> pupal lethality day 11',
        },
    },
    'tc_symbol': {
        'tc_id': {
            'name': 'TC symbol -> TC id',
        },
    },
    'dm_symbol': {
        'dm_id': {
            'name': 'FB symbol -> FBgn',
        },
    },
    'cg_id': {
        'dm_id': {
            'name': 'CG -> FBgn'
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
            }


def execute(steps, initial_input):
    headers, mappings = [], []
    inputs = [set(initial_input)]

    for step in steps:
        try:
            key_input = step['input']
            key_output = step['output']
        except KeyError:
            raise InvalidPipelineError('Malformated json for steps')

        headers.append(key_input)

        try:
            func = get_convert_func(key_input, key_output)
        except KeyError:
            raise InvalidPipelineError(f'No such step: {key_input} -> {key_output}')


        try:
            # Find last occurence of key_input
            input_idx = len(headers) - 1 - headers[::-1].index(key_input)
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
