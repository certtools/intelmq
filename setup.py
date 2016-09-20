#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

REQUIRES = [
    'dnspython>=1.11.1',
    'psutil>=1.2.1',
    'python-dateutil>=2.0',
    'python-termstyle>=0.1.10',
    'pytz>=2014.1',
    'redis>=2.10.3',
    'requests>=2.7.0',
    'tabulate>=0.7.5',
    'rt>=1.0.9',
]

DATA = [
    ('/etc/intelmq/',
     ['intelmq/etc/intelmqcli.conf',
      ],
     ),
    ('/opt/intelmq/etc/',
     ['intelmq/bots/BOTS',
      ],
     ),
    ('/opt/intelmq/etc/examples',
     ['intelmq/etc/defaults.conf',
      'intelmq/etc/harmonization.conf',
      'intelmq/etc/intelmqcli.conf',
      'intelmq/etc/pipeline.conf',
      'intelmq/etc/runtime.conf',
      'intelmq/etc/startup.conf',
      'intelmq/etc/squelcher.conf',
      ],
     ),
    ('/opt/intelmq/var/lib/bots/modify/example',
     ['intelmq/bots/experts/modify/examples/default.conf',
      'intelmq/bots/experts/modify/examples/morefeeds.conf',
      ],
     ),
    ('/opt/intelmq/var/log/',
     [],
     ),
    ('/opt/intelmq/var/lib/bots/file-output/',
     [],
     ),
]

exec(open('intelmq/version.py').read())  # defines __version__


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
        'bots/experts/modify/*.conf',
    ]
    },
    include_package_data=True,
    url='https://github.com/certtools/intelmq/',
    license='AGPLv3',
    description='IntelMQ is a solution for CERTs to process data feeds, '
                'pastebins, tweets throught a message queue.',
    long_description=open('docs/README.rst').read(),
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
        'Topic :: Security',
    ],
    keywords='incident handling cert csirt',
    data_files=DATA,
    entry_points={
        'console_scripts': [
            'intelmqcli = intelmq.bin.intelmqcli:main',
            'intelmqcli_create_reports = intelmq.bin.intelmqcli_create_reports:main',
            'intelmqctl = intelmq.bin.intelmqctl:main',
            'intelmqdump = intelmq.bin.intelmqdump:main',
            'intelmq_psql_initdb = intelmq.bin.intelmq_psql_initdb:main',
        ],
    },
    scripts=[
        'intelmq/bots/experts/tor_nodes/update-tor-nodes',
        'intelmq/bots/experts/maxmind_geoip/update-geoip-data',
        'intelmq/bots/experts/asn_lookup/update-asn-data',
    ],
)
