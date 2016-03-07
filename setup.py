#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from setuptools import find_packages, setup

REQUIRES = [
    'ipaddress>=1.0.14',
    'psutil>=2.1.1',
    'python-dateutil>=2.4.2',
    'python-termstyle>=0.1.10',
    'pytz>=2015.4',
    'redis>=2.10.3',
    'requests>=2.7.0',
    'six>=1.9.0',
]
if sys.version_info[0] == 2:
    REQUIRES += ['dnspython>=1.12.0']
elif sys.version_info[0] == 3:
    REQUIRES += ['dnspython3>=1.12.0']

DATA = [
    ('/opt/intelmq/etc/',
     ['intelmq/bots/BOTS',
      ],
     ),
    ('/opt/intelmq/etc/examples',
     ['intelmq/conf/defaults.conf',
      'intelmq/conf/harmonization.conf',
      'intelmq/conf/pipeline.conf',
      'intelmq/conf/runtime.conf',
      'intelmq/conf/startup.conf',
      'intelmq/conf/system.conf',
      ],
     ),
    ('/opt/intelmq/var/lib/bots/modify/example',
     ['intelmq/bots/experts/modify/modify.conf',
      ],
     ),
]

try:
    import pypandoc
    DESCRIPTION = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    DESCRIPTION = open('README.md').read()


setup(
    name='intelmq',
    version='1.0.0.dev4',
    maintainer='Sebastian Wagner',
    maintainer_email='wagner@cert.at',
    install_requires=REQUIRES,
    test_requires=REQUIRES+[
        'mock>=1.1.1',
        'nose',
        ],
    test_suite='nose.collector',
    packages=find_packages(),
    package_data={'intelmq': [
        'conf/*.conf',
        'bots/BOTS',
        'bots/experts/modify/*.conf',
    ]
    },
    include_package_data=True,
    url='https://github.com/certtools/intelmq/',
    license='AGPLv3',
    description='IntelMQ is a solution for CERTs to process data feeds, '
                'pastebins, tweets throught a message queue.',
    long_description=DESCRIPTION,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Security',
    ],
    keywords='incident handling cert csirt',
    data_files=DATA,
    entry_points={
        'console_scripts': [
            'intelmqctl = intelmq.bin.intelmqctl:main',
            'intelmqdump = intelmq.bin.intelmqdump:main',
            'intelmq_psql_initdb = intelmq.bin.intelmq_psql_initdb:main',
        ],
    },
)
