RIPE DB data import
==========================
A set of tools to manage imports of ripe data into to the contact database.

The following input files are required:

* ripe.db.organisation.gz
* ripe.db.role.gz
* ripe.db.aut-num.gz

They will be searching in the current working directory by default.
The files can be downloaded
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

```shell
d=`date +%F`
mkdir $d
cd $d
for db in ripe.db.organisation.gz ripe.db.role.gz ripe.db.aut-num.gz
 do
  curl -O "http://ftp.ripe.net/ripe/dbase/split/$db"
 done
 curl -O ftp://ftp.ripe.net/ripe/stats/delegated-ripencc-latest
```

Optionally construct an asn-whitelist for your country, for example for `DE`:
```shell
cat delegated-ripencc-latest | \
  awk -F'|' '{if ($2=="DE" && $3=="asn") print "AS"$4}' \
  >asn-DE.txt
```

Call `ripe_import.py --help` or `ripe_diff.py --help`
to see all command line options.

Now import the data into your ContactDB, we assume you used `contactdb` as
database name.

You can use `ripe_diff.py` instead of `ripe_import.py` below
to get shown what would be imported into the database by the import step.

**Make sure the connection to the database is made
with sufficient rights! Use the database superuser when in doubt.**

The next step assumes you are currently in the same folder like the data you
downloaded.

```
cd $d
ripe_import.py --conninfo dbname=contactdb --asn-whitelist-file=asn-DE.txt -v
```

Here is a different example where the paths to the files is specified
explicitly:

```
ripe_import.py --conninfo "host=localhost user=intelmqadm dbname=contactdb" \
    --organisation-file=/tmp/ripe/ripe.db.organisation.gz \
    --role-file=/tmp/ripe/ripe.db.role.gz \
    --asn-file=/tmp/ripe/ripe.db.aut-num.gz \
    --verbose
```

Also see the
[documentation of the libpg conninfo string](https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING).
The [documentation on environment variables](https://www.postgresql.org/docs/current/static/libpq-envars.html) to the connection also
points towards how to savely provide a password with a ~/.pgpass file.

### use as a module
`check-ripe.py` is a simple example how to use the module
ripe_data independently of intelmq to write a simple check
that operates on ripe's dbsplit datafiles. Capabilities and limitations
are documented with ripe_data.py.
