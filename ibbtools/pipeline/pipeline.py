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

        if not steps:
            raise InvalidPipelineError('No steps')

        try:
            input_labels = [steps[0].input] + [s.output for s in steps]
            input_indexes = [find_last_index(input_labels[:i+1], s.input)
                for i, s in enumerate(steps)]

        except ValueError as e:
            raise InvalidPipelineError(f'"{e}" must exist in previous steps' )


        self.steps = steps
        self.__input_indexes = input_indexes


    def execute(self, initial_input):
        if not initial_input:
            raise InvalidPipelineError('No data')

        input_data = [set(initial_input)]
        mappings = []

        for i, step in zip(self.__input_indexes, self.steps):
            input_ = input_data[i]
            output = step.convert_func(input_)
            mappings.append(output)

            # input -> output = [i] -> { i: [o] }
            uniq_values = set(v for values in output.values() for v in values)
            input_data.append(uniq_values)


        header = [self.steps[0].input] + [s.name for s in self.steps]
        return PipelineResult(header, generate_row(initial_input, mappings))



def find_last_index(list_, item):
    """
    Find index of the last occurrence of the item
    """

    return len(list_) - 1 - list_[::-1].index(item)


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
