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
   ADD COLUMN "feed.documentation" text
   ADD COLUMN "feed.provider" text;
UPDATE events
   SET "source.local_hostname"="destination.local_hostname",
       "destination.local_hostname"=DEFAULT
   WHERE "feed.name"='Open-LDAP' AND "source.local_hostname" IS NULL;
```
