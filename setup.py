from setuptools import find_packages, setup

with open('VERSION','r') as f:
    version = f.read()
    
setup(name='entityfk',
    packages=find_packages(),  
    description = 'Django app that allows you to easily add a generic foreign key to a django model.',
    url = 'http://github.com/infoscout/entityfk',
    version = version,   
    install_requires=[
        'django>=1.4',
    ],
    tests_require=[
        'mock==1.0.1',
    ],
)

