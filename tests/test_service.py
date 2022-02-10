import ibbtools.pipeline.service as service


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

    assert list(service.generate_row(keys, mappings)) == expected


def test_execute():
    steps = [
        {'input': 'a', 'output': 'b'},
        {'input': 'b', 'output': 'c'},
        {'input': 'b', 'output': 'd'},
        {'input': 'a', 'output': 'e'},
    ]

    data = [1, 2]

    expected = 'a,b,c,d,e\r\n1,1,1,1,1\r\n2,2,2,2,2'
    assert service.execute(steps, data) == expected
