
# How to install:

Use `intelmq/bin/intelmq_psql_initdb.py` to create initial sql-statements from Harmonization.conf
the script will create the required table layout and save it as /tmp/initdb.sql

Now create a database-user and a database:

```
# su - postgres
$ createuser intelmq
$ createdb -O intelmq intelmq-events
$ psql -c "ALTER ROLE intelmq PASSWORD '**************';"
$ exit
# su - intelmq
$ psql intelmq-events </tmp/initdb.sql
```
