""" Production Settings """
# default: use settings from main settings.py if not overwritten
from .settings import *

import django_heroku


DEBUG = False
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)
# adjust to the URL of your Heroku app
ALLOWED_HOSTS = ['cs-skilltracker.herokuapp.com']

COMPRESS_OFFLINE = True
LIBSASS_OUTPUT_STYLE = 'compressed'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Activate Django-Heroku.
django_heroku.settings(locals())