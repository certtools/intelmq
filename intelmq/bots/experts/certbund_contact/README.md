Expert bot to lookup contact information in a simple database
=============================================================

Requires psycopg and PostgreSQL


Database Setup
--------------

To create a PostgreSQL database for use with the expert bot, execute the
following commands as the user postgres from the top-level directory of
the IntelMQ source tree:

    su - postgres

    createdb contactdb
    psql -f intelmq/bots/experts/certbund_contact/initdb.sql   contactdb
    psql -f intelmq/bots/experts/certbund_contact/defaults.sql contactdb

    createuser intelmq
    psql -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO intelmq;" contactdb


The above commands assume that PostgreSQL is running an listening on the
default port. They create a database called "contactdb" in the default.
This matches the default configuration of the bot.
