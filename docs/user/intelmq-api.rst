.. 
   SPDX-FileCopyrightText: 2020 Birger Schacht
   SPDX-License-Identifier: AGPL-3.0-or-later

###########
Intelmq Api
###########

intelmq-api is a `hug <http://hug.rest>`_ based API for the `intelmq <https://github.com/certtools/intelmq/>`_ project.

**********************************
Installing and running intelmq-api
**********************************

``intelmq-api`` requires the IntelMQ package to be installed on the system (it uses ``intelmqctl`` to control the botnet).

You can install the ``intelmq-api`` package using your preferred system package installation mechanism or using the ``pip`` Python package installer.
We provide packages for the ``intelmq-api`` for the same operating systems as we do for the ``intelmq`` package itself.
Our repository page gives `installation instructions for various operating systems <https://software.opensuse.org/download.html?project=home:sebix:intelmq&package=intelmq>`_.

The ``intelmq-api`` packages ship a configuration file in ``${PREFIX}/etc/intelmq-api/config.json`` and a virtualhost configuration file for Apache 2 in ``${PREFIX}/etc/intelmq-api/apache-virtualhost.conf``.
The value of ``${PREFIX}`` depends on your installation method- with distribution packages it is simply ``/``, when using pip (as root) it is ``/usr/local/lib/pythonX.Y/dist-packages/`` (where ``X.Y`` is your Python version.
Some distribution packages already create a symlink in the relevant apache configuration directory to the apache configuration file, so it should be easy to enable that (i.e. by using ``a2ensite intelmq-api`` on Debian based systems).

But you can also run ``intelmq-api`` directly using ``hug``:

.. code-block:: bash

   hug -m intelmq_api.serve


... or using uwsgi

.. code-block:: bash

   uwsgi --http 0.0.0.0:8000 -w intelmq_api.serve --callable __hug_wsgi__

... or using gunicorn

.. code-block:: bash

   gunicorn intelmq_api.serve:__hug_wsgi__


The ``intelmq-api`` provides the route ``/api`` for managing the ``intelmq`` installation.

***********************
Configuring intelmq-api
***********************

Depending on your setup you might have to install ``sudo`` to make it possible for the ``intelmq-api`` to run the ``intelmq`` command as the user-account usually used to run ``intelmq`` (which is also often called ``intelmq``).

``intelmq-api`` is configured using a configuration file in ``json`` format.
The path to the configuration file is set using the environment variable ``INTELMQ_API_CONFIG``.
The default apache configuration file sets the environment variable to point to ``/etc/intelmq-api/config.json`` so if you are apache and your configuration file is stored somewhere else (i.e. because you used pip to install the package) you have to update the environment variable ``INTELMQ_API_CONFIG`` in the apache config.

When running the API using ``hug``, you can set the environment variable like this:

.. code-block:: bash

   INTELMQ_API_CONFIG=/etc/intelmq-api/config.json hug -m intelmq_api.serve


The configuration file ``/etc/intelmq-api/config.json`` which is shipped with the packages is also listed here for reference.
This also gives an example on how to disable a setting, namely by prefixing the name with an underscore, like it is done here with the ``_session_store`` setting.

.. code-block:: json

   {
           "intelmq_ctl_cmd": ["intelmqctl"],
           "allowed_path": "/opt/intelmq/var/lib/bots/",
           "_session_store": "/tmp/intelmq-session.sqlite",
           "session_duration": 86400,
           "allow_origins": ["*"]
   }

The following configuration options are available:

* ``intelmq_ctl_cmd``: Your ``intelmqctl`` command. If this is not set in a configuration file the default is used, which is ``["sudo", "-u", "intelmq", "/usr/local/bin/intelmqctl"]``
  The option ``"intelmq_ctl_cmd"`` is a list of strings so that we can avoid shell-injection vulnerabilities because no shell is involved when running the command.
  This means that if the command you want to use needs parameters, they have to be separate strings.
* ``allowed_path``: intelmq-api can grant **read-only** access to specific files - this setting defines the path those files can reside in.
* ``session_store``: this is an optional path to a sqlite database, which is used for session storage and authentication. If it is not set (which is the default), no authentication is used!
* ``session_duration``: the maximal duration of a session, its 86400 seconds by default
* ``allow_origins``: a list of origins the responses of the API can be shared with. Allows every origin by default.

Permissions
^^^^^^^^^^^

``intelmq-api`` tries to write a couple of configuration files in the ``${PREFIX}/etc/intelmq`` directory - this is only possible if you set the permissions accordingly, given that ``intelmq-api`` runs under a different user.
If you're using the default apache2 setup, you might want to set the group of the files to ``www-data`` and give it write permissions (``chmod g+w <filename>``).
In addition to that, the ``intelmq-manager`` tries to store the bot positions via the API into the file ``${PREFIX}/etc/intelmq/manager/positions.conf``.
You should therefore create the folder ``${PREFIX}/etc/intelmq/manager`` and the file ``positions.conf`` in it.

*************
Adding a user
*************

If you enable the ``session_store`` you will have to create user accounts to be able to access the API functionality. You can also do this using hug:

.. code-block:: bash

   hug -m intelmq_api.serve -c add_user <username>

**************
Usual problems
**************

If the command is not configured correctly, you'll see exceptions on startup like this:

.. code-block:: bash

   intelmq_manager.runctl.IntelMQCtlError: <ERROR_MESSAGE>

This means the intelmqctl command could not be executed as a subprocess.
The ``<ERROR_MESSAGE>`` should indicate why.
