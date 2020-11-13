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

* CentOS 7
* Debian 9 and 10
* OpenSUSE Leap 15.1, 15.2
* Ubuntu: 16.04, 18.04, 20.04
* Docker Engine: 18.09.1

Other distributions which are (most probably) supported include CentOS 8, RHEL, Fedora and openSUSE Tumbleweed.

Install Dependencies
--------------------

If you are using native packages, you can simply skip this section as all dependencies are installed automatically.

Ubuntu / Debian
^^^^^^^^^^^^^^^

.. code-block:: bash

   apt install python3-pip python3-dnspython python3-psutil python3-redis python3-requests python3-termstyle python3-tz python3-dateutil
   apt install redis-server

Optional dependencies:

.. code-block:: bash

   apt install bash-completion jq
   apt install python3-sleekxmpp python3-pymongo python3-psycopg2

CentOS 7 / RHEL 7
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   yum install epel-release
   yum install python36 python36-devel python36-requests
   yum install gcc gcc-c++
   yum install redis

openSUSE 15.1
^^^^^^^^^^^^^

.. code-block:: bash

   zypper install python3-dateutil python3-dnspython python3-psutil python3-pytz python3-redis python3-requests python3-python-termstyle
   zypper install redis

Optional dependencies:

.. code-block:: bash

   zypper in bash-completion jq
   zypper in python3-psycopg2 python3-pymongo python3-sleekxmpp

Docker
^^^^^^

Follow `Docker Install <https://docs.docker.com/engine/install/>`_ and 
`Docker-Compose Install <https://docs.docker.com/compose/install/>`_ instructions.

Installation
------------

Installation methods available:

* native packages (`.deb`, `.rpm`)
* PyPi (latest releases as python package)

**Note:** installation for development purposes must follow the instructions available on :ref:`development environment`.

Native Packages
^^^^^^^^^^^^^^^

Supported Operating Systems:

* **CentOS 7** (requires `epel-release`)
* **Debian 8** (requires `python3-typing`)
* **Debian 9**
* **Debian 10**
* **Fedora 29**
* **Fedora 30**
* **RHEL 7**  (requires `epel-release`)
* **openSUSE Leap 15.0**
* **openSUSE Leap 15.1**
* **openSUSE Tumbleweed**
* **Ubuntu 16.04** (enable the universe repositories by appending ` universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ xenial main`)
* **Ubuntu 18.04** (enable the universe repositories by appending ` universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ bionic main`)
* **Ubuntu 19.10** (enable the universe repositories by appending ` universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ eoan main`)
* **Ubuntu 20.04** (enable the universe repositories by appending ` universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ focal main`)

Get the installation instructions for your operating system here: `Installation Native Packages <https://software.opensuse.org/download.html?project=home%3Asebix%3Aintelmq&package=intelmq>`_.
To import the key on Debian and Ubuntu, use:

.. code-block:: bash

   curl https://build.opensuse.org/projects/home:sebix:intelmq/public_key | sudo apt-key add -

Please report any errors or improvements at `IntelMQ Issues <https://github.com/certtools/intelmq/issues>`_. Thanks!

PyPi
^^^^

.. code-block:: bash

   sudo -i
   
   pip3 install intelmq
   
   useradd -d /opt/intelmq -U -s /bin/bash intelmq
   sudo intelmqsetup

`intelmqsetup` will create all necessary directories, provides a default configuration for new setups. See the :ref:`configuration` for more information on them and how to influence them.

Docker
^^^^^^

Navigate to your preferred installation directory, i. e. use ``mkdir ~/intelmq && cd ~/intelmq``

.. code-block:: bash

   git clone https://github.com/certat/intelmq-docker.git

   sudo docker pull certat/intelmq-full:1.0

   mkdir intelmq_logs

   cd intelmq-docker

   chown -R $USER:$USER example_config

   sudo docker-compose up

Your installation should be successful now. You're now able to visit ``http://127.0.0.1:1337/`` to access the intelmq-manager.


Additional Information
^^^^^^^^^^^^^^^^^^^^^^

Following any one of the installation methods mentioned before, will setup the IntelMQ base. However, some bots may have additional dependencies which are mentioned in their :doc:`own documentation <bots>`).
