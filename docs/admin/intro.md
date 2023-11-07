<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Intro

This guide provides instructions on how to install, configure and manage IntelMQ and it's components.

IntelMQ uses a message broker such as Redis. This is required for IntelMQ to run.

IntelMQ doesn't handle long term storage of processed Events beyond writing to a file. However it provides connectors (output bots) for writing events to various database systems and log collectors. It is recommended to configure such
system to preserve processed events.

## Base Requirements

The following instructions assume the following requirements. Python versions >= 3.7 are supported.

Supported and recommended operating systems are:

- Debian
- openSUSE Tumbleweed/Leap
- Ubuntu
- For the Docker-installation: Docker Engine: 18.x and higher

Other distributions which are (most probably) supported include AlmaLinux, CentOS, Fedora, FreeBSD 12, RHEL and RockyLinux.

A short guide on hardware requirements can be found on the page
[Hardware Requirements](hardware-requirements.md).
