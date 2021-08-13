..
   SPDX-FileCopyrightText: 2020-2021 Birger Schacht
   SPDX-License-Identifier: AGPL-3.0-or-later

############
Introduction
############

*****
About
*****

**IntelMQ** is a solution for IT security teams (CERTs & CSIRTs, SOCs abuse
departments, etc.) for collecting and processing security feeds (such as
log files) using a message queuing protocol. It's a community driven
initiative called **IHAP** (Incident Handling Automation Project) which
was conceptually designed by European CERTs/CSIRTs during several
InfoSec events. Its main goal is to give to incident responders an easy
way to collect & process threat intelligence thus improving the incident
handling processes of CERTs.

**Incident Handling Automation Project**

- **URL:** <http://www.enisa.europa.eu/activities/cert/support/incident-handling-automation>
- **Mailing-list:** <ihap@lists.trusted-introducer.org>

Several pieces of software are evolved around IntelMQ. For an overview,
look at the :doc:`ecosystem`.

IntelMQ can be used for
- automated incident handling
- situational awareness
- automated notifications
- as data collector for other tools
- etc.

IntelMQ's design was influenced by
`AbuseHelper <https://github.com/abusesa/abusehelper>`__ however it was
re-written from scratch and aims at:

-  Reducing the complexity of system administration
-  Reducing the complexity of writing new bots for new data feeds
-  Reducing the probability of events lost in all process with
   persistence functionality (even system crash)
-  Use and improve the existing Data Harmonization Ontology
-  Use JSON format for all messages
-  Provide easy way to store data into Log Collectors like
   ElasticSearch, Splunk, databases (such as PostgreSQL)
-  Provide easy way to create your own black-lists
-  Provide easy communication with other systems via HTTP RESTful API

It follows the following basic meta-guidelines:

-  Don't break simplicity - KISS
-  Keep it open source - forever
-  Strive for perfection while keeping a deadline
-  Reduce complexity/avoid feature bloat
-  Embrace unit testing
-  Code readability: test with inexperienced programmers
-  Communicate clearly

*****
Usage
*****

Various approaches of installing `intelmq`  are described in :doc:`installation`.

The :doc:`configuration-management` gives an overview how a `intelmq` installation is set up and how to configure and maintain the setup.
There is also a list of available :doc:`feeds` as well as a detailed description of the different :doc:`bots` intelmq brings with it.

If you know additional feeds and how to parse them, please contribute your code or your configuration (by issues or the mailing lists).

For support questions please use the |intelmq-users-list-link|.

IntelMQ Manager
===============

Check out `this graphical tool <https://github.com/certtools/intelmq-manager>`_ to easily manage an IntelMQ system.

**********
Contribute
**********

- Subscribe to the |intelmq-developers-list-link|
- IRC: server: irc.freenode.net, channel: \#intelmq
- Via `GitHub issues <github.com/certtools/intelmq/issues/>`_
- Via `Pull requests <github.com/certtools/intelmq/pulls>`_ (please have a look at the :doc:`/dev/guide` first)
