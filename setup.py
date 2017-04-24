#!/usr/bin/env python3
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
    'pytz>=2014.1',
    'redis>=2.10.3',
    'requests>=2.2.0',
]
if sys.version_info < (3, 5):
    REQUIRES.append('typing')


DATA = [
    ('/opt/intelmq/etc/',
     ['intelmq/bots/BOTS',
      ],
     ),
    ('/opt/intelmq/etc/examples',
     ['intelmq/etc/defaults.conf',
      'intelmq/etc/harmonization.conf',
      'intelmq/etc/pipeline.conf',
      'intelmq/etc/runtime.conf',
      ],
     ),
    ('/opt/intelmq/var/log/',
     [],
     ),
    ('/opt/intelmq/var/lib/bots/file-output/',
     [],
     ),
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
    install_requires=REQUIRES,
    test_suite='intelmq.tests',
    packages=find_packages(),
    package_data={'intelmq': [
        'etc/*.conf',
        'bots/BOTS',
        'bots/experts/modify/examples/*.conf',
    ]
    },
    include_package_data=True,
    url='https://github.com/certtools/intelmq/',
    license='AGPLv3',
    description='IntelMQ is a solution for IT security teams for collecting and '
                'processing security feeds using a message queuing protocol.',
    long_description=README,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security',
    ],
    keywords='incident handling cert csirt',
    data_files=DATA,
    entry_points={
        'console_scripts': [
            'intelmqctl = intelmq.bin.intelmqctl:main',
            'intelmqdump = intelmq.bin.intelmqdump:main',
            'intelmq_psql_initdb = intelmq.bin.intelmq_psql_initdb:main',
        ] + BOTS,
    },
    scripts=[
        'intelmq/bots/experts/tor_nodes/update-tor-nodes',
        'intelmq/bots/experts/maxmind_geoip/update-geoip-data',
        'intelmq/bots/experts/asn_lookup/update-asn-data',
    ],
)
