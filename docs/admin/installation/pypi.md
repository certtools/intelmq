<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Installation from PyPI

This guide provides instruction on how to install IntelMQ and it's components using the Python Package Index (PyPI)
repository.

!!! note
    Some bots may have additional dependencies which are mentioned in their own documentation.

## Installing IntelMQ

### Requirements

#### Ubuntu / Debian

```bash
apt install python3-pip python3-dnspython python3-psutil python3-redis python3-requests python3-termstyle python3-tz python3-dateutil redis-server bash-completion jq
# optional dependencies
apt install python3-pymongo python3-psycopg2
```

#### openSUSE:

```bash
zypper install python3-dateutil python3-dnspython python3-psutil python3-redis python3-requests python3-python-termstyle redis bash-completion jq
# optional dependencies
zypper in python3-psycopg2 python3-pymongo
```

#### CentOS 8:

```bash
dnf install epel-release
dnf install python3-dateutil python3-dns python3-pip python3-psutil python3-redis python3-requests redis bash-completion jq
# optional dependencies
dnf install python3-psycopg2 python3-pymongo
```

#### CentOS 7 / RHEL 7:

!!! warning
    We no longer support already end-of-life Python 3.6, which is the last Python version officially packaged for CentOS 7. You can either use alternative Python source, or stay on the IntelMQ 3.0.2.

```bash
yum install epel-release
yum install python36 python36-dns python36-requests python3-setuptools redis bash-completion jq
yum install gcc gcc-c++ python36-devel
# optional dependencies
yum install python3-psycopg2
```

### Installation

The default installation directory is `/opt/intelmq/`.

If you prefer to use Linux Standard Base (LSB) paths, set the following environment variable:

```bash
export INTELMQ_PATHS_NO_OPT=1
```

If you want to use custom installation directory, set the following environment variable:

```bash
export INTELMQ_ROOT_DIR=/my-installation-directory-path
```

Run the following commands to install IntelMQ. The provided tool `intelmqsetup` will create all the necessary directories and installs a default configuration for new setups.
If you are using the LSB paths installation, change the `--home-dir` parameter to `/var/lib/intelmq`

```bash
sudo --preserve-env=INTELMQ_PATHS_NO_OPT,INTELMQ_ROOT_DIR -i
pip3 install intelmq
[[ ! -z "$INTELMQ_PATHS_NO_OPT" ]] && export HOME_DIR=/var/lib/intelmq || export HOME_DIR=${INTELMQ_ROOT_DIR:-/opt/intelmq}
useradd --system --user-group --home-dir $HOME_DIR --shell /bin/bash intelmq
intelmqsetup
```

### Installation to Python virtual environment

```bash
sudo mkdir -m 755 /opt/intelmq
sudo useradd --system --user-group --home-dir /opt/intelmq --shell /bin/bash intelmq
sudo chown intelmq:intelmq /opt/intelmq/
sudo -u intelmq python3 -m venv /opt/intelmq/venv
sudo -u intelmq /opt/intelmq/venv/bin/pip install intelmq intelmq-api intelmq-manager
sudo /opt/intelmq/venv/bin/intelmqsetup
```


## Installing IntelMQ API (optional)

The `intelmq-api` packages ships:

- **api configuration** file in `${PREFIX}/etc/intelmq/api-config.json`
- **positions configuration** for the intelmq-manager in `{PREFIX}/etc/intelmq/manager/positions.conf`
- **virtualhost configuration** file for Apache 2 in `${PREFIX}/etc/intelmq/api-apache.conf`
- **sudoers configuration** file in `${PREFIX}/etc/intelmq/api-sudoers.conf`

The value of `${PREFIX}` depends on your environment and is something like `/usr/local/lib/pythonX.Y/dist-packages/` (where `X.Y` is your Python version).

The **virtualhost configuration** file needs to be placed in the correct directory for your Apache 2 installation.

- On Debian or Ubuntu, move the file to `/etc/apache2/conf-available.d/` directory and then execute
`a2enconf api-apache`.
- On CentOS, RHEL or Fedora, move the file to `/etc/httpd/conf.d/` directory.
- On openSUSE, move the file to `/etc/apache2/conf.d/` directory.

Don't forget to reload your webserver afterwards.

The **api configuration** file and the **positions configuration** file need to be placed in one of the following directories (based on your IntelMQ installation directory):

- `/etc/intelmq/`
- `/opt/intelmq/etc/`
- `[my-installation-directory-path]/etc/`

The **sudoers configuration** file should be placed in the `/etc/sudoers.d/` directory and adapt the webserver username in this file. Set the file permissions to `0o440`.

Afterwards continue with the section Permissions below.

IntelMQ 2.3.1 comes with a tool `intelmqsetup` which performs these set-up steps automatically. Please note that the
tool is very new and may not detect all situations correctly. Please report us any bugs you are observing. The tools is
idempotent, you can execute it multiple times.

## Installing IntelMQ Manager (optional)

To use the IntelMQ Manager web interface, it is required to have a working IntelMQ and IntelMQ API installation.

For installation via pip, the situation is more complex. The intelmq-manager package does not contain ready-to-use
files, they need to be built locally. First, lets install the Manager itself:

```bash
pip3 install intelmq-manager
```

If your system uses wheel-packages, not the source distribution, you can use the `intelmqsetup` tool. `intelmqsetup`
which performs these set-up steps automatically but it may not detect all situations correctly. If it
finds `intelmq-manager` installed, calls its build routine is called. The files are placed in
`/usr/share/intelmq_manager/html`, where the default Apache configuration expect it.

If your system used the dist-package or if you are using a local source, the tool may not do all required steps. To call
the build routine manually, use
`intelmq-manager-build --output-dir your/preferred/output/directory/`.

`intelmq-manager` ships with a default configuration for the Apache webserver (`manager-apache.conf`):

```
Alias /intelmq-manager /usr/share/intelmq_manager/html/

<Directory /usr/share/intelmq_manager/html>
    <IfModule mod_headers.c>
    Header set Content-Security-Policy "script-src 'self'"
    Header set X-Content-Security-Policy "script-src 'self'"
    </IfModule>
</Directory>
```

This file needs to be placed in the correct place for your Apache 2 installation.

- On Debian and Ubuntu, the file needs to be placed at `/etc/apache2/conf-available.d/manager-apache.conf` and then execute
  `a2enconf manager-apache`.
- On CentOS, RHEL and Fedora, the file needs to be placed at `/etc/httpd/conf.d/` and reload the webserver.
- On openSUSE, the file needs to be placed at `/etc/apache2/conf.d/` and reload the webserver.