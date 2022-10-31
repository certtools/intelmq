<!--
SPDX-FileCopyrightText: 2016-2022 aaronkaplan <aaron@lo-res.org>, Sebastian Wagner <sebix@sebix.at>

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Contrib

This directory contains contributed scripts which are helpful for maintaining an IntelMQ instance.

* **cron-jobs**: cron job files for pulling in newer versions of supporting databases such as pyasn
* **logcheck**: logcheck ruleset to filter logs for error messages
* **prettyprint**: prints the json output for file-output bot prettily
* **config-backup**: simple Makefile for doing a `make backup` inside of `/opt/intelmq` in order to preserve the latest configurations
* **logrotate**: an example configuration for *logrotate* (`/etc/logrotate.d/` directory).
* **check_mk**: Scripts for monitoring an IntelMQ instance with Check_MK.
* **development-tools**: Tools useful for development
