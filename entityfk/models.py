# Empty, file required if running django tests

from entityfk.providers import register_provider, DjangoModelProvider
register_provider(DjangoModelProvider())