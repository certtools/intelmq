Welcome to IntelMQ!
===================

.. figure:: https://raw.githubusercontent.com/certtools/intelmq/master/docs/images/Logo_Intel_MQ.png
   :alt: IntelMQ

|Build Status| |codecov.io|

**IntelMQ** is a solution for IT security teams (CERTs, CSIRTs, abuse
departments,...) for collecting and processing security feeds (such as
log files) using a message queuing protocol. It's a community driven
initiative called **IHAP** (Incident Handling Automation Project) which
was conceptually designed by European CERTs/CSIRTs during several
InfoSec events. Its main goal is to give to incident responders an easy
way to collect & process threat intelligence thus improving the incident
handling processes of CERTs.

Several pieces of software are evolved around IntelMQ. For an overview,
look at the `Ecosystem document  <docs/Ecosystem.md>`__.

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
-  Code readability: test with unexperienced programmers
-  Communicate clearly

Table of Contents
-----------------

1. `How to Install <#how-to-install>`__
2. `Developers Guide <#developers-guide>`__
3. `User Guide <#user-guide>`__
4. `IntelMQ Manager <#intelmq-manager>`__
5. `Incident Handling Automation
   Project <#incident-handling-automation-project>`__
6. `Data Harmonization <#data-harmonization>`__
7. `How to Participate <#how-to-participate>`__
8. `Licence <#licence>`__
9. `Funded by <#funded-by>`__

How to Install
--------------

See `INSTALL <docs/INSTALL.md>`__.

Developers Guide
----------------

See `Developers Guide <docs/Developers-Guide.md>`__.

User Guide
----------

See `User Guide <docs/User-Guide.md>`__.
Which Feeds are supported? Have a look at the `Feeds documentation <docs/Feeds.md>`__ and the `Bots documentation <docs/Bots.md>`__.
If you know additional feeds and how to parse them, please contribute your code or your configuration (by issues or the mailing lists).

For support questions please use the intelmq-users mailing list:
https://lists.cert.at/cgi-bin/mailman/listinfo/intelmq-users

IntelMQ Manager
---------------

Check out this graphical
`tool <https://github.com/certtools/intelmq-manager>`__ and easily
manage an IntelMQ system.

Incident Handling Automation Project
------------------------------------

- **URL:**
  http://www.enisa.europa.eu/activities/cert/support/incident-handling-automation
- **Mailing-list:** ihap@lists.trusted-introducer.org

Data Harmonization
------------------

IntelMQ use the Data Harmonization. Please read `this
document <docs/Data-Harmonization.md>`__ for more details.

How to participate
------------------

- Subscribe to the Intelmq-dev Mailing list:
  https://lists.cert.at/cgi-bin/mailman/listinfo/intelmq-dev (for
  developers)
- Watch out for our regular developers conf call
- IRC: server: irc.freenode.net, channel: #intelmq
- Via github issues
- Via Pull requests (please do read help.github.com first)

Licence
-------

This software is licensed under GNU Affero General Public License
version 3

Funded by
---------

This project was partially funded by the CEF framework

.. figure:: docs/images/cef_logo.png
   :alt: Co-financed by the Connecting Europe Facility of the European Union

.. |Build Status| image:: https://travis-ci.org/certtools/intelmq.svg?branch=master
   :target: https://travis-ci.org/certtools/intelmq
.. |codecov.io| image:: https://codecov.io/github/certtools/intelmq/coverage.svg?branch=master
   :target: https://codecov.io/github/certtools/intelmq?branch=master
