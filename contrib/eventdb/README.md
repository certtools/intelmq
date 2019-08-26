EventDB Utilities
=================

- Apply Malware Name Mapping: Applies the malware name mapping to the eventdb. Source and destination columns can be given, also a local file. If no local file is present, the mapping can be downloaded on demand.
  It queries the database for all distinct malware names with the taxonomy "malicious code" and sets another column to the malware family name.
- Apply Domain Suffix: Writes the public domain suffix to the `source.domain_suffix` / `destination.domain_suffix` columns, extracted from `source.fqdn` / `destination.fqdn`.

Usage
-----

Both scripts can connect to a postgres server with the "eventdb" table. The command line arguments interface for both scripts is the same.
See `--help` for more information.

```
apply_mapping_eventdb.py -h
apply_domain_suffix.py -h
```
