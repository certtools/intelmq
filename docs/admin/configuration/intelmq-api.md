<!-- comment
   SPDX-FileCopyrightText: 2015 Aaron Kaplan <aaron@lo-res.org>, 2015-2021 Sebastian Wagner, 2020-2021 Birger Schacht, 2023 Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Configuring IntelMQ API

Depending on your setup you might have to install `sudo` to make it
possible for the `intelmq-api` to run the `intelmq` command as the
user-account usually used to run `intelmq` (which is also often called
`intelmq`).

`intelmq-api` is configured using a configuration file in `json` format.
`intelmq-api` tries to load the configuration file from
`/etc/intelmq/api-config.json` and
`${PREFIX}/etc/intelmq/api-config.json`, but you can override the path
setting the environment variable `INTELMQ_API_CONFIG`. (When using
Apache, you can do this by modifying the Apache configuration file
shipped with `intelmq-api`, the file contains an example)

When running the API using `hug`, you can set the environment variable
like this:

```bash
INTELMQ_API_CONFIG=/etc/intelmq/api-config.json hug -m intelmq_api.serve
```

The default configuration which is shipped with the packages is also
listed here for reference:

```json
{
    "intelmq_ctl_cmd": ["sudo", "-u", "intelmq", "intelmqctl"],
    "allowed_path": "/opt/intelmq/var/lib/bots/",
    "session_store": "/etc/intelmq/api-session.sqlite",
    "session_duration": 86400,
    "allow_origins": ["*"]
}
```

On Debian based systems, the default path for the `session_store` is
`/var/lib/dbconfig-common/sqlite3/intelmq-api/intelmqapi`, because the
Debian package uses the Debian packaging tools to manage the database
file.

The following configuration options are available:

-   `intelmq_ctl_cmd`: Your `intelmqctl` command. If this is not set in
    a configuration file the default is used, which is
    `["sudo", "-u", "intelmq", "/usr/local/bin/intelmqctl"]` The option
    `"intelmq_ctl_cmd"` is a list of strings so that we can avoid
    shell-injection vulnerabilities because no shell is involved when
    running the command. This means that if the command you want to use
    needs parameters, they have to be separate strings.
-   `allowed_path`: intelmq-api can grant **read-only** access to
    specific files - this setting defines the path those files can
    reside in.
-   `session_store`: this is an optional path to a sqlite database,
    which is used for session storage and authentication. If it is not
    set (which is the default), no authentication is used!
-   `session_duration`: the maximal duration of a session, its 86400
    seconds by default
-   `allow_origins`: a list of origins the responses of the API can be
    shared with. Allows every origin by default.

### Permissions

`intelmq-api` tries to write a couple of configuration files in the
`${PREFIX}/etc/intelmq` directory - this is only possible if you set the
permissions accordingly, given that `intelmq-api` runs under a different
user. The user the API run as also needs write access to the folder the
`session_store` is located in, otherwise there will be an error
accessing the session data. If you\'re using the default Apache 2 setup,
you might want to set the group of the files to `www-data` and give it
write permissions (`chmod -R g+w <directoryname>`). In addition to that,
the `intelmq-manager` tries to store the bot positions via the API into
the file `${PREFIX}/etc/intelmq/manager/positions.conf`. You should
therefore create the folder `${PREFIX}/etc/intelmq/manager` and the file
`positions.conf` in it.

## Adding a user

If you enable the `session_store` you will have to create user accounts
to be able to access the API functionality. You can do this using
`intelmq-api-adduser`:

```bash
intelmq-api-adduser --user <username> --password <password>
```

## A note on SELinux

On systems with SELinux enabled, the API will fail to call `intelmqctl`.
Therefore, SELinux needs to be disabled:

```bash
setenforce 0
```

We welcome contributions to provide SELinux policies.