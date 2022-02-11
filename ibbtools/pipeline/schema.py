from marshmallow import Schema, fields


class OptionSchema(Schema):
    name = fields.Str(required=True)
    value = fields.Str(required=True)


class StepSchema(Schema):
    input = fields.Str(required=True)
    output = fields.Str(required=True)
    name = fields.Str()
    description = fields.Str()
    category = fields.Str()
    options = fields.List(fields.Nested(OptionSchema))


class PipelineSchema(Schema):
    steps = fields.List(fields.Nested(StepSchema), required=True)
    data = fields.List(fields.Str())
    file = fields.Str(metadata={'format': 'binary'})
