#!/usr/bin/python3
#
# SPDX-FileCopyrightText: 2014-2021 Tomás Lima, Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later
# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

from setuptools import find_packages, setup

REQUIRES = [
    'dnspython>=1.11.1',
    'psutil>=1.2.1',
    'python-dateutil>=2.5',
    'python-termstyle>=0.1.10',
    'pytz>=2012c',
    'redis>=2.10',
    'requests>=2.2.0',
    'ruamel.yaml',
]

exec(open(os.path.join(os.path.dirname(__file__),
                       'intelmq/version.py')).read())  # defines __version__
BOTS = []

base_path = Path(__file__).parent / 'intelmq/bots'
botfiles = [botfile for botfile in Path(base_path).glob('**/*.py') if botfile.is_file() and not botfile.name.startswith('_')]
for file in botfiles:
    file = Path(str(file).replace(str(base_path), 'intelmq/bots'))
    module = '.'.join(file.with_suffix('').parts)
    BOTS.append('{0} = {0}:BOT.run'.format(module))

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as handle:
    README = handle.read()

setup(
    name='intelmq',
    version=__version__,  # noqa: F821
    maintainer='Sebastian Wagner',
    maintainer_email='wagner@cert.at',
    python_requires='>=3.6',
    install_requires=REQUIRES,
    tests_require=[
        'Cerberus!=1.3',
        'requests_mock',
    ],
    test_suite='intelmq.tests',
    extras_require={
        'development': [
            'Cerberus',
        ],
    },
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/certtools/intelmq/',
    project_urls={
        'Documentation': 'https://intelmq.readthedocs.io/',
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
)
