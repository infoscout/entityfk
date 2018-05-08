import sys

import django

if sys.version_info[0] < 3:
    from providers import register_provider, DjangoModelProvider
else:
    from .providers import register_provider, DjangoModelProvider


if django.VERSION < (1, 7):
    register_provider(DjangoModelProvider())
