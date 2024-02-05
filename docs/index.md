<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

<!--
[![CII Badge](https://bestpractices.coreinfrastructure.org/projects/4186/badge)](https://bestpractices.coreinfrastructure.org/projects/4186/)
-->

![IntelMQ](docs/static/images/Logo_Intel_MQ.svg)

# Introduction

**IntelMQ** is a solution for IT security teams (CERTs & CSIRTs, SOCs
abuse departments, etc.) for collecting and processing security feeds
(such as log files) using a message queuing protocol. It's a community
driven initiative called **IHAP**[^1] (Incident Handling Automation Project)
which was conceptually designed by European CERTs/CSIRTs during several
InfoSec events. Its main goal is to give to incident responders an easy
way to collect & process threat intelligence thus improving the incident
handling processes of CERTs.

IntelMQ is frequently used for:

- automated incident handling
- situational awareness
- automated notifications
- as data collector for other tools
- and more!

The design was influenced by
[AbuseHelper](https://github.com/abusesa/abusehelper) however it was
re-written from scratch and aims at:

-   Reducing the complexity of system administration
-   Reducing the complexity of writing new bots for new data feeds
-   Reducing the probability of events lost in all process with persistence functionality (even system crash)
-   Use and improve the existing Data Harmonization Ontology
-   Use JSON format for all messages
-   Provide easy way to store data into databases and log collectors such as PostgreSQL, Elasticsearch and Splunk
-   Provide easy way to create your own black-lists
-   Provide easy communication with other systems via HTTP RESTful API

It follows the following basic meta-guidelines:

-   Don't break simplicity - KISS
-   Keep it open source - forever
-   Strive for perfection while keeping a deadline
-   Reduce complexity/avoid feature bloat
-   Embrace unit testing
-   Code readability: test with inexperienced programmers
-   Communicate clearly

## Contribute

- Subscribe to the [IntelMQ Developers mailing list](https://lists.cert.at/cgi-bin/mailman/listinfo/intelmq-dev) and engage in discussions
- Report any errors and suggest improvements via [issues](https://github.com/certtools/intelmq/issues)
- Read the Developer Guide and open a [pull request](https://github.com/certtools/intelmq/pulls)

[^1]: [Incident Handling Automation Project](https://www.enisa.europa.eu/activities/cert/support/incident-handling-automation), mailing list: ihap@lists.trusted-introducer.org


![CEF](https://ec.europa.eu/inea/sites/default/files/ceflogos/en_horizontal_cef_logo_2.png)
