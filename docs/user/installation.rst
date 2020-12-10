Installation
============

.. contents::

Please report any errors you encounter at https://github.com/certtools/intelmq/issues

For upgrade instructions, see :doc:`upgrade`.
For setting up a development environment see the :doc:`../dev/guide` section *Development Environment*.
For testing pre-releases see also the :doc:`../dev/guide` section *Testing Pre-releases*.

Requirements
------------

The following instructions assume the following requirements. Python versions >= 3.5 are supported.

Supported and recommended operating systems are:

* CentOS 7 and 8
* Debian 9 and 10
* OpenSUSE Leap 15.1, 15.2
* Ubuntu: 16.04, 18.04, 20.04

Other distributions which are (most probably) supported include CentOS 8, RHEL, Fedora and openSUSE Tumbleweed.

Install Dependencies
--------------------

**If you are using native packages, you skip this section as all dependencies are installed automatically.**

Ubuntu / Debian
^^^^^^^^^^^^^^^

.. code-block:: bash

   apt install python3-pip python3-dnspython python3-psutil python3-redis python3-requests python3-termstyle python3-tz python3-dateutil
   apt install redis-server

Optional dependencies:

.. code-block:: bash

   apt install bash-completion jq
   apt install python3-pymongo python3-psycopg2

CentOS 7 / RHEL 7
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   yum install epel-release
   yum install python36 python36-devel python36-requests
   yum install gcc gcc-c++
   yum install redis

CentOS 8
^^^^^^^^

.. code-block:: bash

    dnf install epel-release
    dnf install python3-dateutil python3-dns python3-pip python3-psutil python3-pytz python3-redis python3-requests redis

Optional dependencies:

.. code-block:: bash

    dnf install bash-completion jq
    dnf install python3-psycopg2 python3-pymongo

openSUSE 15.1 / 15.2
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   zypper install python3-dateutil python3-dnspython python3-psutil python3-pytz python3-redis python3-requests python3-python-termstyle
   zypper install redis

Optional dependencies:

.. code-block:: bash

   zypper in bash-completion jq
   zypper in python3-psycopg2 python3-pymongo

Installation
------------

Installation methods available:

* native packages (`.deb`, `.rpm`)
* PyPi (latest releases as python package)

**Note:** installation for development purposes must follow the instructions available on :ref:`development environment`.

Native Packages
^^^^^^^^^^^^^^^

These are the operating systems which are currently supported by packages:

* **CentOS 7** (run `yum install epel-release` first)
* **CentOS 8** (run `dnf install epel-release` first)
* **Debian 9**
* **Debian 10**
* **Fedora 30**
* **Fedora 31**
* **Fedora 32**
* **openSUSE Leap 15.1**
* **openSUSE Leap 15.2**
* **openSUSE Tumbleweed**
* **Ubuntu 16.04** (enable the universe repositories by appending `universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ xenial main` first)
* **Ubuntu 18.04** (enable the universe repositories by appending `universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ bionic main` first)
* **Ubuntu 20.04** (enable the universe repositories by appending `universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ focal main` first)

Get the installation instructions for your operating system here: `Installation Native Packages <https://software.opensuse.org/download.html?project=home:sebix:intelmq&package=intelmq>`_.
The instructions show how to add the repository and install the `intelmq` package. You can also install the `intelmq-manager` package to get the [Web-Frontend IntelMQ Manager](https://github.com/certtools/intelmq-manager/).

Please report any errors or improvements at `IntelMQ Issues <https://github.com/certtools/intelmq/issues>`_. Thanks!

PyPi
^^^^

.. code-block:: bash

   sudo -i
   
   pip3 install intelmq
   
   useradd -d /opt/intelmq -U -s /bin/bash intelmq
   sudo intelmqsetup

`intelmqsetup` will create all necessary directories, provides a default configuration for new setups. See the :ref:`configuration` for more information on them and how to influence them.

Additional Information
^^^^^^^^^^^^^^^^^^^^^^

Following any one of the installation methods mentioned before, will setup the IntelMQ base. However, some bots may have additional dependencies which are mentioned in their :doc:`own documentation <bots>`).
