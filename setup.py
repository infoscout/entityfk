from setuptools import setup, find_packages

setup(name='entityfk',
    packages=find_packages(),  
    description = 'Django app that allows you to easily add a generic foreign key to a django model.',
    url = 'http://github.com/infoscout/entityfk',
    #version = '0.1a.dev',    
    install_requires=[
        'django==1.4',
    ]
)

