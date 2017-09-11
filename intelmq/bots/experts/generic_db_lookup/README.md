# Generic DB Lookup

This bot is capable for enriching intelmq events by lookups to a database.
Currently only postgres is supported.

If more than one result is returned, a ValueError is raised.

## Parameters

### Connection

* `database`: string, defaults to "intelmq"
* `host`: string, defaults to "localhost"
* `password`: string
* `port`: integer, defaults to 5432
* `sslmode`: string, defaults to "require"
* `table`: defaults to "contacts"
* `user`: defaults to "intelmq"

### Lookup

* `match_fields`: defaults to `{"source.asn": "asn"}`

The value is a key-value mapping an arbitrary number **intelmq** field names **to table** column names.
The values are compared with `=` only.

### Replace fields.

* `overwrite`: defaults to `false`. Is applied per field
* `replace_fields`: defaults to `{"contact": "source.abuse_contact"}`

`replace_fields` is again a key-value mapping an arbitrary number of **table** column names **to intelmq** field names 
