from __future__ import unicode_literals

import sys

from django.apps import AppConfig

if  sys.version_info[0] < 3:
    from providers import register_provider, DjangoModelProvider
else:
    from .providers import register_provider, DjangoModelProvider


class EntityFKConfig(AppConfig):

    name = 'entityfk'

    def ready(self):
        register_provider(DjangoModelProvider())
