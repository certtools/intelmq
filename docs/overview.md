<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Overview

The complete IntelMQ universe consists of the following components:

* IntelMQ
* IntelMQ API
* IntelMQ Manager
* additional tools
* useful scripts

## IntelMQ

This project contains the core functionality.

The Core includes all the components required for processing data feeds. This includes the bots, configuration, pipeline, the internal data format, management tools etc.

→ [Repository: IntelMQ](https://github.com/certtools/intelmq/)

## IntelMQ API

This is an extension of IntelMQ providing [hug](http://hug.rest) based REST API for remote management.

→ [Repository: IntelMQ API](https://github.com/certtools/intelmq-api/)

## IntelMQ Manager

The Manager is the most known software and can be seen as the face of IntelMQ. It's goal is to provide an intuitive web interface to allow non-programmers to specify the data flow in IntelMQ.

→ [Repository: IntelMQ Manager](https://github.com/certtools/intelmq-manager/)

![IntelMQ Manager Landing page](static/images/intelmq-manager/landing_page.png)

## Additional tools

Here you can find a list of additional tools. If you think something is missing, please let us know!

Unless stated otherwise, the tools are maintained by the IntelMQ community.

### IntelMQ Webinput CSV

A web-based interface to ingest CSV data into IntelMQ with on-line validation and live feedback.

This interface allows inserting "one-shot" data feeds into IntelMQ without the need to configure bots in IntelMQ.

Developed and maintained by [CERT.at](https://cert.at).

→ [Repository: intelmq-webinput-csv](https://github.com/certat/intelmq-webinput-csv)

![IntelMQ Webinput CSV Preview page](https://raw.githubusercontent.com/certat/intelmq-webinput-csv/c20413a401c2077140dd17fb7651db1132fde648/docs/images/screenshot.png)

### IntelMQ Mailgen

A solution allowing an IntelMQ setup with a complex contact database, managed by a web interface and sending out aggregated email reports. In different words: To send grouped notifications to network owners using SMTP.

Developed and maintained by [Intevation](https://intevation.de), initially funded by [BSI](https://bsi.bund.de/).

It consists of the following three components, which can also be used on their own.

#### IntelMQ CertBUND Contact

The certbund-contact consists of two IntelMQ expert bots, which fetch and process the information from the contact database, and scripts to import RIPE data into the contact database. Based on user-defined rules, the experts determine to which contact the event is to be sent to, and which e-mail template and attachment format to use.

→ [Repository: intelmq-certbund-contact](https://github.com/Intevation/intelmq-certbund-contact)

#### IntelMQ Fody

Fody is a web based interface for Mailgen. It allows to read and edit contacts, query sent mails (tickets) and call up data from the PostgreSQL database.

It can also be used to just query the database without using Mailgen.

![IntelMQ Fody Dashboard](https://raw.githubusercontent.com/Intevation/intelmq-fody/6e41b836d0a2c350a5f2c5c95a4b3be4d3f46027/docs/images/landing_page.png)

→ [Repository: intelmq-fody](https://github.com/Intevation/intelmq-fody)

→ [Repository:
intelmq-fody-backend](https://github.com/Intevation/intelmq-fody-backend)

#### intelmq-mailgen

Sends emails with grouped event data to the contacts determined by the certbund-contact. Mails can be encrypted with
PGP.

→ [Repository:
intelmq-mailgen](https://github.com/Intevation/intelmq-mailgen)

### "Constituency Portal" tuency

A web application helping CERTs to enable members of their constituency to self-administrate how they get warnings related to their network objects (IP addresses, IP ranges, autonomous systems, domains). *tuency* is developed by [Intevation](https://intevation.de/) for [CERT.at](https://cert.at).

If features organizational hierarchies, contact roles, self-administration and network objects per organization (Autonomous systems, network ranges, (sub)domains, RIPE organization handles). A network object claiming and approval process prevents abuse. An hierarchical rule-system on the network objects allow fine-grained settings. The tagging system for contacts and organization complement the contact-management features of the portal. Authentication is based on keycloak, which enables the re-use of the user accounts in the portal. The integrated API enables IntelMQ to query the portal for the right abuse contact and notification settings with the `intelmq.bots.experts.tuency.expert` expert bot.

![Tuency Netobjects Overview](https://gitlab.com/intevation/tuency/tuency/-/raw/64b95ec0/docs/images/netobjects.png)

→ [Repository: tuency](https://gitlab.com/Intevation/tuency/tuency)

### "Constituency Portal" do-portal (deprecated)

!!! warning
    The *do-portal* is deprecated and succeeded by *tuency*.

A contact portal with organizational hierarchies, role functionality and network objects based on RIPE, allows
self-administration by the contacts. Can be queried from IntelMQ and integrates the stats-portal.

Originally developed by [CERT-EU](https://cert.europa.eu/), then adapted by [CERT.at](https://cert.at).

→ [Repository: do-portal](https://github.com/certat/do-portal)

### Stats Portal

A Grafana-based statistics portal for the `eventdb`{.interpreted-text role="doc"}. Can be integrated into do-portal. It uses aggregated data to serve statistical data quickly.

![Stats Portal Architecture](https://raw.githubusercontent.com/certtools/stats-portal/38515266aabdf661a0b4becd8e921b03f32429fa/architecture-overview-stats-portal-screen.png)

→ [Repository: stats-portal](https://github.com/certtools/stats-portal)

### Malware Name Mapping

A mapping for malware names of different feeds with different names to a common family name.

→ [Repository: malware_name_mapping](https://github.com/certtools/malware_name_mapping)

### IntelMQ-Docker

A repository with tools for IntelMQ docker instance.

Developed and maintained by [CERT.at](https://cert.at).

→ [Repository: intelmq-docker](https://github.com/certat/intelmq-docker)

## Useful scripts

The list of useful scripts contributed to the IntelMQ universe can be found in the main repository.

→ [Repository: intelmq/contrib](https://github.com/certtools/intelmq/tree/develop/contrib)