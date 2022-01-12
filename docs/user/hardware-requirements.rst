..
   SPDX-FileCopyrightText: 2021 Sebastian Wagner
   SPDX-License-Identifier: AGPL-3.0-or-later

#####################
Hardware Requirements
#####################

Do you ask yourself how much RAM do you need to give your new IntelMQ virtual machine?

The honest answer is simple and pointless: It depends ;)

.. contents::

****************************************
IntelMQ and the messaging queue (broker)
****************************************

IntelMQ uses a messaging queue to move the messages between the bots.
All bot instances can only process one message at a time, therefore all other messages need to wait in the queue.
As not all bots are equally fast, the messages will naturally "queue up" before the slower ones.
Further, parsers produce many events with just one message (the report) as input.

The following estimations assume Redis as messaging broker which is the default for IntelMQ.
When RabbitMQ is used, the required resources will differ, and RabbitMQ can handle system overload and therefore a shortage of memory.

As Redis stores all data in memory, the data which is processed at any point in time must fit there, including overheads. Please note that IntelMQ does *neither store nor cache* any input data. These estimates therefore only relate to the processing step, not the storage.

For a minimal system, these requirements suffice:

- 4 GB of RAM
- 2 CPUs
- 10 GB disk size

**Depending on your data input, you will need the twentiethfold of the input data size as memory for processing.**

When using `Redis persistence <http://redis.io/topics/persistence>`_, you will additionally need twice as much memory for Redis.

Disk space
==========

Disk space is only relevant if you save your data to a file, which is not recommended for production setups, and only useful for testing and evaluation.

Do not forget to rotate your logs or use syslog, especially if you use the logging level "DEBUG".
logrotate is in use by default for all installation with deb/rpm packages. When other means of installation are used (pip, manual), configure log rotation manually. See :ref:`configuration-logging`.

Background on memory
====================
For experimentation, we used multiple Shadowserver Poodle reports for demonstration purpose, totaling in 120 MB of data. All numbers are estimates and are rounded.
In memory, the report data requires 160 MB. After parsing, the memory usage increases to 850 MB in total, as every data line is stored as JSON, with additional information plus the original data encoded in Base 64.
The further processing steps depend on the configuration, but you can estimate that caches (for lookups and deduplication) and other added information cause an additional size increase of about 2x.
Once a dataset finished processing in IntelMQ, it is no longer stored in memory. Therefore, the memory is only needed to catch high load.

The above numbers result in a factor of 14 for input data size vs. memory required by Redis. Assuming some overhead and memory for the bots' processes, a factor of 20 seems sensible.

To reduce the amount of required memory and disk size, you can optionally remove the `raw` data field, see :ref:`faq-remove-raw-data` in the FAQ.

*********************
Additional components
*********************

If some of the `optional` components of the :doc:`ecosystem` are in use, they can add additional hardware requirements.

Those components do not add relevant requirements:

- IntelMQ API: It is just an API for `intelmqctl`.
- IntelMQ Manager: Only contains static files served by the webserver.
- IntelMQ Webinput CSV: Just a webinterface to insert data. Requires the amount of processed data to fit in memory, see above.
- Stats Portal: The aggregation step and Graphana require some resources, but no exact numbers are known.
- Malware Name Mapping
- Docker: The docker layer adds only minimal hardware requirements.

EventDB
=======

When storing data in databases (such as MongoDB, PostgreSQL, ElasticSearch), it is recommended to do this on separate machines for operational reasons.
Using a different machine results in a separation of stream processing to data storage and allows for a specialized system optimization for both use-cases.

IntelMQ cb mailgen
=============================

While the Fody backend and frontend do not have significant requirements, the `RIPE import tool of the certbund-contact <https://github.com/Intevation/intelmq-certbund-contact/blob/master/README-ripe-import.md>`_ requires about 8 GB of memory as of March 2021.
