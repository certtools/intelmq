<!--
SPDX-FileCopyrightText: 2016-2021 CERT.at GmbH <intelmq@cert.at>, 2023-2025 Institute for Common Good Technology

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Contrib

This directory contains contributed scripts which are helpful for maintaining an IntelMQ instance.

* **autostart**: Contains the start scripts and systemd units for the package `intelmq-autostart`.
* **bash-completion**: Bash completion scripts for the command line interfaces. Part of the package `intelmq`.
* **check_mk**: Scripts for monitoring an IntelMQ instance with Check_MK.
* **config-backup**: simple Makefile for doing a `make backup` inside of `/opt/intelmq` in order to preserve the latest configurations
* **cron-jobs**: cron job files for pulling in newer versions of supporting databases such as pyasn
* **development-tools**: Tools useful for development
* **elasticsearch**: Generate an ElasticSearch mapping
* **eventdb**: Some scripts related to the EventDB, see https://docs.intelmq.org/latest/admin/database/postgresql/#eventdb-utilities
* **example-extension-package**: An example bot extension package, see https://docs.intelmq.org/latest/dev/extensions-packages/
* **feeds-config-generator**: Outdated tool to generate configuration snippets for feeds
* **logcheck**: logcheck ruleset to filter logs for error messages
* **logrotate**: an example configuration for *logrotate* (`/etc/logrotate.d/` directory). Part of the package `intelmq`.
* **malware_name_mapping**: Script to download the malware name mapping and convert it to IntelMQ syntax
* **systemd**: Scripts to generate systemd unit files
* **tmpfiles.d**: systemd `tmpfiles.d` configuration

## Packages

When you have IntelMQ installed via packages, these scripts are part of the package `intelmq-contrib`.

The logcheck rules are directly installed to `/etc/logcheck/`, and the other files are in `/usr/share/intelmq/contrib/`.
