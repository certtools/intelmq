Welcome to IntelMQ!
===================

![IntelMQ](https://raw.githubusercontent.com/certtools/intelmq/master/docs/images/Logo_Intel_MQ.png)

[![Build
Status](https://travis-ci.org/certtools/intelmq.svg?branch=master)](https://travis-ci.org/certtools/intelmq)
[![codecov.io](https://codecov.io/github/certtools/intelmq/coverage.svg?branch=master)](https://codecov.io/github/certtools/intelmq?branch=master)

**IntelMQ** is a solution for IT security teams (CERTs, CSIRTs, abuse
departments,...) for collecting and processing security feeds (such as
log files) using a message queuing protocol. It's a community driven
initiative called **IHAP** (Incident Handling Automation Project) which
was conceptually designed by European CERTs/CSIRTs during several
InfoSec events. Its main goal is to give to incident responders an easy
way to collect & process threat intelligence thus improving the incident
handling processes of CERTs.

IntelMQ's design was influenced by
[AbuseHelper](https://github.com/abusesa/abusehelper)
however it was re-written from scratch and aims at:

-   Reduce the complexity of system administration
-   Reduce the complexity of writing new bots for new data feeds
-   Reduce the probability of events lost in all process with
    persistence functionality (even system crash)
-   Use and improve the existing Data Harmonization Ontology
-   Use JSON format for all messages
-   Integration of the existing tools (AbuseHelper, CIF)
-   Provide easy way to store data into Log Collectors like
    ElasticSearch, Splunk, databases (such as PostgreSQL)
-   Provide easy way to create your own black-lists
-   Provide easy communication with other systems via HTTP RESTFUL API

It follows the following basic meta-guidelines:

-   Don't break simplicity - KISS
-   Keep it open source - forever
-   Strive for perfection while keeping a deadline
-   Reduce complexity/avoid feature bloat
-   Embrace unit testing
-   Code readability: test with unexperienced programmers
-   Communicate clearly

Table of Contents
-----------------

1.  [How to Install](#how-to-install)
2.  [Developers Guide](#developers-guide)
3.  [User Guide](#user-guide)
3.  [IntelMQ Manager](#intelmq-manager)
4.  [Incident Handling Automation Project](#incident-handling-automation-project)
5.  [Data Harmonization](#data-harmonization)
6.  [How to Participate](#how-to-participate)
7.  [Licence](#licence)

How to Install
--------------

See [INSTALL](INSTALL.md).

Developers Guide
----------------

See [Developers Guide](Developers-Guide.md).

User Guide
----------------

See [User Guide](User-Guide.md).

For support use the intelmq-users mailing list: <https://lists.cert.at/cgi-bin/mailman/listinfo/intelmq-users>

IntelMQ Manager
---------------

Check out this graphical
[tool](https://github.com/certtools/intelmq-manager) and easily manage
an IntelMQ system.

Incident Handling Automation Project
------------------------------------

-   **URL:**
    <http://www.enisa.europa.eu/activities/cert/support/incident-handling-automation>
-   **Mailing-list:** <ihap@lists.trusted-introducer.org>

Data Harmonization
------------------

IntelMQ use the Data Harmonization. Check the following
[document](Data-Harmonization.md).

How to participate
------------------

-   Subscribe to the Intelmq-dev Mailing list:
    <https://lists.cert.at/cgi-bin/mailman/listinfo/intelmq-dev> (for
    developers)
-   Watch out for our regular developers conf call
-   IRC: server: irc.freenode.net, channel: \#intelmq
-   Via github issues
-   Via Pull requests (please do read help.github.com first)

Licence
-------

This software is licensed under GNU Affero General Public License
version 3
