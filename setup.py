#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import sys

from setuptools import find_packages, setup

REQUIRES = [
    'dnspython>=1.11.1',
    'psutil>=1.2.1',
    'python-dateutil>=2.5',
    'python-termstyle>=0.1.10',
    'pytz>=2012c',
    'redis>=2.10',
    'requests>=2.2.0',
]

exec(open(os.path.join(os.path.dirname(__file__),
                       'intelmq/version.py')).read())  # defines __version__
BOTS = []
bots = json.load(open(os.path.join(os.path.dirname(__file__), 'intelmq/bots/BOTS')))
for bot_type, bots in bots.items():
    for bot_name, bot in bots.items():
        module = bot['module']
        BOTS.append('{0} = {0}:BOT.run'.format(module))

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as handle:
    README = handle.read().replace('<docs/',
                                   '<https://github.com/certtools/intelmq/blob/master/docs/')

setup(
    name='intelmq',
    version=__version__,
    maintainer='Sebastian Wagner',
    maintainer_email='wagner@cert.at',
    python_requires='>=3.5',
    install_requires=REQUIRES,
    tests_require=[
        'Cerberus!=1.3',
        'pyyaml',
    ],
    test_suite='intelmq.tests',
    extras_require={
        'development': [
            'Cerberus',
            'pyyaml',
        ],
    },
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/certtools/intelmq/',
    project_urls={
        'Travis CI': 'https://travis-ci.org/certtools/intelmq',
        'Documentation': 'https://github.com/certtools/intelmq/blob/master/docs/',
        'Source and Issue Tracker': 'https://github.com/certtools/intelmq/',
    },
    license='AGPLv3',
    description='IntelMQ is a solution for IT security teams for collecting and '
                'processing security feeds using a message queuing protocol.',
    long_description=README,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Security',
    ],
    keywords='incident handling cert csirt',
    entry_points={
        'console_scripts': [
            'intelmqctl = intelmq.bin.intelmqctl:main',
            'intelmqdump = intelmq.bin.intelmqdump:main',
            'intelmq_psql_initdb = intelmq.bin.intelmq_psql_initdb:main',
            'intelmq.bots.experts.sieve.validator = intelmq.bots.experts.sieve.validator:main',
            'intelmqsetup = intelmq.bin.intelmqsetup:main',
        ] + BOTS,
    },
    scripts=[
        'intelmq/bots/experts/tor_nodes/update-tor-nodes',
        'intelmq/bots/experts/maxmind_geoip/update-geoip-data',
        'intelmq/bots/experts/asn_lookup/update-asn-data',
        'intelmq/bots/experts/recordedfuture_iprisk/update-rfiprisk-data',
    ],
)
