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
createuser --encrypted --pwprompt intelmq
```

Create the new database:
```
createdb --owner=intelmq intelmq-events
```

Now initialise it as database-user `intelmq` (should ask for the password):
```
psql -h localhost intelmq-events intelmq </tmp/initdb.sql
```
