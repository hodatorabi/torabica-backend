from decouple import config

DEBUG = config('DEBUG', cast=bool, default=True)

if DEBUG:
    from torabica_backend.settings.base import *  # NOQA
else:
    from torabica_backend.settings.production import *  # NOQA
