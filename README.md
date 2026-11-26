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
| `MAIN_SPECIES` | `Tcas` | Main species used by the orthology and dsRNA steps |
| `MAIN_GENE_LABEL` | `TC` | Label for the main-species gene ID in step names and CSV headers |
| `MAIN_SPECIES_GENE_PATTERN` | `^TC\d+$` | Regex used to keep only main-species orthologs |
| `DSRNA_LABEL` | `iB` | Label for dsRNA fragment IDs in step names and CSV headers |
| `LETHALITY_STEPS_ENABLED` | `true` | Include the iBeetle phenotype/lethality steps |
| `ORTHOLOGY_SOURCE` | `OrthoFinder` | Orthology source filter. The legacy pipeline used OrthoFinder; the portal also holds Eggnog6, which groups genes differently |
| `GENOMICS_VERSION` | empty | Fallback genomics Database Version when a request does not send one; empty uses the genomics default |

The reference side is fixed to Dmel for now, so `FBgn`, `FB symbol`, `FB name`
and `CG` are not configurable. `MAIN_GENE_LABEL` and `DSRNA_LABEL` are used in
the step names and CSV headers, e.g. `FBgn -> TC` and `TC -> iB` for the iBeetle
defaults.

Steps that need dsRNA data carry `requires: "dsrna"` in the `/steps` response so
the frontend can hide them when the selected version has no `dsrna.csv`.

`POST /pipelines` accepts an optional `version` form field with the genomics
Database Version to query. This is the value selected in the frontend's version
dropdown; it takes precedence over `GENOMICS_VERSION`. Requests that omit it
fall back to `GENOMICS_VERSION`, then to the genomics default version.

The gene-ID patterns matter because `GET /orthology/{species}` returns genes
from every other species in a group, while the pipeline steps only promise
main-species/Dmel conversions.

