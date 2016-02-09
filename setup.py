#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup


DIRS = ['/opt/intelmq/bin',
        '/opt/intelmq/docs',
        '/opt/intelmq/etc/examples',
        '/opt/intelmq/var/lib/bots',
        '/opt/intelmq/var/lib/bots/file-output',
        '/opt/intelmq/var/lib/bots/modify/example/',
        '/opt/intelmq/var/log',
        '/opt/intelmq/var/run',
        ]
DATA = [('/opt/intelmq/etc/', [
                           'intelmq/bots/BOTS',
                           ],
         ),
        ('/opt/intelmq/etc/examples', [
                           'intelmq/conf/defaults.conf',
                           'intelmq/conf/harmonization.conf',
                           'intelmq/conf/pipeline.conf',
                           'intelmq/conf/runtime.conf',
                           'intelmq/conf/startup.conf',
                           'intelmq/conf/system.conf',
                          ],
         ),
        ('/opt/intelmq/bin/', [
                           'intelmq/bin/intelmqctl',
                           'intelmq/bin/intelmqdump',
                           'intelmq/bin/intelmq_gen_harm_docs.py',
                           'intelmq/bin/intelmq_psql_initdb.py',
                          ],
         ),
        ('/opt/intelmq/var/lib/bots/modify/example', [
                           'intelmq/bots/experts/modify/modify.conf',
                          ],
         ),
        ]
if 'TRAVIS' in os.environ:
    DATA = []
else:
    for dir in DIRS:
        if not os.path.exists(dir):
            os.makedirs(dir)


setup(
    name='intelmq',
    version='1.0.0.dev1',
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
    url='https://github.com/certtools/intelmq/',
    license='AGPLv3',
    description="IntelMQ Tool",
    long_description='IntelMQ is a solution for CERTs to process data feeds, '
                     'pastebins, tweets throught a message queue.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: License :: OSI Approved :: GNU Affero General Public License v3',
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
)
