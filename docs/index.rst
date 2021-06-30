..
   SPDX-FileCopyrightText: 2020-2021 Birger Schacht
   SPDX-License-Identifier: AGPL-3.0-or-later

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
   user/hardware-requirements
   user/installation
   user/upgrade
   user/configuration-management
   user/bots
   user/intelmqctl
   user/feeds
   user/FAQ
   user/intelmq-api
   user/intelmq-manager

Connecting with other systems
=============================

.. toctree::
   :glob:
   :maxdepth: 1

   user/ecosystem
   user/ELK-Stack
   user/MISP-Integrations
   user/n6-integrations
   user/eventdb
   user/abuse-contacts


Getting involved
================

.. toctree::
   :maxdepth: 1

   dev/guide
   dev/data-format
   dev/harmonization-fields
   dev/release-procedure
   dev/feeds-wishlist

Licence
=======

This software is licensed under GNU Affero General Public License version 3

Funded by
=========

This project was partially funded by the CEF framework

.. figure:: https://ec.europa.eu/inea/sites/default/files/ceflogos/en_horizontal_cef_logo_2.png
   :alt: Co-financed by the Connecting Europe Facility of the European Union

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
