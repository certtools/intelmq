#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys

from setuptools import find_packages, setup


if sys.version[0] == '2':
    input = raw_input

if os.path.isdir("/opt/intelmq"):
    print()
    print("IntelMQ seems to be already installed due the existence of "
          "/opt/intelmq directory. If you continue the directory will be"
          " overwritten.")
    answer = input("Do you want to proceed? [y/N] ")
    if answer.lower().strip() != "y":
        sys.exit(-1)

dirs = ['/opt/intelmq',
        '/opt/intelmq/bin',
        '/opt/intelmq/docs',
        '/opt/intelmq/etc',
        '/opt/intelmq/var',
        '/opt/intelmq/var/lib',
        '/opt/intelmq/var/lib/bots',
        '/opt/intelmq/var/lib/bots/file-output',
        '/opt/intelmq/var/lib/bots/modify',
        '/opt/intelmq/var/log',
        '/opt/intelmq/var/run',
        ]

for dir in dirs:
    if not os.path.exists(dir):
        os.makedirs(dir)


setup(
    name='intelmq',
    version='1.0.0',
    maintainer='Tomas Lima',
    maintainer_email='synchroack@gmail.com',
    install_requires=[
       'ipaddress>=1.0.14',
       'psutil>=2.1.1',
       'python-dateutil>=2.4.2',
       'pytz>=2015.4',
       'redis>=2.10.3',
       'requests>=2.7.0',
       'six>=1.9.0',
    ],
    packages=find_packages(),
    package_data={'intelmq': ['conf/*.conf', 'bots/experts/modify/*.conf']},
    url='http://pypi.python.org/pypi/intelmq/',
    license='AGPLv3',
    description="IntelMQ Tool",
    long_description='IntelMQ is a solution for CERTs to process data feeds, '
                     'pastebins, tweets throught a message queue.',
    data_files=[
                ('/opt/intelmq/etc/', [
                                   'intelmq/bots/BOTS',
                                   'intelmq/conf/defaults.conf',
                                   'intelmq/conf/harmonization.conf',
                                   'intelmq/conf/pipeline.conf',
                                   'intelmq/conf/runtime.conf',
                                   'intelmq/conf/squelcher.conf',
                                   'intelmq/conf/startup.conf',
                                   'intelmq/conf/system.conf',
                                  ],
                 ),
                ('/opt/intelmq/bin/', [
                                   'intelmq/bin/intelmqcli',
                                   'intelmq/bin/intelmqctl',
                                   'intelmq/bin/intelmqdump',
                                   'intelmq/bin/intelmq_gen_harm_docs.py',
                                   'intelmq/bin/intelmq_psql_initdb.py',
                                  ],
                 ),
                ('/opt/intelmq/var/lib/bots/modify/', [
                                   'intelmq/bots/experts/modify/modify.conf',
                                  ],
                 ),
    ],
)
