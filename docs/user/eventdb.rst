..
   SPDX-FileCopyrightText: 2021 Birger Schacht
   SPDX-License-Identifier: AGPL-3.0-or-later

=======
EventDB
=======

The EventDB is not a software itself.

The EventDB is a database (usually PostgreSQL) that gets filled with with data from intelmq using the SQL Output bot.

-----------------
EventDB Utilities
-----------------

Some scripts related to the eventdb are located in the `contrib/eventdb <https://github.com/certtools/intelmq/tree/develop/contrib/eventdb>`_ folder in the IntelMQ git repository.

Apply Malware Name Mapping
--------------------------

The `apply_mapping_eventdb.py` script applies the malware name mapping to the eventdb.
Source and destination columns can be given, also a local file. If no local file is present, the mapping can be downloaded on demand.
It queries the database for all distinct malware names with the taxonomy "malicious-code" and sets another column to the malware family name.


Apply Domain Suffix
-------------------

The `apply_domain_suffix.py` script writes the public domain suffix to the `source.domain_suffix` / `destination.domain_suffix` columns, extracted from `source.fqdn` / `destination.fqdn`.

Usage
^^^^^

The Python scripts can connect to a PostgreSQL server with an `eventdb` database and an `events` table. The command line arguments interface for both scripts are the same.
See `--help` for more information:

.. code-block:: bash

   apply_mapping_eventdb.py -h
   apply_domain_suffix.py -h


PostgreSQL trigger
------------------

PostgreSQL trigger is a trigger keeping track of the oldest inserted/updated "time.source" data. This can be useful to (re-)generate statistics or aggregation data.


The SQL script can be executed in the database directly.

------------------
EventDB Statistics
------------------

The EventDB provides a great base for statistical analysis of the data.

The `eventdb-stats repository <https://github.com/wagner-certat/eventdb-stats>`_ contains a Python script that generates an HTML file and includes the `Plotly JavaScript Open Source Graphing Library <https://plotly.com/javascript/>`_.
By modifying the configuration file it is possible to configure various queries that are then displayed using graphs:

.. image:: /_static/eventdb_stats.png
   :alt: EventDB Statistics Example


-------------------------------
Using EventDB with Timescale DB
-------------------------------

TBD
