from setuptools import find_packages
from isc_ops.setup_tools import setup, current_version

setup(name='entityfk',
    packages=find_packages(),  
    description = 'Django app that allows you to easily add a generic foreign key to a django model.',
    url = 'http://github.com/infoscout/entityfk',
    version = current_version(),   
    install_requires=[
        'django==1.4',
    ]
)

