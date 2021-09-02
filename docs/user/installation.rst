..
   SPDX-FileCopyrightText: 2017 Sebastian Wagner
   SPDX-License-Identifier: AGPL-3.0-or-later

Installation
============

.. contents::

Please report any errors you encounter at https://github.com/certtools/intelmq/issues

For upgrade instructions, see :doc:`upgrade`.
For setting up a development environment see the :doc:`../dev/guide` section *Development Environment*.
For testing pre-releases see also the :doc:`../dev/guide` section *Testing Pre-releases*.

Requirements
------------

The following instructions assume the following requirements. Python versions >= 3.6 are supported.

Supported and recommended operating systems are:

* CentOS 7 and 8
* Debian 10 Buster and 11 Bullseye
* openSUSE Leap 15.2, 15.13
* Ubuntu: 18.04, 20.04
* Docker Engine: 18.x and higher

Other distributions which are (most probably) supported include RHEL, Fedora, openSUSE Tumbleweed and FreeBSD 12.

A short guide on hardware requirements can be found on the page :doc:`hardware-requirements`.

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

openSUSE 15.2 / 15.3
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   zypper install python3-dateutil python3-dnspython python3-psutil python3-pytz python3-redis python3-requests python3-python-termstyle
   zypper install redis

Optional dependencies:

.. code-block:: bash

   zypper in bash-completion jq
   zypper in python3-psycopg2 python3-pymongo

Docker (beta)
^^^^^^^^^^^^^

**ATTENTION** Currently you can't manage your botnet via :doc:`intelmqctl`. You need to use `IntelMQ-Manager <https://github.com/certtools/intelmq-manager>`_ currently!

Follow `Docker Install <https://docs.docker.com/engine/install/>`_ and
`Docker-Compose Install <https://docs.docker.com/compose/install/>`_ instructions.

The latest image is hosted on `Docker Hub <https://hub.docker.com/r/certat/intelmq-full>`_

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
* **Debian 10** Buster
* **Debian 11** Bullseye
* **Fedora 33**
* **Fedora 34**
* **openSUSE Leap 15.2**
* **openSUSE Leap 15.3** (make sure the ``openSUSE:Backports:SLE-15-SP3`` repository is enabled)
* **openSUSE Tumbleweed**
* **Ubuntu 18.04** (enable the universe repositories by appending `universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ bionic main` first)
* **Ubuntu 20.04** (enable the universe repositories by appending `universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ focal main` first)

Get the installation instructions for your operating system here: `Installation Native Packages <https://software.opensuse.org/download.html?project=home:sebix:intelmq&package=intelmq>`_.
The instructions show how to add the repository and install the `intelmq` package. You can also install the `intelmq-manager` package to get the `Web-Frontend IntelMQ Manager <https://github.com/certtools/intelmq-manager/>`_.

Please report any errors or improvements at `IntelMQ Issues <https://github.com/certtools/intelmq/issues>`_. Thanks!

PyPi
^^^^

.. code-block:: bash

   sudo -i

   pip3 install intelmq

   useradd -d /opt/intelmq -U -s /bin/bash intelmq
   sudo intelmqsetup

`intelmqsetup` will create all necessary directories, provides a default configuration for new setups. See the :ref:`configuration` for more information on them and how to influence them.

Docker **with** docker-compose (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Navigate to your preferred installation directory and run the following commands.

**NOTE** If not already installed, please install `Docker <https://docs.docker.com/get-docker/>`_

Before you start using docker-compose or any docker related tools, make sure docker is running

.. code-block:: bash

   # To start the docker daemon
   systemctl start docker.service

   # To enable the docker daemon for the future
   systemctl enable docker.service

.. code-block:: bash

   git clone https://github.com/certat/intelmq-docker.git --recursive

   cd intelmq-docker

   sudo docker-compose pull

   sudo docker-compose up

Your installation should be successful now. You're now able to visit ``http://127.0.0.1:1337/`` to access the intelmq-manager.

NOTE: If you get an `Permission denied`, you should use `chown -R $USER:$USER example_config`

Docker without docker-compose
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**NOTE** If not already installed, please install `Docker <https://docs.docker.com/get-docker/>`_

Navigate to your preferred installation directory and run ``git clone https://github.com/certat/intelmq-docker.git --recursive``.

You need to prepare some volumes & configs. Edit the left-side after -v, to change paths.

Change ``redis_host`` to a running redis-instance. Docker will resolve it automatically.
All containers are connected using `Docker Networks <https://docs.docker.com/engine/tutorials/networkingcontainers/>`_.

In order to work with your current infrastructure, you need to specify some environment variables

.. code-block:: bash

   sudo docker pull redis:latest

   sudo docker pull certat/intelmq-full:latest

   sudo docker pull certat/intelmq-nginx:latest

   sudo docker network create intelmq-internal

   sudo docker run -v ~/intelmq/example_config/redis/redis.conf:/redis.conf \
                   --network intelmq-internal \
                   --name redis \
                   redis:latest

   sudo docker run --network intelmq-internal \
                   --name nginx \
                   certat/intelmq-nginx:latest

   sudo docker run -e INTELMQ_IS_DOCKER="true" \
                   -e INTELMQ_PIPELINE_DRIVER="redis" \
                   -e INTELMQ_PIPELINE_HOST=redis_host \
                   -e INTELMQ_REDIS_CACHE_HOST=redis_host \
                   -v ~/intelmq/example_config/intelmq/etc/:/opt/intelmq/etc/ \
                   -v ~/intelmq/example_config/intelmq-api:/opt/intelmq-api/config \
                   -v /var/log/intelmq:/opt/intelmq/var/log \
                   -v ~/intelmq/lib:/opt/intelmq/var/lib \
                   --network intelmq-internal \
                   --name intelmq \
                   certat/intelmq-full:1.0

Additional Information
^^^^^^^^^^^^^^^^^^^^^^

Following any one of the installation methods mentioned before, will setup the IntelMQ base. However, some bots may have additional dependencies which are mentioned in their :doc:`own documentation <bots>`).
