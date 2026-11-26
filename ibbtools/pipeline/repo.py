class StepNotFoundError(Exception):
    def __init__(self, input_, output):
        super().__init__(f'No such step: {input_} -> {output}')


class Step:
    def __init__(self, input, output,
            name=None,
            description=None,
            category=None,
            options=[],
            requires=None,
            convert_func=None):

        self.input = input
        self.output = output
        self.description = description
        self.options = options
        self.category = category
        self.requires = requires
        self.name = name if name else f'{self.input} -> {self.output}'
        self.convert_func = convert_func

    def __repr__(self):
        return f'Step[{self.name}]'


class StepRepo:
    def __init__(self):
        self.mapping = {}

    def add(self, step):
        if (step.input, step.output) in self.mapping:
            raise ValueError(f'{step} already existed')
        if not step.convert_func:
            raise ValueError(f'No convert function found for step {step}')
        self.mapping[(step.input, step.output)] = step

    def add_all(self, steps):
        for step in steps:
            self.add(step)

    def clear(self):
        self.mapping.clear()

    def get(self, input_, output):
        try:
            return self.mapping[(input_, output)]
        except KeyError:
            raise StepNotFoundError(input_, output)


    def get_all(self):
        return self.mapping.values()
