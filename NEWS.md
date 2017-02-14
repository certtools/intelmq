NEWS
====

1.0
---

### Configuration
* For renamed bots, see the changelog for a complete list.
* Many bots have new/change parameters
* Syntax of runtime.conf has changed
* system.conf and startup.conf have been dropped entirely, use defaults.conf and runtime.conf instead


### Postgres databases
Use this statement to upgrade your database:
```SQL
ALTER TABLE events
   ADD COLUMN "classification.identifier" text,
   ADD COLUMN "feed.accuracy" text,
   ADD COLUMN "feed.documentation" text,
   ADD COLUMN "feed.provider" text,
   ADD COLUMN "protocol.transport" text,
   RENAME COLUMN "additional_information" TO "extra",
   RENAME COLUMN "misp_id" TO "misp.event_uuid",
   RENAME COLUMN "source.bgp_prefix" TO "source.network" text,
   RENAME COLUMN "source.cc" TO "source.cc" text,
   RENAME COLUMN "source.cc" TO "source.geolocation.cc" text,
   RENAME COLUMN "source.email_address" TO "source.account" text,
   RENAME COLUMN "source.reverse_domain_name" TO "source.reverse_dns" text,
   RENAME COLUMN "webshot_url" TO "screenshot_url" text,
   ALTER COLUMN "extra" SET DATA TYPE json,
   ALTER COLUMN "misp.evetn_uuid" SET DATA TYPE varchar(36),

UPDATE events
   SET "source.local_hostname"="destination.local_hostname",
       "destination.local_hostname"=DEFAULT
   WHERE "feed.name"='Open-LDAP' AND "source.local_hostname" IS NULL;
UPDATE events
   SET "extra"=json_build_object('os.name', "os.name", 'os.version', "os.version", 'user_agent', "user_agent")
   WHERE "os.name" IS NOT NULL AND "os.version" IS NOT NULL AND "user_agent" IS NOT NULL AND "extra" IS NULL;
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

ALTER TABLE events
   DROP COLUMN "os.name",
   DROP COLUMN "os.version",
   DROP COLUMN "user_agent",
```

Also note, that size constraints have changed!
