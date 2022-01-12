..
   SPDX-FileCopyrightText: 2019-2021 Sebastian Wagner
   SPDX-License-Identifier: AGPL-3.0-or-later

MISP integrations in IntelMQ
============================

While MISP and IntelMQ seem to solve similar problems in the first hindsight, their intentions and strengths differ significantly.

In a nutshell, MISP *stores* manually curated indicators (called *attributes*) grouped in *events*. An event can have an arbitrary number of attributes.
MISP correlates these indicators with each other and can synchronize the data between multiple MISP instances.

On the other side, IntelMQ in it's essence (not considering the :doc:`EventDB <eventdb>`) has no state or database, but is stream-oriented.
IntelMQ acts as a toolbox which can be configured as needed to automate processes of mass data with little or no human interaction
At the end of the processing the data may land in some database or be sent to other systems.

Both systems do not intend to replace each other or do compete.
They integrate seamless and combine each other enabling more use-cases and

MISP API Collector
-------------------------------

The MISP API Collector fetches data from MISP via the `MISP API <https://misp.gitbooks.io/misp-book/content/automation/>`_.

Look at the :ref:`Bots' documentation <intelmq.bots.collectors.misp.collector>` for more information.

MISP Expert
-------------------------------

The MISP Expert searches MISP by using the `MISP API <https://misp.gitbooks.io/misp-book/content/automation/>`_
for attributes/events matching the ``source.ip`` of the event.
The MISP Attribute UUID and MISP Event ID of the newest attribute are added to the event.

Look at the :ref:`Bots' documentation <intelmq.bots.experts.misp.expert>` for more information.

MISP Feed Output
-------------------------------

This bot creates a complete `MISP feed <https://misp.gitbooks.io/misp-book/content/managing-feeds/>`_ ready to be configured in MISP as incoming data source.

Look at the :ref:`Bots' documentation <intelmq.bots.outputs.misp.output_feed>` for more information.


MISP API Output
-------------------------------

Can be used to directly create MISP events in a MISP instance by using the `MISP API <https://misp.gitbooks.io/misp-book/content/automation/>`_.

Look at the :ref:`Bots' documentation <intelmq.bots.outputs.misp.output_api>` for more information.
