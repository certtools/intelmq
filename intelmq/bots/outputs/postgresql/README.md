* Install PostgreSQL, at least version 9.4 is recommended.

```bash
> apt-get install postgresql-9.4 python-psycopg2 postgresql-server-dev-9.4
```

* Create a User and Database:

```shell
> su - postgres
> createuser intelmq -W
  Shall the new role be a superuser? (y/n) n
  Shall the new role be allowed to create databases? (y/n) y
  Shall the new role be allowed to create more new roles? (y/n) n
  Password: 

> createdb -O intelmq --encoding='utf-8' intelmq-events
```

* Depending on your setup adjust `/etc/postgresql/9.4/main/pg_hba.conf` to allow network connections for the intelmq user.

* Restart PostgreSQL.

* Generate `initdb.sql` by using the [psql_initdb_generator.py](https://github.com/certtools/intelmq/blob/master/intelmq/bin/intelmq_psql_initdb.py) tool which extracts all field names and data types from `Data-Harmonization.md`.

* Create the `events` table:

```bash
> psql < /tmp/initdb.sql # as intelmq user
> psql -U intelmq intelmq-events -W < /tmp/initdb.sql # as other user
```
