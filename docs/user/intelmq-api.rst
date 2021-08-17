..
   SPDX-FileCopyrightText: 2020-2021 Birger Schacht, Sebastian Wagner
   SPDX-License-Identifier: AGPL-3.0-or-later

###########
IntelMQ API
###########

`intelmq-api` is a `hug <http://hug.rest>`_ based API for the `IntelMQ <https://github.com/certtools/intelmq/>`_ project.

.. contents::

**********************************
Installing and running intelmq-api
**********************************

`intelmq-api` requires the IntelMQ package to be installed on the system (it uses ``intelmqctl`` to control the botnet).

You can install the ``intelmq-api`` package using your preferred system package installation mechanism or using the ``pip`` Python package installer.
We provide packages for the `intelmq-api` for the same operating systems as we do for the `intelmq` package itself.
For the list of supported distributions, please see the intelmq :doc:`installation` page.

Our repository page gives `installation instructions for various operating systems <https://software.opensuse.org/download.html?project=home:sebix:intelmq&package=intelmq-api>`_.
No additional set-up steps are needed if you use these packages.

The `intelmq-api` provides the route ``/api`` for managing the IntelMQ installation.

For development purposes and testing you can also run `intelmq-api` directly using ``hug``:

.. code-block:: bash

   hug -m intelmq_api.serve

Installation using pip
^^^^^^^^^^^^^^^^^^^^^^

The `intelmq-api` packages ship a configuration file in ``${PREFIX}/etc/intelmq/api-config.json``, a positions configuration for the manager in ``{PREFIX}/etc/intelmq/manager/positions.conf``, a virtualhost configuration file for Apache 2 in ``${PREFIX}/etc/intelmq/api-apache.conf`` and a sudoers configuration file in ``${PREFIX}/etc/intelmq/api-sudoers.conf``.
The value of ``${PREFIX}`` depends on your environment and is something like ``/usr/local/lib/pythonX.Y/dist-packages/`` (where ``X.Y`` is your Python version).

The file ``${PREFIX}/etc/intelmq/api-apache.conf`` needs to be placed in the correct place for your Apache 2 installation.
 - On Debian and Ubuntu, move the file to ``/etc/apache2/conf-available.d/manager-apache.conf`` and then execute ``a2enconf manager-apache``.
 - On CentOS, RHEL and Fedora, move the file to ``/etc/httpd/conf.d/``.
 - On openSUSE, move the file to ``/etc/apache2/conf.d/``.
Don't forget to reload your webserver afterwards.

- The file ``${PREFIX}/etc/intelmq/api-config.json`` needs to be moved to ``/etc/intelmq/api-config.json``.
- The file ``${PREFIX}/etc/intelmq/manager/positions.conf`` needs to be moved to ``/etc/intelmq/manager/positions.conf``.
- Last but not least move the file ``${PREFIX}/etc/intelmq/api-sudoers.conf`` to ``/etc/sudoers.d/01_intelmq-api`` and adapt the webserver user name in this file. Set the file permissions to ``0o440``.

Afterwards continue with the section Permissions below.

IntelMQ 2.3.1 comes with a tool ``intelmqsetup`` which performs these set-up steps automatically.
Please note that the tool is very new and may not detect all situations correctly. Please report us any bugs you are observing.
The tools is idempotent, you can execute it multiple times.

***********************
Configuring intelmq-api
***********************

Depending on your setup you might have to install ``sudo`` to make it possible for the ``intelmq-api`` to run the ``intelmq`` command as the user-account usually used to run ``intelmq`` (which is also often called ``intelmq``).

``intelmq-api`` is configured using a configuration file in ``json`` format.
``intelmq-api`` tries to load the configuration file from ``/etc/intelmq/api-config.json`` and ``${PREFIX}/etc/intelmq/api-config.json``, but you can override the path setting the environment variable ``INTELMQ_API_CONFIG``.
(When using Apache, you can do this by modifying the Apache configuration file shipped with ``intelmq-api``, the file contains an example)

When running the API using ``hug``, you can set the environment variable like this:

.. code-block:: bash

   INTELMQ_API_CONFIG=/etc/intelmq/api-config.json hug -m intelmq_api.serve


The default configuration which is shipped with the packages is also listed here for reference:

.. code-block:: json

   {
       "intelmq_ctl_cmd": ["sudo", "-u", "intelmq", "intelmqctl"],
       "allowed_path": "/opt/intelmq/var/lib/bots/",
       "session_store": "/etc/intelmq/api-session.sqlite",
       "session_duration": 86400,
       "allow_origins": ["*"]
   }


On Debian based systems, the default path for the ``session_store`` is ``/var/lib/dbconfig-common/sqlite3/intelmq-api/intelmqapi``, because the Debian package uses the Debian packaging tools to manage the database file.

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
The user the API run as also needs write access to the folder the ``session_store`` is located in, otherwise there will be an error accessing the session data.
If you're using the default Apache 2 setup, you might want to set the group of the files to ``www-data`` and give it write permissions (``chmod -R g+w <directoryname>``).
In addition to that, the ``intelmq-manager`` tries to store the bot positions via the API into the file ``${PREFIX}/etc/intelmq/manager/positions.conf``.
You should therefore create the folder ``${PREFIX}/etc/intelmq/manager`` and the file ``positions.conf`` in it.

*************
Adding a user
*************

If you enable the ``session_store`` you will have to create user accounts to be able to access the API functionality. You can do this using ``intelmq-api-adduser``:

.. code-block:: bash

   intelmq-api-adduser --user <username> --password <password>

*****************
A note on SELinux
*****************

On systems with SELinux enabled, the API will fail to call intelmqctl.
Therefore, SELinux needs to be disabled:

.. code-block:: bash

   setenforce 0

We welcome contributions to provide SELinux policies.

*******************
Usage from programs
*******************

The IntelMQ API can also be used from programs, not just browsers.
To do so, first send a POST-Request with JSON-formatted data to http://localhost/intelmq/v1/api/login/

.. code-block:: json

   {
       "username": "$your_username",
       "password: "$your_password"
   }

With valid credentials, the JSON-formatted response contains the ``login_token``.
This token can be used like an API key in the Authorization header for the next API calls:

.. code-block:: bash

   Authorization: $login_token

Here is a full example using *curl*:

.. code-block:: bash

   > curl --location --request POST "http://localhost/intelmq/v1/api/login/"\
       --header "Content-Type: application/x-www-form-urlencoded"\
       --data-urlencode "username=$username"\
       --data-urlencode "password=$password"
   {"login_token":"68b329da9893e34099c7d8ad5cb9c940","username":"$username"}
   > curl --location "http://localhost/intelmq/v1/api/version"\
       --header "Authorization: 68b329da9893e34099c7d8ad5cb9c940"
   {"intelmq":"3.0.0rc1","intelmq-manager":"2.3.1"}


The same approach also works for *Ansible*, as you can see here:

1. https://github.com/schacht-certat/intelmq-vagrant/blob/7082719609c0aafc9324942a8775cf2f8813703d/ansible/tasks/api/00_registerauth.yml#L1-L9
2. https://github.com/schacht-certat/intelmq-vagrant/blob/7082719609c0aafc9324942a8775cf2f8813703d/ansible/tasks/api/02_queuestatus.yml#L1-L5

*****************************
Frequent operational problems
*****************************

IntelMQCtlError
^^^^^^^^^^^^^^^

If the command is not configured correctly, you'll see exceptions on startup like this:

.. code-block:: bash

   intelmq_manager.runctl.IntelMQCtlError: <ERROR_MESSAGE>

This means the intelmqctl command could not be executed as a subprocess.
The ``<ERROR_MESSAGE>`` should indicate why.

Access Denied / Authentication Required "Please provide valid Token verification credentials"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you see the IntelMQ Manager interface and menu, but the API calls to the back-end querying configuration and status of IntelMQ fail with "Access Denied" or "Authentication Required: Please provide valid Token verification credentials" errors, you are maybe not logged in while the API requires authentication.

By default, the API requires authentication. Create user accounts and login with them or - if you have other protection means in place - deactivate the authentication requirement by removing or renaming the `session_store` parameter in the configuration.

Internal Server Error
^^^^^^^^^^^^^^^^^^^^^

There can be various reasons for internal server errors. You need to look at the error log of your web server, for example ``/var/log/apache2/error.log`` or ``/var/log/httpd/error_log`` for Apache 2. It could be that the sudo-setup is not functional, the configuration file or session database file can not be read or written or other errors in regards to the execution of the API program.

Can I just install it from the deb/rpm packages while installing IntelMQ from a different source?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes, you can install the API and the Manager from the deb/rpm repositories, and install your IntelMQ from a somewhere else, e.g. a local repository.
However, knowledge about Python and system administration experience is recommended if you do so.

The packages install IntelMQ to ``/usr/lib/python3*/site-packages/intelmq/``.
Installing with ``pip`` results in ``/usr/local/lib/python3*/site-packages/intelmq/`` (and some other accompaning resources) which overrides the installation in ``/usr/lib/``.
You probably need to adapt the configuration parameter ``intelmq_ctl_cmd`` to the ``/usr/local/bin/intelmqctl`` executable and some other tweaks.

sqlite3.OperationalError: attempt to write a readonly database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SQLite does not only need write access to the database itself, but also the folder the database file is located in. Please check that the webserver has write permissions to the folder
the session file is located in.


************
Getting help
************

You can use the `IntelMQ users mailing lists <https://lists.cert.at/cgi-bin/mailman/listinfo/intelmq-users>`_ and `GitHub issues <https://github.com/certtools/intelmq-api/issues/new>`_ for getting help and getting in touch with other users and developers. See also the :doc:`introduction` page.
