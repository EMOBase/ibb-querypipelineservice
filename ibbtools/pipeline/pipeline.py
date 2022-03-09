import io
import csv


class InvalidPipelineError(Exception):
    pass


class PipelineResult:
    def __init__(self, header, rows):
        self.header = header
        self.rows = rows


    def to_csv(self):
        result = io.StringIO()
        writer = csv.writer(result)

        writer.writerow(self.header)
        writer.writerows(self.rows)

        return result.getvalue()


class Pipeline:
    def __init__(self, steps):
        try:
            input_labels = [steps[0].input] + [s.output for s in steps]
            input_indexes = [find_last_index(input_labels[:i+1], s.input)
                for i, s in enumerate(steps)]

        except ValueError as e:
            raise InvalidPipelineError(f'"{e}" must exist in previous steps' )


        self.steps = steps
        self.__input_indexes = input_indexes


    def execute(self, initial_input):
        input_data = [set(initial_input)]
        mappings = []

        for i, step in zip(self.__input_indexes, self.steps):
            input_ = input_data[i]
            output = step.convert_func(input_) if input_ else {}
            mappings.append(output)

            uniq_values = set(v for values in output.values() for v in values)
            input_data.append(uniq_values)


        header = [self.steps[0].input] + [s.name for s in self.steps]
        return PipelineResult(header,
                generate_row(initial_input, self.__input_indexes, mappings))



def find_last_index(list_, item):
    """
    Find index of the last occurrence of the item
    """

    return len(list_) - 1 - list_[::-1].index(item)


def generate_row(queries, input_indexes, mappings, i=0, current_row=[]):
    """
    Backtracking algorithm to generate rows from mappings
        A -> [B], A -> [C], C -> [D] ...

    The number of columns equals the number of mappings plus 1

    Params:
        - queries: starting values
        - input_indexes: index of the input in the row for the current mapping
        - mappings: list of mappings from string to list of strings.
            The value `None` should not be the key in any mapping

    For example:
        Input:  queries = [a1, a2, a3]
                input_indexes = [0, 0, 2]
                mappings = [
                    {a1: [b1, b2, b3]},
                    {a1: [c1, c2], a2: [c3, c4]},
                    {c1: [d1, d2]},
                ]

        Output:
                a1 b1 c1 d1
                a1 b1 c1 d2
                a1 b1 c2 None
                a1 b2 c1 d1
                a1 b2 c1 d2
                a1 b2 c2 None
                a1 b3 c1 d1
                a1 b3 c1 d2
                a1 b3 c2 None
                a2 None c3 None
                a2 None c4 None
                a3 None None None
    """

    for query in queries:
        current_row.append(query)
        if i == len(mappings):
            yield current_row.copy()
        else:
            key = current_row[input_indexes[i]]
            values = mappings[i].get(key)
            if not values: #Also handle empty list
                values = [None]

            yield from generate_row(values, input_indexes, mappings,
                i+1, current_row)
        current_row.pop()
