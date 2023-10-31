<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

# SQLite

Similarly to PostgreSQL, you can use `intelmq_psql_initdb` to create initial SQL statements from `harmonization.conf`.
The script will create the required table layout and save it as `/tmp/initdb.sql`.

Create the new database (you can ignore all errors since SQLite doesn't know all SQL features generated for PostgreSQL):

```bash
sqlite3 your-db.db
sqlite> .read /tmp/initdb.sql
```

Then, set the `database` parameter to the `your-db.db` file path.

To output data to SQLite use SQL Output Bot with parameter `engine` set to `sqlite`. For more information see SQL Output Bot documentation page.