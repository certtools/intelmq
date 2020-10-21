Welcome to IntelMQ!
===================

.. figure:: https://raw.githubusercontent.com/certtools/intelmq/master/docs/images/Logo_Intel_MQ.png
   :alt: IntelMQ

|Build Status| |codecov.io| |CII Badge|

**IntelMQ** is a solution for IT security teams (CERTs & CSIRTs, SOCs, abuse
departments, etc.) for collecting and processing security feeds (such as
log files) using a message queuing protocol. It's a community driven
initiative called **IHAP** (Incident Handling Automation Project) which
was conceptually designed by European CERTs/CSIRTs during several
InfoSec events. Its main goal is to give to incident responders an easy
way to collect & process threat intelligence thus improving the incident
handling processes of CERTs.

Several pieces of software are evolved around IntelMQ. For an overview,
look at the `Ecosystem document  <https://intelmq.readthedocs.io/en/latest/guides/Ecosystem.html>`__.

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
-  Code readability: test with unexperienced programmers
-  Communicate clearly

Table of Contents
-----------------

1. `How to Install <#how-to-install>`__
2. `User Guide <#user-guide>`__
3. `IntelMQ Manager and more tools <#intelmq-manager-and-more-tools>`__
4. `How to Participate <#how-to-participate>`__
5. `Incident Handling Automation
   Project <#incident-handling-automation-project>`__
6. `Licence <#licence>`__
7. `Funded by <#funded-by>`__

How to Install
--------------

See `INSTALL <https://intelmq.readthedocs.io/en/latest/guides/INSTALL.html>`__.

User Guide
----------

See `User Guide <https://intelmq.readthedocs.io/en/latest/guides/User-Guide.html>`__.
Which Feeds are supported? Have a look at the `Feeds documentation <https://intelmq.readthedocs.io/en/latest/guides/Feeds.html>`__
and the `Bots documentation <https://intelmq.readthedocs.io/en/latest/guides/Bots.html>`__.
If you know additional feeds and how to parse them, please contribute your code or your configuration (by issues or the mailing lists).

For support questions please use the intelmq-users mailing list:
https://lists.cert.at/cgi-bin/mailman/listinfo/intelmq-users

IntelMQ use the Data Harmonization. Please read `this
document <https://intelmq.readthedocs.io/en/latest/guides/Data-Harmonization.html>`__ for more details.

IntelMQ Manager and more tools
------------------------------

Check out this graphical
`tool <https://github.com/certtools/intelmq-manager>`__ and easily
manage an IntelMQ system.

More tools can be found in the `ecosystem documentation <https://intelmq.readthedocs.io/en/latest/guides/Ecosystem.html>`__.

How to participate
------------------

IntelMQ is a community project depending on your contributions. Please consider sharing your work.

- Have a look at our `Developers Guide <https://intelmq.readthedocs.io/en/latest/guides/Developers-Guide.html>`__ for documentation.
- Subscribe to the Intelmq-dev Mailing list to get answers to your development questions:
  https://lists.cert.at/cgi-bin/mailman/listinfo/intelmq-dev
- The `Github issues <github.com/certtools/intelmq/issues/>`__ lists all the open feature requests, bug reports and ideas.
- Looking for ideas which additional feeds you could add support for? The
  `Feeds whishlist <https://intelmq.readthedocs.io/en/latest/guides/Feeds-whishlist.html>`__ is the list you are looking for.
- Contribute code with pull requests (The `Github help <https://help.github.com/>`__ can be useful if you are not familiar with the system yet).
- Some developers are also on IRC: `channel #intelmq on irc.freenode.net <ircs://chat.freenode.net:6697/intelmq>`__.

Incident Handling Automation Project
------------------------------------

- **URL:**
  http://www.enisa.europa.eu/activities/cert/support/incident-handling-automation
- **Mailing-list:** ihap@lists.trusted-introducer.org

Licence
-------

This software is licensed under GNU Affero General Public License
version 3

Funded by
---------

This project was partially funded by the CEF framework

.. figure:: https://raw.githubusercontent.com/certtools/intelmq/develop/docs/guides/images/cef_logo.png
   :alt: Co-financed by the Connecting Europe Facility of the European Union

.. |Build Status| image:: https://travis-ci.org/certtools/intelmq.svg?branch=master
   :target: https://travis-ci.org/certtools/intelmq
.. |codecov.io| image:: https://codecov.io/github/certtools/intelmq/coverage.svg?branch=master
   :target: https://codecov.io/github/certtools/intelmq?branch=master
.. |CII Badge| image:: https://bestpractices.coreinfrastructure.org/projects/4186/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/4186/
