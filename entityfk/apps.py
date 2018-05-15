# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from .providers import DjangoModelProvider, register_provider


class EntityFKConfig(AppConfig):

    name = 'entityfk'

    def ready(self):
        register_provider(DjangoModelProvider())
