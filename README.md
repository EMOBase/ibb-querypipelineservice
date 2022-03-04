# ibbtools.pipeline

## Development

Commands

```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
flask run
```

To add a new step and make it available in the query pipeline, edit 
`ibbtools/pipeline/default_steps.py`:

1. Create a new convert function which accepts a `list` of input strings and
returns a `dict`. The values of the dict are lists of output values for the
corresponding input. The datatype `list` must be used even though the
relationship is 1-to-1 mapping. To indicate there are no mapped values for an
input, either exclude the input or use `None`, `[]`, `[None]` as the output.

2. Create a new instance of `Step` with the newly-created convert function
and proper attributes (input, output, description, category)

3. Add the step to the returned list of the `get_default_steps` function

## Environment variables

These variables must be set especially in production

- `GENEINFO_SERVICE_BASE_URL`
- `ORTHOLOGY_SERVICE_BASE_URL`
- `GENESILENCING_SERVICE_BASE_URL`
- `PUBLIC_SERVER`: the base url of this service which is accessible from
outside of proxy (if any) to be included in OpenAPI document
