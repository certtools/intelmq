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
    version='0.0.9',
    maintainer='Tomas Lima',
    maintainer_email='synchroack@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/intelmq/',
    license='GPLv3',
    description="IntelMQ Tool",
    long_description='IntelMQ is a solution for CERTs to process data feeds, pastebins, tweets throught a message queue.',
    package_data={
                  '/opt/intelmq/docs': [
                            'LICENSE',
                            'README.md',
                            'CONTRIBUTORS.md'
                        ]
                 },
    data_files=[
                ('/opt/intelmq/etc/', [
                                   'intelmq/bots/BOTS',
                                   'intelmq/conf/startup.conf',
                                   'intelmq/conf/runtime.conf',
                                   'intelmq/conf/pipeline.conf',
                                   'intelmq/conf/system.conf'
                                  ]
                ),
                ('/opt/intelmq/bin/', [
                                   'intelmq/bin/intelmqctl'
                                  ]
                ),
                ('/opt/intelmq/docs/', [
                                   'docs/UserGuide.md',
                                   'docs/DevGuide.md',
                                   'docs/DataHarmonization.md'
                                  ]
                )
    ],
    install_requires=[
        "python-dateutil==1.5",
        "geoip2==0.5.1",
        "dnspython==1.11.1",
        "redis==2.10.3",
        "pymongo==2.7.1",
        "xmpppy==0.5.0rc1",
        "imbox==0.5.5",
        "unicodecsv==0.9.4",
        "pytz==2012d",
        "psutil==2.1.1"
    ],
)

