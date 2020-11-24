Upgrade instructions
====================

.. contents::

For installation instructions, see :doc:`installation`.

Read NEWS.md
------------

Read the `NEWS.md <https://github.com/certtools/intelmq/blob/develop/NEWS.md>`_ file to look for things you need to have a look at.

Stop IntelMQ and create a Backup
--------------------------------

* Make sure that your IntelMQ system is completely stopped: `intelmqctl stop`
* Create a backup of IntelMQ Home directory, which includes all configurations. They are not overwritten, but backups are always nice to have!

.. code-block:: bash

   sudo cp -R /opt/intelmq /opt/intelmq-backup

Upgrade IntelMQ
---------------

Before upgrading, check that your setup is clean and there are no events in the queues:

.. code-block:: bash

   intelmqctl check
   intelmqctl list queues -q

The upgrade depends on how you installed IntelMQ.

Packages
^^^^^^^^

Use your systems package management.

Docker (beta)
^^^^^^^^^^^^^

**ATTENTION** Currently the version published on docker hub is not tagged with the same IntelMQ version. During beta, each version is published with tag `1.0`.

.. code-block:: bash

   docker pull certat/intelmq-full:1.0

Alternativly you can use `docker-compose`:

.. code-block:: bash

   docker-compose pull

You can check the current versions from intelmq & intelmq-manager via git commit ref.

The first one is the intelmq commit ref, and the second one is for intelmq-manager

.. code-block:: bash

   docker inspect --format '{{ index .Config.Labels "org.label-schema.vcs-ref"}}' certat/intelmq-full:1.0

Now restart your container, if you're using docker-compose you simply write:

.. code-block:: bash
   
   docker-compose down

If you dont use docker-compose, you can restart a single container using:

.. code-block:: bash

   docker ps | grep certat

   docker stop CONTAINER_ID

PyPi
^^^^

.. code-block:: bash

   pip install -U --no-deps intelmq
   sudo intelmqsetup

Using `--no-deps` will not upgrade dependencies, which would probably overwrite the system's libraries.
Remove this option to also upgrade dependencies.

Local repository
^^^^^^^^^^^^^^^^

If you have an editable installation, refer to the instructions in the :doc:`/dev/guide`.

Update the repository depending on your setup (e.g. `git pull origin master`).

And run the installation again:

.. code-block:: bash

   pip install .
   sudo intelmqsetup

For editable installations (development only), run `pip install -e .` instead.

Upgrade configuration and check the installation
------------------------------------------------

Go through `NEWS.md <https://github.com/certtools/intelmq/blob/develop/NEWS.md>`_ and apply necessary adaptions to your setup.
If you have adapted IntelMQ's code, also read the `CHANGELOG.md <https://github.com/certtools/intelmq/blob/develop/CHANGELOG.md>`_.

Check your installation and configuration to detect any problems:

.. code-block:: bash

   intelmqctl upgrade-config
   intelmqctl check

## Start IntelMQ

.. code-block:: bash

   intelmqctl start
