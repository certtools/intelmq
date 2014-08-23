* Install postgresql:
```
apt-get install postgresql-9.1 python-psycopg2
```

* Create a User and Database:
```
sudo su - 
su - postgres
createuser intelmq -W
createdb -O intelmq --encoding='utf-8' intelmq-events;
```

* Allow Local User Connect to the Database:
```
cat /etc/postgresql/9.1/main/pg_hba.conf
(...)
local   all             all                                     trust
(...)
```

* Restart PostgreSQL

* Create Database Table:

Run the tool [psql-initdb-generator.py](https://github.com/certtools/intelmq/blob/master/intelmq/bots/outputs/postgresql/psql-initdb-generator.py) to get the initdb.sql file updated. After that, run the following command to create the table.
```
psql -U intelmq intelmq-events < /tmp/initdb.sql
```
