RIPE DB data import
==========================
A set of tools to manage imports of ripe data into to the contact database.

The following input files are required:

* ripe.db.organisation.gz
* ripe.db.role.gz
* ripe.db.aut-num.gz
* ripe.db.inetnum.gz
* ripe.db.inet6num.gz
* delegated-ripencc-latest (only for --restrict-to-country)

The Tools `ripe_import` and `ripe_diff` will be searching for these files
in the current working directory by default.

The files can be downloaded
from the RIPE website (ftp://ftp.ripe.net/ripe/dbase/split/).

It is also possible to provide a whitelist of ASNs to load. Use the
``--asn-whitelist-file`` parameter to pass a filename. The script expects one
AS entry per line, with the AS-prefix, e.g. ``AS123``.

Usage
=====

Download data to a directory using the script `ripe_download`.

Call `ripe_import.py --help` or `ripe_diff.py --help`
to see all command line options.

The importer is capable of importing only entries which can be associated to a
CountryCode. This is suppported natively for `inetnum` and `inetnum6` data
(IP-Data). For ASN an additional step is required, as the `autnum` datasets
(ASN-Data) do not provide this information. Thats where the `delegated-list`
comes to play. In order to import only IP and ASN Data for one country, for
instance DE, use the following parameters: `--restrict-to-country DE` and
`--ripe-delegated-file delegated-ripencc-latest`.

Note: When providing an asn-whitelist file, the file specified with
`--ripe-delegated-file` and CountryCode based imports will be ignored for
ASN-Data. Only the ASN specified in the whitelist will be imported. IP-Data
will not be affected.

Now import the data into your ContactDB, we assume you used `contactdb` as
database name.

You can use `ripe_diff.py` instead of `ripe_import.py` below
to get shown what would be imported into the database by the import step
and which manual entries are related to the affected ASNs or networks.

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
ripe_import.py --conninfo "host=localhost dbname=contactdb" \
    --organisation-file=/tmp/ripe/ripe.db.organisation.gz \
    --role-file=/tmp/ripe/ripe.db.role.gz \
    --asn-file=/tmp/ripe/ripe.db.aut-num.gz \
    --ripe-delegated-file=/tmp/ripe/delegated-ripencc-latest \
    --restrict-to-country DE \
    --verbose
```

Also see the
[documentation of the libpg conninfo string](https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING).
The [documentation on environment variables](https://www.postgresql.org/docs/current/static/libpq-envars.html) to the connection also
points towards how to savely provide a password with a ~/.pgpass file.

### use as a module
`check-ripe.py` is a simple example how to use the module
`ripe_data` independently of intelmq to write a simple check
that operates on ripe's dbsplit datafiles. Capabilities and limitations
are documented with `ripe_data.py`.
