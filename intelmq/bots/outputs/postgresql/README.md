You have two basic choices to run PostgreSQL:
1. on the same machine as intelmq, then you could use unix-sockets if available on your platform
2. on a different machine. In which case you would need to use a TCP connection and make sure you give the right connection parameters to each psql or client call.

Make sure to consult your PostgreSQL documentation 
about how to allow network connections and authentication in case 2.


# PostgreSQL Version
Any supported version of PostgreSQL should work 
(v>=9.2 as of Oct 2016)[[1](https://www.postgresql.org/support/versioning/)].

If you use PostgreSQL server v >= 9.4, it gives you the possibility 
to use the time-zone [formatting string](https://www.postgresql.org/docs/9.4/static/functions-formatting.html) "OF" for date-times 
and the [GiST index for the cidr type](https://www.postgresql.org/docs/9.4/static/release-9-4.html#AEN120769). This may be useful depending on how 
you plan to use the events that this bot writes into the database.

# How to install:

Use `intelmq_psql_initdb` to create initial sql-statements
from Harmonization.conf. The script will create the required table layout
and save it as /tmp/initdb.sql

You need a postgresql database-user to own the result database.
The recommendation is to use the name `intelmq`.
There may already be such a user for the postgresql database-cluster
to be used by other bots. (For example from setting up
the expert/certbund_contact bot.)

Therefore if still necessary: create the database-user
as postgresql superuser, which usually is done via the system user `postgres`:
```
createuser --no-superuser --no-createrole --no-createdb --encrypted --pwprompt intelmq
```

Create the new database:
```
createdb --encoding='utf-8' --owner=intelmq intelmq-events
```

(The encoding parameter should ensure the right encoding on platform
where this is not the default.)

Now initialize it as database-user `intelmq` (in this example
a network connection to localhost is used, so you would get to test
if the user `intelmq` can authenticate):
```
psql -h localhost intelmq-events intelmq </tmp/initdb.sql
```
