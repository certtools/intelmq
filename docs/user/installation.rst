..
   SPDX-FileCopyrightText: 2017-2021 Sebastian Wagner
   SPDX-License-Identifier: AGPL-3.0-or-later

Installation
============

.. contents::

Please report any errors an suggest improvements at `IntelMQ Issues <https://github.com/certtools/intelmq/issues>`_. Thanks!

For upgrade instructions, see :doc:`upgrade`.
For testing pre-releases see also :ref:`testing`.

Following any one of the installation methods will setup the IntelMQ base.
Some bots may have additional special dependencies which are mentioned in their :doc:`own documentation <bots>`.

The following installation methods are available:

* native `.deb`/`.rpm` packages
* Docker, with and without docker-compose
* Python package from PyPI
* From the git-repository, see :ref:`development environment`


Base Requirements
-----------------

The following instructions assume the following requirements. Python versions >= 3.6 are supported.

Supported and recommended operating systems are:

* CentOS 7 and 8
* Debian 10 Buster and 11 Bullseye
* openSUSE Leap 15.2, 15.13 and Tumbleweed
* Ubuntu: 18.04, 20.04
* For the Docker-installation: Docker Engine: 18.x and higher

Other distributions which are (most probably) supported include RHEL, Fedora and FreeBSD 12.

A short guide on hardware requirements can be found on the page :doc:`hardware-requirements`.


Native deb/rpm packages
-----------------------

These are the operating systems which are currently supported by packages:

* **CentOS 7** (run ``yum install epel-release`` first)
* **CentOS 8** (run ``dnf install epel-release`` first)
* **Debian 10** Buster
* **Debian 11** Bullseye
* **Fedora 33**
* **Fedora 34**
* **openSUSE Leap 15.2**
* **openSUSE Leap 15.3** (make sure the ``openSUSE:Backports:SLE-15-SP3`` repository is enabled)
* **openSUSE Tumbleweed**
* **Ubuntu 18.04** Bionic Beaver (enable the universe repositories by appending ``universe`` in ``/etc/apt/sources.list`` to ``deb http://[...].archive.ubuntu.com/ubuntu/ bionic main`` first)
* **Ubuntu 20.04** Focal Fossa (enable the universe repositories by appending ``universe`` in ``/etc/apt/sources.list`` to ``deb http://[...].archive.ubuntu.com/ubuntu/ focal main`` first)

Get the installation instructions for your operating system here: `Installation Native Packages <https://software.opensuse.org/download.html?project=home:sebix:intelmq&package=intelmq>`_.
The instructions show how to add the repository and install the `intelmq` package. You can also install the `intelmq-manager` package to get the `Web-Frontend IntelMQ Manager <https://github.com/certtools/intelmq-manager/>`_.


Docker
------

Attention: Currently you can't manage your botnet via :doc:`intelmqctl`. You need to use `IntelMQ-Manager <https://github.com/certtools/intelmq-manager>`_ currently!

The latest IntelMQ image is hosted on `Docker Hub <https://hub.docker.com/r/certat/intelmq-full>`_ and the image build instructions are in our `intelmq-docker repository <https://github.com/certat/intelmq-docker>`.

Follow `Docker Install <https://docs.docker.com/engine/install/>`_ and
`Docker-Compose Install <https://docs.docker.com/compose/install/>`_ instructions.

Before you start using docker-compose or any docker related tools, make sure docker is running:

.. code-block:: bash

   # To start the docker daemon
   systemctl start docker.service
   # To enable the docker daemon for the future
   systemctl enable docker.service

Now we can download IntelMQ and start the containers.
Navigate to your preferred installation directory and run the following commands:

.. code-block:: bash

   git clone https://github.com/certat/intelmq-docker.git --recursive
   cd intelmq-docker
   sudo docker-compose pull
   sudo docker-compose up

Your installation should be successful now. You're now able to visit ``http://127.0.0.1:1337/`` to access the intelmq-manager.
You have to login with the username ``intelmq`` and the password ``intelmq``, if you want to change the username or password,
you can do this by adding the environment variables ``INTELMQ_API_USER`` for the username and ``INTELMQ_API_PASS`` for the
password.

NOTE: If you get an `Permission denied`, you should use ``chown -R $USER:$USER example_config``.


With pip from PyPI
------------------

Requirements
^^^^^^^^^^^^

Ubuntu / Debian

.. code-block:: bash

   apt install python3-pip python3-dnspython python3-psutil python3-redis python3-requests python3-termstyle python3-tz python3-dateutil redis-server bash-completion jq
   # optional dependencies
   apt install python3-pymongo python3-psycopg2

CentOS 7 / RHEL 7:

.. code-block:: bash

   yum install epel-release
   yum install python36 python36-dns python36-pytz python36-requests python3-setuptools redis bash-completion jq
   yum install gcc gcc-c++ python36-devel
   # optional dependencies
   yum install python3-psycopg2

CentOS 8:

.. code-block:: bash

    dnf install epel-release
    dnf install python3-dateutil python3-dns python3-pip python3-psutil python3-pytz python3-redis python3-requests redis bash-completion jq
    # optional dependencies
    dnf install python3-psycopg2 python3-pymongo

openSUSE:

.. code-block:: bash

   zypper install python3-dateutil python3-dnspython python3-psutil python3-pytz python3-redis python3-requests python3-python-termstyle redis bash-completion jq
   # optional dependencies
   zypper in python3-psycopg2 python3-pymongo

Installation
^^^^^^^^^^^^

The base directory is ``/opt/intelmq/``, if the environment variable ``INTELMQ_ROOT_DIR`` is not set to something else, see :ref:`configuration-paths` for more information.

.. code-block:: bash

   sudo -i
   pip3 install intelmq
   useradd -d /opt/intelmq -U -s /bin/bash intelmq
   sudo intelmqsetup

`intelmqsetup` will create all necessary directories, provides a default configuration for new setups. See the :ref:`configuration` for more information on them and how to influence them.


Docker without docker-compose
-----------------------------

If not already installed, please install `Docker <https://docs.docker.com/get-docker/>`_.

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
                   -e INTELMQ_SOURCE_PIPELINE_BROKER: "redis" \
                   -e INTELMQ_PIPELINE_BROKER: "redis" \
                   -e INTELMQ_DESTIONATION_PIPELINE_BROKER: "redis" \
                   -e INTELMQ_PIPELINE_HOST: redis \
                   -e INTELMQ_SOURCE_PIPELINE_HOST: redis \
                   -e INTELMQ_DESTINATION_PIPELINE_HOST: redis \
                   -e INTELMQ_REDIS_CACHE_HOST: redis \
                   -v $(pwd)/example_config/intelmq/etc/:/etc/intelmq/etc/ \
                   -v $(pwd)/example_config/intelmq-api/config.json:/etc/intelmq/api-config.json \
                   -v $(pwd)/intelmq_logs:/etc/intelmq/var/log \
                   -v $(pwd)/intelmq_output:/etc/intelmq/var/lib/bots \
                   -v ~/intelmq/lib:/etc/intelmq/var/lib \
                   --network intelmq-internal \
                   --name intelmq \
                   certat/intelmq-full:latest

If you want to use another username and password for the intelmq-manager / api login, additionally add two new environment variables.

.. code-block:: bash

   -e INTELMQ_API_USER: "your username"
   -e INTELMQ_API_PASS: "your password"
