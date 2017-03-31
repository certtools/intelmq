
# Contrib

This directory contains contributed scripts which are helpful for maintaining an intelmq instance.

* **cron-jobs**: cron job files for pulling in newer versions of supporting databases such as pyasn
* **logcheck**: logcheck ruleset
* **prettyprint**: prints the json output for file-output bot prettyly
* **config-backup**: simple Makefile for doing a `make backup` inside of /opt/intelmq in order to preserve the latest configs
* **logrotate**: an example scrpt for Debian's /etc/logrotate.d/ directory.

## Outdated
The following scripts are out of date but are left here for reference. TODO: adapt to current version

* **ansible**: ansible playbooks for IntelMQ. **Out of date**
* **vagrant**: vagrantfile to create virtual machines with IntelMQ. **Out of date**
* **vagrant-ansible**: Configures IntelMQ plus the whole elasticsearch stack. **Out of date**
