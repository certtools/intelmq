..
   SPDX-FileCopyrightText: 2019 Sebastian Wagner
   SPDX-License-Identifier: AGPL-3.0-or-later

MISP integrations in IntelMQ
============================

MISP API Collector
-------------------------------

The MISP API Collector fetches data from MISP via the MISP API.

Look at the Bots' documentation for more information.

MISP Expert
-------------------------------

The MISP Expert searches MISP by API
for attributes/events matching the `source.ip` of the event.
The MISP Attribute UUID and MISP Event ID of the newest attribute are added to the event.

Look at the Bots' documentation for more information.

MISP Feed Output
-------------------------------

This bot creates a complete "MISP feed" ready to be configured in MISP as incoming data source.

Look at the Bots' documentation for more information.


MISP API Output
-------------------------------

Can be used to directly create MISP events in a MISP instance.

Look at the Bots' documentation for more information.
