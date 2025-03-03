<!--
SPDX-FileCopyrightText: 2019 Sebastian Wagner

SPDX-License-Identifier: AGPL-3.0-or-later
-->

EventDB Utilities
=================

- Apply Malware Name Mapping: Applies the malware name mapping to the eventdb. Source and destination columns can be given, also a local file. If no local file is present, the mapping can be downloaded on demand.
  It queries the database for all distinct malware names with the taxonomy "malicious-code" and sets another column to the malware family name.
- Apply Domain Suffix: Writes the public domain suffix to the `source.domain_suffix` / `destination.domain_suffix` columns, extracted from `source.fqdn` / `destination.fqdn`.
- `trigger_oldest_time.source.sql`: PostgreSQL trigger keeping track of the oldest inserted/updated "time.source" data. This can be useful to (re-)generate statistics or aggregation data.
- `to_json.py`: Export EventDB data to JSON, to use it in IntelMQ again.

Usage
-----

The Python scripts can connect to a PostgreSQL server with an `eventdb` database and an `events` table. The command line arguments interface for both scripts are the same.
See `--help` for more information:

```
apply_mapping_eventdb.py -h
apply_domain_suffix.py -h
to_json.py -h
```

The SQL script can be executed in the database directly.

### `to_json.py`


- Get an event by ID: `~intevation/to_json.py --id $id`
	- You can give multiple IDs
- Pretty printed: Add `--pretty`
- Inject the data into an IntelMQ bot (dry run):
	- `intelmqctl run $botid process --dry-run --show-sent --msg '$jsondata'`