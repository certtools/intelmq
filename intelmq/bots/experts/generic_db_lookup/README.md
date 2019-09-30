# Generic DB Lookup

This bot is capable for enriching intelmq events by lookups to a database.
Currently only PostgreSQL and SQLite are supported.

If more than one result is returned, a ValueError is raised.

## Parameters

### Connection

* `engine`: `postgresql` or `sqlite`
* `database`: string, defaults to "intelmq", database name or the SQLLite filename
* `table`: defaults to "contacts"

#### PostgreSQL specific
* `host`: string, defaults to "localhost"
* `password`: string
* `port`: integer, defaults to 5432
* `sslmode`: string, defaults to "require"
* `user`: defaults to "intelmq"

### Lookup and replace

* `lookup`: defauls

### Lookup

* `match_fields`: defaults to `{"source.asn": "asn"}`

The value is a key-value mapping an arbitrary number **intelmq** field names **to table** column names.
The values are compared with `=` only.

### Replace fields.

* `overwrite`: defaults to `false`. Is applied per field
* `replace_fields`: defaults to `{"contact": "source.abuse_contact"}`

`replace_fields` is again a key-value mapping an arbitrary number of **table** column names **to intelmq** field names 
