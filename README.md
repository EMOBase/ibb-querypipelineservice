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

## Configuration

The service reads these environment variables:

| Variable | Default | Description |
| --- | --- | --- |
| `GENOMICSSERVICE_BASE_URL` | `http://genomicsservice:8080` | Base URL on which `/genes/...`, `/orthology/...` and `/silencingseqs/...` are served. Include the portal prefix when calling through the portal, e.g. `https://portal.example.com/api/genomicsservice/v1` |
| `PHENOTYPESERVICE_BASE_URL` | `http://phenotypeservice:8080` | Base URL of the iBeetle phenotype service |
| `MAIN_SPECIES` | `Tcas` | Species used by the `TC` and `iB` steps |
| `ORTHOLOG_SPECIES` | `Dmel` | Reference species used by the `FBgn` steps |
| `ORTHOLOGY_SOURCE` | `all` | Orthology source filter, e.g. `OrthoFinder` or `all` |
| `GENOMICS_VERSION` | empty | Fallback genomics Database Version when a request does not send one; empty uses the genomics default |
| `MAIN_SPECIES_GENE_PATTERN` | `^TC\d+$` | Regex used to keep only main-species orthologs |
| `ORTHOLOG_SPECIES_GENE_PATTERN` | `^FBgn\d+$` | Regex used to keep only reference-species orthologs |

`POST /pipelines` accepts an optional `version` form field or query parameter
with the genomics Database Version to query. This is the value selected in the
frontend's version dropdown; it takes precedence over `GENOMICS_VERSION`.
Requests that omit it fall back to `GENOMICS_VERSION`, then to the genomics
default version.

The gene-ID patterns matter because `GET /orthology/{species}` returns genes
from every other species in a group, while the pipeline steps only promise
Tcas/Dmel conversions.

