<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Upgrade instructions

In order to upgrade your IntelMQ installation it is recommended to follow these five steps:

## 1. Read NEWS.md

Read the
[NEWS.md](https://github.com/certtools/intelmq/blob/develop/NEWS.md)
file to look for things you need to have a look at.

## 2. Stop IntelMQ and create a backup

- Make sure that your IntelMQ system is completely stopped: `intelmqctl stop`
- Create a backup of IntelMQ Home directory, which includes all configurations. They are not overwritten, but backups are always nice to have!

```bash
sudo cp -R /opt/intelmq /opt/intelmq-backup
```

## 3. Upgrade IntelMQ

Before upgrading, check that your setup is clean and there are no events
in the queues:

```bash
intelmqctl check
intelmqctl list queues -q
```

The upgrade depends on how you installed IntelMQ.

### Linux Packages

Use your system's package manager.

### PyPi

```bash
pip install -U --no-deps intelmq
sudo intelmqsetup
```

Using `--no-deps` will not upgrade dependencies, which would probably overwrite the system's libraries. Remove this option to
also upgrade dependencies.

### Docker

You can check out all current versions on our [DockerHub](https://hub.docker.com/r/certat/intelmq-full).

```bash
docker pull certat/intelmq-full:latest

docker pull certat/intelmq-nginx:latest
```

Alternatively you can use `docker-compose`:

```bash
docker-compose pull
```

You can check the current versions from intelmq & intelmq-manager & intelmq-api via git commit ref.

The Version format for each included item is `key=value` and they are saparated via `,`. I. e. `IntelMQ=ab12cd34f,IntelMQ-API=xy65z23`.

```bash
docker inspect --format '{{ index .Config.Labels "org.opencontainers.image.version" }}' intelmq-full:latest
```

Now restart your container, if you're using docker-compose you simply run:

```bash
docker-compose down
```

If you don't use `docker-compose`, you can restart a single container using:

```bash
docker ps | grep certat

docker restart CONTAINER_ID
```

### Source repository

If you have an editable installation, refer to the instructions in the
`/dev/guide`.

Update the repository depending on your setup (e.g. [git pull origin
master]).

And run the installation again:

```bash
pip install .
sudo intelmqsetup
```

For editable installations (development only), run [pip install -e
.] instead.

## 4. Upgrade configuration and check the installation

Go through
[NEWS.md](https://github.com/certtools/intelmq/blob/develop/NEWS.md) and
apply necessary adaptions to your setup. If you have adapted IntelMQ's
code, also read the
[CHANGELOG.md](https://github.com/certtools/intelmq/blob/develop/CHANGELOG.md).

Check your installation and configuration to detect any problems:

```bash
intelmqctl upgrade-config
intelmqctl check
```

`intelmqctl upgrade-config` supports upgrades from one IntelMQ version
to the succeeding. If you skip one or more IntelMQ versions, some
automatic upgrades *may not* work and manual intervention *may* be
necessary.

## 5. Start IntelMQ

```bash
intelmqctl start
```
