from __future__ import unicode_literals

from django.apps import AppConfig

from providers import register_provider, DjangoModelProvider


class EntityFKConfig(AppConfig):

    name = 'entityfk'

    def ready(self):
        register_provider(DjangoModelProvider())
