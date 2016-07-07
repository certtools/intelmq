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

    createuser intelmq
    psql -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO intelmq;" contactdb

```

### Configuration

The database is configured directly using SQL.

Connect to the database:

```

  su - postgres
  psql contactdb

```

#### Expected classification types

FIXME: For each classifcation type name that will come along
in the intelmq you need to have an entry 
in the table ```classification_type```.

For example create them like this
```
COPY classification_type (name) FROM stdin;
botnet drone
spam
malware
ransomware
malware configuration
c&c
scanner
exploit
brute-force
ids alert
defacement
compromised
backdoor
ddos
dropzone
phishing
vulnerable service
blacklist
other
unknown
\.
```


#### Configure Templates

```

-- Configure templates
  BEGIN TRANSACTION;
  WITH new_classification_type AS (
    INSERT INTO classification_type (name) VALUES ('botnet drone')
    RETURNING id
  ),
  new_template AS (
    INSERT INTO template (path,classification_type_id)
    VALUES ('/usr/local/lib/intelmq/mailgen/templates/test01',
      (SELECT id from new_classification_type))
    RETURNING *
  )
  select * from new_template;
  COMMIT TRANSACTION;

```

#### Add New Contacts

```pgsql

-- 1. Choose a template

  SELECT * FROM template;

  -- use its ID to set it for the new contact
  \set template_id 1

-- 2. Prepare contact information

  \set asn 3320
  \set org_name 'org1' -- unique name of the organization
  \set org_comment 'Test comment'
  \set contact_email 'test@example.com'
  \set contact_format_id 1 -- CSV
  \set contact_comment 'Test contact'
  \set notification_interval 0

-- 3. Add new contact
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
  ),
  new_ott AS (
    INSERT INTO organisation_to_template (organisation_id,template_id)
    VALUES (
      (SELECT id from new_org),
      (SELECT id FROM template WHERE id = :template_id)
    )
  )
  INSERT INTO role (organisation_id,contact_id) VALUES (
      (SELECT id from new_org),
      (SELECT id from new_contact)
    )
  ;
  COMMIT TRANSACTION;

```

