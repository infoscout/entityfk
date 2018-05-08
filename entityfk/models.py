import django

from entityfk.providers import register_provider, DjangoModelProvider


if django.VERSION < (1, 7):
    register_provider(DjangoModelProvider())
