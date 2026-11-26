import os

SECRET_KEY = os.environ.get('SECRET_KEY', default='dev')
VERSION = os.environ.get('VERSION', default='latest')
PUBLIC_SERVER = os.environ.get('PUBLIC_SERVER', default='0.0.0.0:5000')

GENOMICSSERVICE_BASE_URL = os.environ.get('GENOMICSSERVICE_BASE_URL',
        'http://genomicsservice:8080')

PHENOTYPESERVICE_BASE_URL = os.environ.get('PHENOTYPESERVICE_BASE_URL',
        'http://phenotypeservice:8080')

# Species used by the iBeetle conversion steps. The reference side is fixed to
# Dmel for now; MAIN_SPECIES is the species the iB/TC steps refer to.
REFERENCE_SPECIES = 'Dmel'
REFERENCE_SPECIES_GENE_PATTERN = r'^FBgn\d+$'

MAIN_SPECIES = os.environ.get('MAIN_SPECIES', default='Tcas')
MAIN_GENE_LABEL = os.environ.get('MAIN_GENE_LABEL', default='TC')
MAIN_SPECIES_GENE_PATTERN = os.environ.get('MAIN_SPECIES_GENE_PATTERN',
        default=r'^TC\d+$')
DSRNA_LABEL = os.environ.get('DSRNA_LABEL', default='iB')
LETHALITY_STEPS_ENABLED = os.environ.get('LETHALITY_STEPS_ENABLED',
        default='true')

# The legacy pipeline used the OrthoFinder source; the portal can also hold
# Eggnog6 orthology, which groups genes differently and changes the output.
ORTHOLOGY_SOURCE = os.environ.get('ORTHOLOGY_SOURCE', default='OrthoFinder')
