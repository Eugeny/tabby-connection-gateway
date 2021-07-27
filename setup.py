#!/usr/bin/env python
from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['websockets>=9.1']

setup(
    name='tabby-connection-gateway',
    version='0.2.2',
    author='Eugene Pankov',
    author_email='e@ajenti.org',
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'tabby-connection-gateway=tabby_connection_gateway.cli:main',
        ],
    },
    install_requires=requirements,
    license='MIT license',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='tabby',
    packages=['tabby_connection_gateway'],
    url='https://github.com/eugeny/tabby-connection-gateway',
)
