# Upgrade instructions

For installation instructions, see [INSTALL.md](INSTALL.md).

**Table of Contents:**
- [Stop IntelMQ and Backup](#stop-intelmq-and-backup)
- [Upgrade IntelMQ](#upgrade-intelmq)
  - [Packages](#packages)
  - [PyPi](#pypi)
  - [Local repository](#local-repository)
- [Check the installation](#check-the-installation)
- [Redefine/Check permissions](#redefinecheck-permissions)
- [Start IntelMQ](#start-intelmq)


## Read NEWS.md

Read the [NEWS.md](https://github.com/certtools/intelmq/blob/develop/NEWS.md) file to look for things you need to have a look at.

## Stop IntelMQ and Backup

* Make sure that your IntelMQ system is completely stopped: `intelmqctl stop`
* Create a backup of IntelMQ Home directory, which includes all configurations. They are not overwritten, but backups are always nice to have!

```bash
> sudo cp -R /opt/intelmq /opt/intelmq-backup
```

## Upgrade IntelMQ

Before upgrading, check that your setup is clean and there are no events in the queues:
```bash
intelmqctl check
intelmqctl list queues -q
```

The upgrade depends on how you installed IntelMQ.

### Packages

Use your systems package management.

### PyPi

```
pip install -U --no-deps intelmq
sudo intelmqsetup
```
Using `--no-deps` will not upgrade dependencies, which would probably overwrite the system's libraries.
Remove this option to also upgrade dependencies.

### Local repository

If you have an editable installation, refer to the instructions in the [Developers Guide](Developers-Guide.html#development-environment).

Update the repository depending on your setup (e.g. `git pull origin master`).

And run the installation again:
```bash
pip install .
sudo intelmqsetup
```
For editable installations (development only), run `pip install -e .` instead.

## Upgrade configuration and check the installation

Go through [NEWS.md](../NEWS.md) and apply necessary adaptions to your setup.
If you have adapted IntelMQ's code, also read the [CHANGELOG.md](../CHANGELOG.md).

Check your installation and configuration to detect any problems:
```bash
intelmqctl upgrade-config
intelmqctl check
```

## Start IntelMQ

```
> intelmqctl start
```
