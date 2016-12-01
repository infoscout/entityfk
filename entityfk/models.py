# Empty, file required if running django tests

from providers import register_provider, DjangoModelProvider
register_provider(DjangoModelProvider())
