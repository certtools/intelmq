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

For each contact that is created by this script, the format `feed_specific`
will be set as default. You can change this by using the parameter
`--notification-format`.

You can also set the notification intervall with `--notification-intervall`.
Default is 0. The intervall is set in seconds. 0: Immediate notification,
-1 No Notification, 60: 1 Minute, etc...

It is also possible to provide a whitelist of ASNs to load. Use the ``--asn-whitelist-file``
parameter to pass a filename. The script expects one AS entry per line, with
the AS-prefix, e.g. ``AS123``.

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
ripe_import.py --conninfo dbname=contactdb --verbose
```

If you start the script from a different working directory,
you can give the paths to the ripe files like:

```
su postgres
ripe_import.py --conninfo dbname=contactdb \
    --organisation-file=/tmp/ripe/ripe.db.organisation.gz \
    --role-file=/tmp/ripe/ripe.db.role.gz \
    --asn-file=/tmp/ripe/ripe.db.aut-num.gz \
    --verbose
```

See also the help provided by ``--help`` and the
[documentation of the libpg conninfo string](https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING).
The [documentaion on environment variables](https://www.postgresql.org/docs/current/static/libpq-envars.html) to the connection also
points towards how to savely provide a password with a ~/.pgpass file.
