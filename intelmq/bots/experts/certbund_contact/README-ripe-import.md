RIPE DB data import script
==========================

This script can be used to import automatic contact data to the
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

Download data to a directory:

```
mkdir /tmp/ripe
cd /tmp/ripe
for db in ripe.db.organisation.gz ripe.db.role.gz ripe.db.aut-num.gz
 do
  wget "http://ftp.ripe.net/ripe/dbase/split/$db"
 done
```

Now import the data into your ContactDB, we assume you used `contactdb` as
database name.

**You need to be the user `postgres` to do this!**

The next step assumes you are currently in the same folder like the data you
downloaded.

```
cd /tmp/ripe
su postgres
ripe_import.py --database contactdb --verbose
```

In case you are somewhere else, use:

```
su postgres
ripe_import.py --database contactdb \
    --organisation-file=/tmp/ripe/ripe.db.organisation.gz \
    --role-file=/tmp/ripe/ripe.db.role.gz \
    --asn-file=/tmp/ripe/ripe.db.aut-num.gz \
    --verbose
```

See also the help provided by ``--help``
