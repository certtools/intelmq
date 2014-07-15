from setuptools import setup

setup(
    name='intelmq',
    version='0.1.0',
    maintainer='Tomas Lima',
    maintainer_email='tomas.lima@cert.pt',
    packages=[
                  'intelmq',
                  'intelmq.lib',
                  'intelmq.bots',
                  'intelmq.bots.inputs',
                  'intelmq.bots.inputs.arbor',
                  'intelmq.bots.inputs.abusehelper',
    ],
    scripts=['bin/intelmqctl'],
    url='http://pypi.python.org/pypi/IntelMQ/',
    license='MPL v2.0',
    description="IntelMQ Tool",
    long_description='IntelMQ is a solution for CERTs to process data feeds, pastebins, tweets throught a message queue.',
    package_data={'': ['LICENSE', 'README.md', 'CONTRIBUTORS.md']},
    install_requires=[
        "pika==0.9.14",
        "python-dateutil==1.5",
        "geoip2==0.5.1",
        "dnspython==1.11.1",
        "redis==2.4.9",
        "pymongo==2.7.1",
        "xmpppy==0.5.0rc1",
    ],
)
