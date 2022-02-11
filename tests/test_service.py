import io
import csv

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

    csv_string = io.StringIO(service.execute(steps, data))
    reader = csv.reader(csv_string)

    headers = next(reader)
    assert headers == ['a', 'b', 'b', 'a', 'e']

    rows = list(reader)
    assert len(rows) == 2
