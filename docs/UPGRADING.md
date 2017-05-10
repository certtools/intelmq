# Upgrade instructions

For installation instructions, see [INSTALL.md](INSTALL.md).

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
> pip install -U --no-deps intelmq
```
Using `--no-deps` will not upgrade dependencies, which would probably overwrite the system's libraries.
Remove this option to also upgrade dependencies.

### Local repository

If you have an editable installation, refer to the instructions in the [Developers Guide](Developers-Guide.md#development-environment).

Update the repository depending on your setup (e.g. `git pull origin master`).

And run the installation again:
```bash
> pip install .
```
For editable installations, run `pip install -e .` instead.

## Check the installation

Go through [NEWS.md](../NEWS.md) and apply necessary adaptions to your setup.
If you have adapted IntelMQ's code, also read the [CHANGELOG.md](../CHANGELOG.md).

Check your installation and configuration fix detected problems:
```bash
> intelmqctl check
```

## Redefine/Check permissions

If you used `pip` for installation check and/or fix the permissions:
```bash
> chmod -R 0770 /opt/intelmq
> chown -R intelmq.intelmq /opt/intelmq
```

## Start IntelMQ

```
> intelmqctl start
```
