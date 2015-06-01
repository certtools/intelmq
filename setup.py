import os
import sys
import time
from setuptools import setup, find_packages

if os.path.isdir("/opt/intelmq"):
    print
    print "IntelMQ seems to be already installed due the existence of /opt/intelmq directory. If you continue the directory will be overwritten."
    answer = raw_input("Do you want to proceed? [y/N] ")
    if answer != "Y" and answer != "y":
        sys.exit(-1)

dirs = [
        '/opt/intelmq',
        '/opt/intelmq/etc',
        '/opt/intelmq/var',
        '/opt/intelmq/var/log',
        '/opt/intelmq/var/run',
        '/opt/intelmq/var/lib',
        '/opt/intelmq/var/lib/bots',
        '/opt/intelmq/var/lib/bots/file-output',
        '/opt/intelmq/bin',
        '/opt/intelmq/docs'
       ]

for dir in dirs:
    if not os.path.exists(dir):
        os.makedirs(dir)
        

setup(
    name='intelmq',
    version='1.0.0',
    maintainer='Tomas Lima',
    maintainer_email='synchroack@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/intelmq/',
    license='GPLv3',
    description="IntelMQ Tool",
    long_description='IntelMQ is a solution for CERTs to process data feeds, pastebins, tweets throught a message queue.',
    data_files=[
                ('/opt/intelmq/etc/', [
                                   'intelmq/bots/BOTS',
                                   'intelmq/conf/startup.conf',
                                   'intelmq/conf/runtime.conf',
                                   'intelmq/conf/defaults.conf',
                                   'intelmq/conf/pipeline.conf',
                                   'intelmq/conf/system.conf',
                                   'intelmq/conf/harmonization.conf'
                                  ]
                ),
                ('/opt/intelmq/bin/', [
                                   'intelmq/bin/intelmqctl'
                                  ]
                )
    ]
)

