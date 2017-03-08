NEWS
====

See the changelog for a full list of changes.

### Configuration
* For renamed bots, see the changelog for a complete list.
* Many bots have new/change parameters
* Syntax of runtime.conf has changed
* system.conf and startup.conf have been dropped entirely, use defaults.conf and runtime.conf instead
* Many bots have been renamed/moved or deleted. Please read the Bots section in the changelog and upgrade your configuration accordingly.

1.0.0.dev7 (in developement)
----------------------------

### Configuration
* The deduplicator expert requires a new parameter `filter_type`, the old previous default was `blacklist`. The key `ignore_keys` has been renamed to `filter_keys`.
* The configuration format of the modify expert has been change to a list-based syntax.
  Old format:

      {
      "Blocklist.de": {
          "__default": [{
                  "feed.name": "^BlockList\\.de$",
                  "classification.identifier": ""
              }, {
              }]
          },
		  ...
      }

  new format:

      [
          {
              "rulename": "Blocklist.de __default",
              "if": {
                  "classification.identifier": "",
                  "feed.name": "^BlockList\\.de$"
              },
              "then": {}
          },
		  ...
      ]

### Postgres databases
Use the following statement carefully to upgrade your database.
Take care that no data will be lost, the statement may not be complete!

Also note that size constraints have changed!
```SQL
ALTER TABLE events
   ADD COLUMN "feed.documentation" text

UPDATE events
   SET "source.local_hostname"="destination.local_hostname",
       "destination.local_hostname"=DEFAULT
   WHERE "feed.name"='Open-LDAP' AND "source.local_hostname" IS NULL;
```

1.0.0.dev6
----------

### Postgres databases
```sql
ALTER TABLE events
   ADD COLUMN "feed.provider" text
```

1.0.0.dev5
----------

### Postgres databases
```sql
ALTER TABLE events
   ADD COL   ADD COLUMN "msip.attribute_uuid" varchar(36),
   ALTER COLUMN "misp.event_uuid" SET DATA TYPE varchar(36).
   RENAME COLUMN "misp_uuid" TO "misp.event_uuid";

UPDATE events
   SET "protocol.application" = lower("protocol.application")
   WHERE "protocol.application" IS NOT NULL;
UPDATE events
   SET "source.abuse_contact" = lower("source.abuse_contact")
   WHERE "source.abuse_contact" IS NOT NULL;
UPDATE events
   SET "destination.abuse_contact" = lower("destination.abuse_contact")
   WHERE "destination.abuse_contact" IS NOT NULL;
UPDATE events
   SET "event_hash" = lower("event_hash")
   WHERE "event_hash" IS NOT NULL;
UPDATE events
   SET "malware.hash" = lower("malware.hash")
   WHERE "malware.hash" IS NOT NULL;
UPDATE events
   SET "malware.hash.md5" = lower("malware.hash.md5")
   WHERE "malware.hash.md5" IS NOT NULL;
UPDATE events
   SET "malware.hash.sha1" = lower("malware.hash.sha1")
   WHERE "malware.hash.sha1" IS NOT NULL;
```

1.0.0.dev1
----------

### Postgres databases

```sql
ALTER TABLE events
   ADD CO   ADD COLUMN "classification.identifier" text,
   ADD COLUMN "feed.accuracy" text,
   ADD COLUMN "feed.code" text,
   ADD COLUMN "malware.hash.md5" text,
   ADD COLUMN "malware.hash.sha1" text,
   ADD COLUMN "protocol.transport" text,
   ALTER COLUMN "extra" SET DATA TYPE json,
   RENAME COLUMN "additional_information" TO "extra",
   RENAME COLUMN "description.target" TO "event_description.target",
   RENAME COLUMN "description.text" TO "event_description.text",
   RENAME COLUMN "destination.bgp_prefix" TO "destination.network" text,
   RENAME COLUMN "destination.cc" TO "destination.geolocation.cc" text,
   RENAME COLUMN "destination.email_address" TO "destination.account" text,
   RENAME COLUMN "destination.reverse_domain_name" TO "destination.reverse_dns" text,
   RENAME COLUMN "misp_id" TO "misp_uuid",
   RENAME COLUMN "source.bgp_prefix" TO "source.network" text,
   RENAME COLUMN "source.cc" TO "source.geolocation.cc" text,
   RENAME COLUMN "source.email_address" TO "source.account" text,
   RENAME COLUMN "source.reverse_domain_name" TO "source.reverse_dns" text,
   RENAME COLUMN "webshot_url" TO "screenshot_url" text;

UPDATE events
   SET "extra"=json_build_object('os.name', "os.name", 'os.version', "os.version", 'user_agent', "user_agent")
   WHERE "os.name" IS NOT NULL AND "os.version" IS NOT NULL AND "user_agent" IS NOT NULL AND "extra" IS NULL;

ALTER TABLE events
   DROP COLUMN "os.name",
   DROP COLUMN "os.version",
   DROP COLUMN "user_agent";
```
