#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

REQUIRES = [
    'dnspython3>=1.11.1',
    'psutil>=1.2.1',
    'python-dateutil>=2.0',
    'python-termstyle>=0.1.10',
    'pytz>=2014.1',
    'redis>=2.10.3',
    'requests>=2.7.0',
    'tabulate>=0.7.5',
]

DATA = [
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
      'intelmq/etc/system.conf',
      'intelmq/etc/squelcher.conf',
      ],
     ),
    ('/opt/intelmq/var/lib/bots/modify/example',
     ['intelmq/bots/experts/modify/modify.conf',
      ],
     ),
    ('/opt/intelmq/var/log/',
     [],
     ),
    ('/opt/intelmq/var/lib/bots/file-output/',
     [],
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
    long_description=DESCRIPTION,
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
            'intelmqctl = intelmq.bin.intelmqctl:main',
            'intelmqdump = intelmq.bin.intelmqdump:main',
            'intelmq_psql_initdb = intelmq.bin.intelmq_psql_initdb:main',
        ],
    },
)
