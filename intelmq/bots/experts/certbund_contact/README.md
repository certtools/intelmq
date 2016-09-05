# Expert bot to lookup contact information in a simple database

Requires Psycopg.

## Contact DB

### Database Setup

The following commands assume that PostgreSQL is running and listening on the
default port. They create a database called "contactdb" which matches the
default configuration of the bot.

```
    su - postgres

    createdb --encoding=UTF8 --template=template0 contactdb
    psql -f /usr/share/intelmq/certbund_contact/initdb.sql   contactdb
    psql -f /usr/share/intelmq/certbund_contact/defaults.sql contactdb
```

A database user with the right to select the data in the Contact DB
must be created.  This is the account, which will be used in the bot's
configuration for accessing the database.

```
    createuser intelmq --pwprompt
    psql -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO intelmq;" contactdb

```

### Adding New Contacts

Contacts can be added to the database directly using SQL.  These
manually configured contacts will take precedence over contacts which
were imported automatically, i.e. by `ripe_import.py`.

Connect to the database:

```
  su - postgres
  psql contactdb

```
Add a contact:

```pgsql

-- 1. Prepare contact information

  \set asn 3320
  -- unique name of the organization:
  \set org_name 'org1'
  \set org_comment 'Example comment on organization.'
  \set contact_email 'test@example.com'
  \set contact_comment 'Test comment on contact.'
  -- set the notification interval in seconds
  -- an interval of -1 means no notifications will be generated
  \set notification_interval 0

-- 2. Add new contact

  BEGIN TRANSACTION;
  INSERT INTO autonomous_system (number) VALUES (:asn);
  WITH new_org AS (
    INSERT INTO organisation (name,comment)
    VALUES (:'org_name',:'org_comment')
    RETURNING id
  ),
  new_contact AS (
    INSERT INTO contact (email,format_id,comment)
    VALUES (:'contact_email', 2, :'contact_comment')
    RETURNING id
  ),
  new_ota AS (
    INSERT INTO organisation_to_asn (organisation_id,asn_id,notification_interval)
    VALUES (
      (SELECT id from new_org), :asn, :notification_interval
    )
  )
  INSERT INTO role (organisation_id,contact_id) VALUES (
      (SELECT id from new_org),
      (SELECT id from new_contact)
    )
  ;
  COMMIT TRANSACTION;

```

## Suppress notification of contacts based upon certain criteria:

It ist possible to suppress the notification of contacts based upon certain
criteria. Such can be: AS-number, IP address or network (CIDR-notation),
classification type and classification identifier.

The rules for this suppression are stored in the `inhibition` table.

To add new rules to the inhibition-table, simply run the script `add_inhibiton`.
Please see `add_inhibition.py --help` for a list of available commands.

The criteria within a rule are "linked" with a "and-operation".

**Examples**:

Suppose you have inserted a rule for `AS123456` and a
Classification-Type `malware` and a classification.identifier `botnet-drone`.
The contact of the event:

```
{
    "source.as": "as123456",
    "classification.type": "malware",
    "classification.identifier": "botnet-drone"
}
```
Would not be notified, wheras the same contact would be notified, if the event
is:
```
{
    "source.as": "as123456",
    "classification.type": "malware",
    "classification.identifier": "zeus"
}
```


Suppose you have inserted a rule for `AS123456` and a
Classification-Type `c&c` and no classification.identifier.

For both events, no notification would be created, as the rule matches:
```
{
    "source.as": "as123456",
    "classification.type": "c&c",
    "classification.identifier": "myC&C"
}

{
    "source.as": "as123456",
    "classification.type": "malware",
    "classification.identifier": "AnotherIdentifier"
}
```



# Generating a graphic which visualizes the schema of the ContactDB

You can use `postgresql-autodoc` to do this. PG autodoc is available on both
debian and ubuntu via apt.
