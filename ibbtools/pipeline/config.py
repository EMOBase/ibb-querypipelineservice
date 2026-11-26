import os

SECRET_KEY = os.environ.get('SECRET_KEY', default='dev')
VERSION = os.environ.get('VERSION', default='latest')
PUBLIC_SERVER = os.environ.get('PUBLIC_SERVER', default='0.0.0.0:5000')

GENOMICSSERVICE_BASE_URL = os.environ.get('GENOMICSSERVICE_BASE_URL',
        'http://genomicsservice:8080')

PHENOTYPESERVICE_BASE_URL = os.environ.get('PHENOTYPESERVICE_BASE_URL',
        'http://phenotypeservice:8080')

# Species used by the iBeetle conversion steps. MAIN_SPECIES is the species the
# iB/TC steps refer to; ORTHOLOG_SPECIES is the reference species for FBgn.
MAIN_SPECIES = os.environ.get('MAIN_SPECIES', default='Tcas')
ORTHOLOG_SPECIES = os.environ.get('ORTHOLOG_SPECIES', default='Dmel')
ORTHOLOGY_SOURCE = os.environ.get('ORTHOLOGY_SOURCE', default='all')

# Optional genomics Database Version. Empty means the configured default.
GENOMICS_VERSION = os.environ.get('GENOMICS_VERSION', default='')

# Gene-ID patterns used to keep only the orthologs from the expected species.
# The genomics /orthology response contains genes from every other species in
# a group, but the pipeline step names only promise Tcas/Dmel conversions.
MAIN_SPECIES_GENE_PATTERN = os.environ.get('MAIN_SPECIES_GENE_PATTERN',
        default=r'^TC\d+$')
ORTHOLOG_SPECIES_GENE_PATTERN = os.environ.get('ORTHOLOG_SPECIES_GENE_PATTERN',
        default=r'^FBgn\d+$')
