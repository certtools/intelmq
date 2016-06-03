Contact data import script
==========================

This script can be used to import automatic contact data to the certBUND
contact database. It is intended to be called automatically, e.g. by a
cronjob.


Usage
=====

Example usage:
```
   cdb_import.py --database contactdb \
                 --network-file delegated-ripencc-latest \
                 --asn-file asn_abuse_c.txt \
                 --verbose
```

See also the help provided by ``--help``
