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

    createuser intelmq --pwprompt
    psql -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO intelmq;" contactdb

```

### Adding New Contacts

The database is configured directly using SQL.

Connect to the database:

```

  su - postgres
  psql contactdb

```

```pgsql

-- 1. Prepare contact information

  \set asn 3320
  -- unique name of the organization:
  \set org_name 'org1'
  \set org_comment 'Test comment'
  \set contact_email 'test@example.com'
  -- set format to feed_spefic (ID 2 as per the setup with defaults.sql above):
  \set contact_format_id 2
  \set contact_comment 'Test contact'
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
    VALUES (:'contact_email', :contact_format_id, :'contact_comment')
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
