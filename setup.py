# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import Command, find_packages, setup


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
    description=(
        "Django app that allows you to easily add a generic foreign key"
        "to a django model."
    ),
    url='http://github.com/infoscout/entityfk',
    version=version,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.2',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
    ],
    install_requires=[
        'six',
        'Django >= 1.8, < 5.0',
    ],
    tests_require=[
        'mock==1.0.1',
    ],
    cmdclass={'test': TestCommand},
)
