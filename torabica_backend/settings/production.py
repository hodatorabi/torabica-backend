import django_heroku

from torabica_backend.settings.base import *  # NOQA

django_heroku.settings(locals())
