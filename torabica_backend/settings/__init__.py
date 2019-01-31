from decouple import config

if config('DEBUG', cast=bool, default=True):
    from torabica_backend.settings.base import *  # NOQA
else:
    from torabica_backend.settings.production import *  # NOQA
