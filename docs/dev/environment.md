<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Development Environment

## Directories

For development purposes, you need two directories:

* directory with the local source code repository
* root directory of the IntelMQ installation

The default root directory of the IntelMQ installation is `/opt/intelmq`. This
directory is used for configurations (`/opt/intelmq/etc`),
local states (`/opt/intelmq/var/lib`) and logs
(`/opt/intelmq/var/log`). If you want to change it, please
set the `INTELMQ_ROOT_DIR` environment variable with a
desired location.

For repository directory, you can use any path that is accessible by
users you use to run IntelMQ. For globally installed IntelMQ, the
directory has to be readable by other unprivileged users (e.g. home
directories on Fedora can't be read by other users by default).

To keep commands in the guide universal, we will use environmental
variables for repository and installation paths. You can set them with
following commands:

```bash
# Adjust paths if you want to use non-standard directories
export INTELMQ_REPO=/opt/dev_intelmq
export INTELMQ_ROOT_DIR=/opt/intelmq
```

!!! note
    If using non-default installation directory, remember to keep the root directory variable set for every run of IntelMQ commands. If you don't, then the default location `/opt/intelmq` will be used.

## Installation

Developers can create a fork repository of IntelMQ in order to commit the new code to this repository and then be able
to do pull requests to the main repository. Otherwise you can just use the 'certtools' as username below.

The following instructions will use `pip3 -e`, which gives you a so called *editable* installation. No code is copied in
the libraries directories, there's just a link to your code. However, configuration files still required to be moved to
`/opt/intelmq` as the instructions show.

The traditional way to work with IntelMQ is to install it globally and have a separated user for running it. If you wish
to separate your machine Python's libraries, e.g. for development purposes, you could alternatively use a Python
virtual environment and your local user to run IntelMQ. Please use your preferred way from instructions below.

#### Using globally installed IntelMQ

```bash
sudo -s

git clone https://github.com/<your username>/intelmq.git $INTELMQ_REPO
cd $INTELMQ_REPO

pip3 install -e .

useradd -d $INTELMQ_ROOT_DIR -U -s /bin/bash intelmq

intelmqsetup
```

#### Using virtual environment

```bash
git clone https://github.com/<your username>/intelmq.git $INTELMQ_REPO
cd $INTELMQ_REPO

python -m venv .venv
source .venv/bin/activate

pip install -e .

# If you use a non-local directory as INTELMQ_ROOT_DIR, use following
# command to create it and change the ownership.
sudo install -g `whoami` -o `whoami` -d $INTELMQ_ROOT_DIR
# For local directory, just create it with mkdir:
mkdir $INTELMQ_ROOT_DIR

intelmqsetup --skip-ownership
```

!!! note
    Please do not forget that configuration files, log files will be available on `$INTELMQ_ROOT_DIR`. However, if your development is somehow related to any shipped configuration file, you need to apply the changes in your repository `$INTELMQ_REPO/intelmq/etc/`.

### Additional services

Some features require additional services, like message queue or database. The commonly used services are gained for development purposes in the Docker Compose file in `contrib/development-tools/docker-compose-common-services.yaml` in the repository. You can use them to run services on your machine in a docker containers, or decide to configure them in an another way. To run them using Docker Compose, use following command from the main repository directory:

```bash
# For older Docker versions, you may need to use `docker-compose` command
docker compose -f contrib/development-tools/docker-compose-common-services.yaml up -d
```

This will start in the background containers with Redis, RabbitMQ, PostgreSQL and MongoDB.

### How to develop

After you successfully setup your IntelMQ development environment, you can perform any development on any `.py` file on `$INTELMQ_REPO`. After you change, you can use the normal procedure to run the bots:

```bash
su - intelmq # Use for global installation
source .venv/bin/activate # Use for virtual environment installation

intelmqctl start spamhaus-drop-collector

tail -f $INTELMQ_ROOT_DIR/var/log/spamhaus-drop-collector.log
```

You can also add new bots, creating the new `.py` file on the proper directory inside `cd $INTELMQ_REPO/intelmq`.
However, your IntelMQ installation with pip3 needs to be updated. Please check the following section.

### Update

In case you developed a new bot, you need to update your current development installation. In order to do that, please follow this procedure:

1. Make sure that you have your new bot in the right place.
2. Update pip metadata and new executables:
```bash
sudo -s # Use for global installation
source .venv/bin/activate # Use for virtual environment installation

cd /opt/dev_intelmq
pip3 install -e .
```

3. If you're using the global installation, an additional step of changing permissions and ownership is necessary:
```bash
find $INTELMQ_ROOT_DIR/ -type d -exec chmod 0770 {} \+
find $INTELMQ_ROOT_DIR/ -type f -exec chmod 0660 {} \+
chown -R intelmq.intelmq $INTELMQ_ROOT_DIR
## if you use the intelmq manager (adapt the webservers' group if needed):
chown intelmq.www-data $INTELMQ_ROOT_DIR/etc/*.conf
```

Now you can test run your new bot following this procedure:

```bash
su - intelmq              # Use for global installation
source .venv/bin/activate # Use for virtual environment installation

intelmqctl start <bot_id>
```

