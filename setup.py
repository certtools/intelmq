import os
import pwd
import grp
import sys
import stat
from setuptools import setup, find_packages


try:
    uid = pwd.getpwnam("intelmq").pw_uid
    gid = grp.getgrnam("intelmq").gr_gid
except:
    print "\nPlease, read intelmq documentation and create 'intelmq' user.\n"
    sys.exit()


dirs = [
        '/opt/intelmq',
        '/opt/intelmq/etc/',
        '/opt/intelmq/etc/bots/',
        '/opt/intelmq/var/',
        '/opt/intelmq/var/log/',
        '/opt/intelmq/var/run',
        '/opt/intelmq/bin',
        '/opt/intelmq/docs'
       ]

files = [
        '/opt/intelmq/etc/BOTS',
        '/opt/intelmq/etc/system.conf',
        '/opt/intelmq/etc/startup.conf',
        '/opt/intelmq/etc/runtime.conf',
        '/opt/intelmq/etc/pipeline.conf',
       ]

for dir in dirs:
    if not os.path.exists(dir):
        os.makedirs(dir)
        os.chown(dir, uid, gid)
        os.chmod(dir, 0770)
        

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


for file in files:
    os.chmod(file, 0770)
    os.chown(file, uid, gid)
