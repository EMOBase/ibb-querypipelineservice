from ibbtools.pipeline.pipeline import generate_row

def test_generate_row():
    queries = ['a1', 'a2', 'a3']
    input_indexes = [0, 0, 2]
    mappings = [
        {'a1': ['b1', 'b2', 'b3']},
        {'a1': ['c1', 'c2'], 'a2': ['c3', 'c4']},
        {'c1': ['d1', 'd2']},
    ]

    expected = [
        ['a1', 'b1', 'c1', 'd1'],
        ['a1', 'b1', 'c1', 'd2'],
        ['a1', 'b1', 'c2', None],
        ['a1', 'b2', 'c1', 'd1'],
        ['a1', 'b2', 'c1', 'd2'],
        ['a1', 'b2', 'c2', None],
        ['a1', 'b3', 'c1', 'd1'],
        ['a1', 'b3', 'c1', 'd2'],
        ['a1', 'b3', 'c2', None],
        ['a2', None, 'c3', None],
        ['a2', None, 'c4', None],
        ['a3', None, None, None],
    ]

    assert list(generate_row(queries, input_indexes, mappings)) == expected
