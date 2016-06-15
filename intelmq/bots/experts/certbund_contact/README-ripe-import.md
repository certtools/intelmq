RIPE DB data import script
==========================

This script can be used to import automatic contact data to the certBUND
contact database. It is intended to be called automatically, e.g. by a
cronjob.

It expects the files

* ripe.db.organisation.gz
* ripe.db.role.gz
* ripe.db.aut-num.gz

to be present in the same folder as the script. These files can be downloaded
from the RIPE website (ftp://ftp.ripe.net/ripe/dbase/split/).


Usage
=====

Example usage:
```
 importer.py --database contactdb
```

See also the help provided by ``--help``
