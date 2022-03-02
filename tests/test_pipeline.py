from ibbtools.pipeline.pipeline import generate_row

def test_generate_row():
    keys = [1, 2]
    mappings = [
        {1:[3,4,9]},
        {3:[5,6], 4:[7,8]}
    ]

    expected = [
        [1, 3, 5],
        [1, 3, 6],
        [1, 4, 7],
        [1, 4, 8],
        [1, 9, None],
        [2, None, None],
    ]

    assert list(generate_row(keys, mappings)) == expected
