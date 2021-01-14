IntelMQ
-------


.. figure:: _static/Logo_Intel_MQ.png
   :alt: IntelMQ

|Build Status| |codecov.io| |CII Badge|

.. |Build Status| image:: https://github.com/certtools/intelmq/workflows/Nosetest%20test%20suite/badge.svg
   :target: https://github.com/certtools/intelmq/actions
.. |codecov.io| image:: https://codecov.io/github/certtools/intelmq/coverage.svg?branch=develop
   :target: https://codecov.io/github/certtools/intelmq?branch=master
.. |CII Badge| image:: https://bestpractices.coreinfrastructure.org/projects/4186/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/4186/

**IntelMQ** is a solution for IT security teams (CERTs & CSIRTs, SOCs abuse
departments, etc.) for collecting and processing security feeds (such as
log files) using a message queuing protocol. It's a community driven
initiative called **IHAP** (Incident Handling Automation Project) which
was conceptually designed by European CERTs/CSIRTs during several
InfoSec events. Its main goal is to give to incident responders an easy
way to collect & process threat intelligence thus improving the incident
handling processes of CERTs.

User guide
==========

.. toctree::
   :glob:
   :maxdepth: 1

   user/introduction
   user/installation
   user/upgrade
   user/configuration-management
   user/bots
   user/intelmqctl
   user/feeds
   user/ecosystem
   user/intelmq-api
   user/ELK-Stack
   user/FAQ
   user/MISP-Integrations
   user/n6-integrations


Getting involved
================

.. toctree::
   :maxdepth: 1

   dev/guide
   dev/data-harmonization
   dev/harmonization-fields
   dev/release-procedure
   dev/feeds-wishlist

Licence
=======

This software is licensed under GNU Affero General Public License version 3

Funded by
=========

This project was partially funded by the CEF framework

.. figure:: _static/cef_logo.png
   :alt: Co-financed by the Connecting Europe Facility of the European Union

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
