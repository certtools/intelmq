<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Common Problems 

## IntelMQ

### Permission denied when using Redis Unix socket

If you get an error like this:

```
intelmq.lib.exceptions.PipelineError: pipeline failed - ConnectionError('Error 13 connecting to unix socket: /var/run/redis/redis.sock. Permission denied.',)
```

Make sure the intelmq user as sufficient permissions for the socket.

In `/etc/redis/redis.conf` (or wherever your configuration is), check
the permissions and set it for example to group-writeable:

```
unixsocketperm 770
```

And add the user intelmq to the redis-group:

```bash
usermod -aG redis intelmq
```

### My bot(s) died on startup with no errors logged

Rather than starting your bot(s) with `intelmqctl start`, try
`intelmqctl run [bot]`. This will provide valuable debug output you
might not otherwise see, pointing to issues like system configuration
errors.

### Orphaned Queues

This section has been moved to the [Management Guide](management/intelmq.md#orphaned-queues).


### Multithreading is not available for this bot

Multithreading is not available for some bots and AMQP broker is
necessary. Possible reasons why a certain bot or a setup does not
support Multithreading include:

 -   Multithreading is only available when using the AMQP broker.
 -   For most collectors, Multithreading is disabled. Otherwise this
     would lead to duplicated data, as the data retrieval is not
     atomic.
 -   Some bots use libraries which are not thread safe. Look a the
     bot's documentation for more information.
 -   Some bots' operations are not thread safe. Look a the bot's
     documentation for more information.

If you think this mapping is wrong, please report a bug.


## IntelMQ API


### IntelMQCtlError

If the command is not configured correctly, you will see exceptions on
startup like this:

```bash
intelmq_manager.runctl.IntelMQCtlError: <ERROR_MESSAGE>
```

This means the intelmqctl command could not be executed as a subprocess.
The `<ERROR_MESSAGE>` should indicate why.

### Access Denied / Authentication Required "Please provide valid Token verification credentials"

If you see the IntelMQ Manager interface and menu, but the API calls to
the back-end querying configuration and status of IntelMQ fail with
"Access Denied" or "Authentication Required: Please provide valid
Token verification credentials" errors, you are maybe not logged in
while the API requires authentication.

By default, the API requires authentication. Create user accounts and
login with them or - if you have other protection means in place -
deactivate the authentication requirement by removing or renaming the
`session_store` parameter in the configuration.

### Internal Server Error

There can be various reasons for internal server errors. You need to
look at the error log of your web server, for example
`/var/log/apache2/error.log` or `/var/log/httpd/error_log` for Apache 2.
It could be that the sudo-setup is not functional, the configuration
file or session database file can not be read or written or other errors
in regards to the execution of the API program.

### Can I just install it from the deb/rpm packages while installing IntelMQ from a different source?

Yes, you can install the API and the Manager from the deb/rpm
repositories, and install your IntelMQ from a somewhere else, e.g. a
local repository. However, knowledge about Python and system
administration experience is recommended if you do so.

The packages install IntelMQ to
`/usr/lib/python3*/site-packages/intelmq/`. Installing with `pip`
results in `/usr/local/lib/python3*/site-packages/intelmq/` (and some
other accompaning resources) which overrides the installation in
`/usr/lib/`. You probably need to adapt the configuration parameter
`intelmq_ctl_cmd` to the `/usr/local/bin/intelmqctl` executable and some
other tweaks.

### sqlite3.OperationalError: attempt to write a readonly database

SQLite does not only need write access to the database itself, but also
the folder the database file is located in. Please check that the
webserver has write permissions to the folder the session file is
located in.