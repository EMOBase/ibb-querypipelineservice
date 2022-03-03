import os

SECRET_KEY = os.environ.get('SECRET_KEY', default='dev')
VERSION = os.environ.get('VERSION', default='latest')
PUBLIC_SERVER = os.environ.get('PUBLIC_SERVER', default='0.0.0.0:5000')

GENEINFO_SERVICE_BASE_URL = os.environ.get('GENEINFO_SERVICE_BASE_URL',
        'http://ibb-test.vm19002.virt.gwdg.de/ibb/api/geneinfo/v1')

ORTHOLOGY_SERVICE_BASE_URL = os.environ.get('ORTHOLOGY_SERVICE_BASE_URL',
        'http://ibb-test.vm19002.virt.gwdg.de/ibb/api/orthology/v1')
