* Install postgresql:
```
apt-get install postgresql-9.1 postgresql-server-dev-9.1  python-psycopg2
```

* Create a user for and database intelmq in Postgres:
```
sudo su - 
su - postgres
createuser intelmq -W
createdb -O intelmq intelmq
```

* Make sure that the local user intelmq can connect to the DB:
```
cat /etc/postgresql/9.1/main/pg_hba.conf
(...)
local   all             all                                     trust
(...)
```

* Restart PostgreSQL

* Run the script which will create the initial database tables:
```
cd /opt/intelmq/src/bots/outputs/postgresql/
psql -U intelmq intelmq < initdb.sql
```

* Update the corresponding 'bot_id' section in 'conf/bots.conf':

```
    [postgresql]
    host = <host>
    port = <port>
    database = intelmq
    user = intelmq
    password = <password>
```
