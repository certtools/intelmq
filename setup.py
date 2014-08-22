import os
from setuptools import setup, find_packages

dirs = [
        '/etc/intelmq',
        '/var/log/intelmq',
        '/var/run/intelmq',
        '/var/lib/intelmq',
        '/var/lib/intelmq/archive/'
       ]

for dir in dirs:
    if not os.path.exists(dir):
        os.makedirs(dir)

setup(
    name='intelmq',
    version='0.0.9',
    maintainer='Tomas Lima',
    maintainer_email='tomas.lima@cert.pt',
    packages=find_packages(),
    scripts=['intelmq/bin/intelmqctl'],
    url='http://pypi.python.org/pypi/intelmq/',
    license='GPLv3',
    description="IntelMQ Tool",
    long_description='IntelMQ is a solution for CERTs to process data feeds, pastebins, tweets throught a message queue.',
    package_data={
                    '': [
                            'LICENSE',
                            'README.md',
                            'CONTRIBUTORS.md'
                        ]
                 },
    data_files=[
                ('/etc/intelmq/', [
                                   'intelmq/conf/startup.conf',
                                   'intelmq/conf/runtime.conf',
                                   'intelmq/conf/pipeline.conf',
                                   'intelmq/conf/system.conf'
                                  ]
                )
    ],
    install_requires=[
        "pika==0.9.14",
        "python-dateutil==1.5",
        "geoip2==0.5.1",
        "dnspython==1.11.1",
        "redis==2.4.9",
        "pymongo==2.7.1",
        "xmpppy==0.5.0rc1",
        "imbox==0.5.5",
        "unicodecsv==0.9.4",
        "pytz==2012d",
        "psutil==2.1.1"
    ],
)
