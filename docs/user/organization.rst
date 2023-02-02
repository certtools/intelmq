..
   SPDX-FileCopyrightText: 2022 Sebastian Wagner
   SPDX-License-Identifier: AGPL-3.0-or-later

IntelMQ Organizational Structure
################################

.. contents::

The central IntelMQ components are maintained by multiple people and organizations in the IntelMQ community.
Please note that some components of the :doc:`universe` can have a different project governance, but all are part of the IntelMQ universe and community.

IntelMQ Enhancement Proposals (IEP)
***********************************

Major changes, including architecture, strategy and the internal data format, require so-called IEPs, IntelMQ Enhancement Proposals.
Their name is based on the famous `"PEPs" of Python <https://peps.python.org/>`_.

IEPs are collected in the separate `iep repository <github.com/certtools/ieps/>`_.

Code-Reviews and Merging
------------------------

Every line of code checked in for the IntelMQ Core, is checked by at least one trusted developer (excluding the author of the changes) of the IntelMQ community.
Afterwards, the code can be merged. Currently, these three contributors, have the permission to push and merging code to IntelMQ Core, Manager and API:
 * Aaron Kaplan (`aaronkaplan <https://github.com/aaronkaplan>`_)
 * Sebastian Wagner (`sebix <https://github.com/sebix>`_)
 * Sebastian Waldbauer (`waldbauer-certat <https://github.com/waldbauer-certat>`_)

Additionally, these people significantly contributed to IntelMQ:
 * Bernhard Reiter
 * Birger Schacht
 * Edvard Rejthar
 * Filip Pokorný
 * Karl-Johan Karlsson
 * Marius Karotkis
 * Marius Urkus
 * Mikk Margus Möll
 * navtej
 * Pavel Kácha
 * Robert Šefr
 * Tomas Bellus
 * Zach Stone

Short history
-------------

The idea and overall concept of an free, simple and extendible software for automated incident handling was born at an meeting of several European CSIRTs in Heraklion, Greece, in 2014.
Following the event, `Tomás Lima "SYNchroACK" <https://github.com/synchroack>`_ (working at CERT.pt back then) created IntelMQ from scratch. IntelMQ was born on June 24th, 2014.
A major support came from CERT.pt at this early stage.
Aaron Kaplan (CERT.at until 2020) engaged in the long-term advancement and from 2015 on, CERT.at took the burden of the maintenance and development (Sebastian Wagner 2015-2021 at CERT.at).
From 2016 onward, CERT.at started projects, initiated and lead by Aaron Kaplan, receiving CEFF-funding from the European Union to support IntelMQ's development.
IntelMQ became a software component of the EU-funded MeliCERTes framework for CSIRTs.

In 2020, IntelMQ's organizational structure and architectural development gained new thrive by the newly founded Board and the start of the IEP process, creating more structure and more transparency in the IntelMQ community's decisions.
