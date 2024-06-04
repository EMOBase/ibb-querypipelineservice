import os

SECRET_KEY = os.environ.get('SECRET_KEY', default='dev')
VERSION = os.environ.get('VERSION', default='latest')
PUBLIC_SERVER = os.environ.get('PUBLIC_SERVER', default='0.0.0.0:5000')

GENESERVICE_BASE_URL = os.environ.get('GENESERVICE_BASE_URL',
        'http://geneservice:8080')

PHENOTYPESERVICE_BASE_URL = os.environ.get('PHENOTYPESERVICE_BASE_URL',
        'http://phenotypeservice:8080')
