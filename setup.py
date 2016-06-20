# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='synclady',
    version='0.0.1',
    description='Make data smarter',
    long_description=readme,
    author='Swaathi Kakarla',
    author_email='swaathi@skcript.com',
    url='http://www.skcript.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': [
            'synclady = synclady.cli:main',
        ],
    },
    install_requires=(
    	['pyyaml'],
        ['logging'],
        ['watchdog'],
        ['observer'],
        ['requests'],
        ['rq'],
        ['redis'],
        ['rratelimit']
    )
)
