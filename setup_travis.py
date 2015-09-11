from __future__ import print_function

from setuptools import find_packages, setup


setup(
    name='intelmq',
    version='1.0.0',
    maintainer='Tomas Lima',
    maintainer_email='synchroack@gmail.com',
    packages=find_packages(),
    package_data={'intelmq': ['conf/*.conf', 'bots/experts/modify/*.conf']},
    url='http://pypi.python.org/pypi/intelmq/',
    license='AGPLv3',
    description="IntelMQ Tool",
    long_description='IntelMQ is a solution for CERTs to process data feeds, '
                     'pastebins, tweets throught a message queue.',
)
