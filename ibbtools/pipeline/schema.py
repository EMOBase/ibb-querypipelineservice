from marshmallow import Schema, fields, post_load
from ibbtools.pipeline.repo import Step


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

    @post_load
    def make_step(self, data, **kwargs):
        return Step(**data)


class PipelineSchema(Schema):
    steps = fields.List(fields.Nested(StepSchema), required=True)
    data = fields.List(fields.Str())
    version = fields.Str()
    file = fields.Str(metadata={'format': 'binary'})
