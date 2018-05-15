# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import find_packages, setup, Command


with open('VERSION', 'r') as f:
    version = f.read().strip()


class TestCommand(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import django
        from django.conf import settings
        from django.core.management import call_command

        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3',
                },
            },
            INSTALLED_APPS=(
                'entityfk',
                'entityfk.tests',
            )
        )
        django.setup()
        call_command('test', 'entityfk')


setup(
    name='entityfk',
    packages=find_packages(),
    description='Django app that allows you to easily add a generic foreign key to a django model.',
    url='http://github.com/infoscout/entityfk',
    version=version,
    install_requires=[
        'six',
        'Django >= 1.8',
    ],
    tests_require=[
        'mock==1.0.1',
    ],
    cmdclass={'test': TestCommand},
)
