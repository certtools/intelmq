from setuptools import find_packages, setup

setup(
    name='intelmqExampleAddBot',
    version=3.1,  # noqa: F821
    maintainer='Sebastian Wagner',
    maintainer_email='intelmq-dev@lists.cert.at',
    python_requires='>=3.7',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/certtools/intelmq/',
    project_urls={
        'Documentation': 'https://intelmq.readthedocs.io/',
        'Source and Issue Tracker': 'https://github.com/certtools/intelmq/',
    },
    license='AGPLv3',
    description='IntelMQ is a solution for IT security teams for collecting and '
                'processing security feeds using a message queuing protocol.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Security',
    ],
    keywords='incident handling cert csirt',
)
