..
   SPDX-FileCopyrightText: 2019-2021 Sebastian Wagner
   SPDX-License-Identifier: AGPL-3.0-or-later

IntelMQ Ecosystem
=================


IntelMQ is more than a the core library itself and many programs are developed around in the IntelMQ initiative.
This document provides an overview of the ecosystem and all related tools. If you think something is missing, please let us know!

IntelMQ "Core"
--------------

This is IntelMQ itself, as it is available on `github <https://github.com/certtools/intelmq>`_.

It includes all the bots, the harmonization, etc.

IntelMQ Manager
---------------

The Manager is the most known software and can be seen as the face of IntelMQ.
This software provides a graphical user interface to the management tool `intelmqctl`.

→ `Repository: IntelMQ Manager <https://github.com/certtools/intelmq-manager/>`_

intelmq-webinput-csv
--------------------

A web-based interface to inject CSV data into IntelMQ with on-line validation and live feedback.

→ `Repository: intelmq-webinput-csv <https://github.com/certat/intelmq-webinput-csv>`_

intelmq-cb-mailgen
------------------

A solution allowing
an IntelMQ setup with a complex contact database,
managed by a web interface and sending out aggregated email reports.
(In different words:
To send grouped notifications to network owners using SMTP.)

→ `Repository: intelmq-cb-mailgen <https://github.com/Intevation/intelmq-mailgen-release>`_


IntelMQ Fody + Backend
^^^^^^^^^^^^^^^^^^^^^^

Fody is a web based interface for intelmq-mailgen's contact database
and the :doc:`eventdb`. It can also be used to just query the :doc:`eventdb`.

The certbund-contact expert fetches the information from this contact database and provides scripts to import RIPE data into the contact database.

→ `Repository: intelmq-fody <https://github.com/Intevation/intelmq-fody>`_

→ `Repository: intelmq-fody-backend <https://github.com/Intevation/intelmq-fody-backend>`_

→ `Repository: intelmq-certbund-contact <https://github.com/Intevation/intelmq-certbund-contact>`_

intelmq-mailgen
^^^^^^^^^^^^^^^

The email sending part:

→ `Repository: intelmq-mailgen <https://github.com/Intevation/intelmq-mailgen>`_


"Constituency Portal" tuency
----------------------------

A web application helping CERTs to enable members of their constituency
to self-administrate how they get warnings related to their network objects
(IP addresses, IP ranges, autonomous systems, domains).
*tuency* is developed by `Intevation <https://intevation.de/>`_ for
`CERT.at <https://cert.at/>`_.

If features organizational hierarchies, contact roles, self-administration
and network objects per organization (Autonomous systems, network ranges,
(sub-)domains, RIPE organization handles). A network object claiming and
approval process prevents abuse.
An hierarchical rule-system on the network objects allow fine-grained settings.
The tagging system for contacts and organization complement the
contact-management features of the portal.
Authentication is based on keycloak, which enables the re-use of the user
accounts in the portal.
The integrated API enables IntelMQ to query the portal for the right abuse
contact and notification settings with the
:ref:`intelmq.bots.experts.tuency.expert` expert.

→ `Repository: tuency <https://gitlab.com/Intevation/tuency/tuency>`_


"Constituency Portal" do-portal (not developed any further)
-----------------------------------------------------------

*Note:* The *do-portal* is deprecated and succeeded by *tuency*.

A contact portal with organizational hierarchies, role functionality and network objects based on RIPE, allows self-administration by the contacts.
Can be queried from IntelMQ and integrates the stats-portal.

→ `Repository: do-portal <https://github.com/certat/do-portal>`_

stats-portal
------------

A Grafana-based statistics portal for the :doc:`eventdb`. Integrated in do-portal.

→ `Repository: stats-portal <https://github.com/certtools/stats-portal>`_

Malware Name Mapping
--------------------

A mapping for malware names of different feeds with different names to a common family name.

→ `Repository: malware_name_mapping <https://github.com/certtools/malware_name_mapping>`_

IntelMQ-Docker
--------------

A repository with tools for IntelMQ docker instance.

→ `Repository: intelmq-docker <https://github.com/certat/intelmq-docker>`_
