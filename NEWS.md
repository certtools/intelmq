NEWS
====

See the changelog for a full list of changes.

1.1.0
-----
### Tools
- `intelmqctl start` prints bot's error messages in stderr if it failed to start.
- `intelmqctl check` checks if all keys in the packaged defaults.conf are present in the current configuration.

### Harmonization
- added `destination.urlpath` and `source.urlpath` to harmonization.

### Configuration
A new harmonization type `JSONDict` has been added specifically for the `extra` field. It is highly recommended to change the type of this field.
The feed names in the shadowserver parser have been adapted to the current subjects. Change your configuration accordingly:
* `Botnet-Drone-Hadoop` to `Drone`
* `DNS-open-resolvers` to `DNS-Open-Resolvers`
* `Open-NetBIOS` to `Open-NetBIOS-Nameservice`
* `Ssl-Freak-Scan` to `SSL-FREAK-Vulnerable-Servers`
* `Ssl-Scan` to `SSL-POODLE-Vulnerable-Servers`

The Maxmind GeoIP expert did previously always overwrite existing data. A new parameter `overwrite` has been added,
which is by default set to `false` to be consistent with other bots.

The bot `bots.collectors.n6.collector_stomp` has been renamed to the new module `bots.collectors.stomp.collector`. Adapt your `runtime.conf` accordingly.

### Postgres databases
The following statements optionally update existing data.
Please check if you did use these feed names and eventually adapt them for your setup!
```SQL
ALTER TABLE events
   ADD COLUMN "destination.urlpath" text,
   ADD COLUMN "source.urlpath" text;
UPDATE events
   SET "classification.identifier" = 'openmdns'
   WHERE "classification.identifier" = 'open-mdns' AND "feed.name" = 'Open-mDNS';
UPDATE events
   SET "classification.identifier" = 'openchargen'
   WHERE "classification.identifier" = 'open-chargen' AND "feed.name" = 'Open-Chargen';
UPDATE events
   SET "classification.identifier" = 'opentftp'
   WHERE "classification.identifier" = 'open-tftp' AND "feed.name" = 'Open-TFTP';
UPDATE events
   SET "classification.identifier" = 'botnet'
   WHERE "classification.identifier" = 'infected system' AND "feed.name" = 'Sinkhole-HTTP-Drone';
UPDATE events
   SET "classification.identifier" = 'botnet'
   WHERE "classification.identifier" = 'infected system' AND "feed.name" = 'Microsoft-Sinkhole';
UPDATE events
   SET "classification.identifier" = 'openredis'
   WHERE "classification.identifier" = 'open-redis' AND "feed.name" = 'Open-Redis';
UPDATE events
   SET "classification.identifier" = 'open-portmapper',
       "protocol.application" = 'portmap'
   WHERE "classification.identifier" = 'openportmapper' AND "feed.name" = 'Open-Portmapper' AND "protocol.application" = 'portmapper';
UPDATE events
   SET "classification.identifier" = 'open-ipmi'
   WHERE "classification.identifier" = 'openipmi' AND "feed.name" = 'Open-IPMI';
UPDATE events
   SET "classification.identifier" = 'open-qotd'
   WHERE "classification.identifier" = 'openqotd' AND "feed.name" = 'Open-QOTD';
UPDATE events
   SET "classification.identifier" = 'open-snmp'
   WHERE "classification.identifier" = 'opensnmp' AND "feed.name" = 'Open-SNMP';
UPDATE events
   SET "classification.identifier" = 'open-mssql'
   WHERE "classification.identifier" = 'openmssql' AND "feed.name" = 'Open-MSSQL';
UPDATE events
   SET "classification.identifier" = 'open-mongodb'
   WHERE "classification.identifier" = 'openmongodb' AND "feed.name" = 'Open-MongoDB';
UPDATE events
   SET "classification.identifier" = 'open-netbios', "feed.name" = 'Open-NetBIOS-Nameservice'
   WHERE "classification.identifier" = 'opennetbios' AND "feed.name" = 'Open-NetBIOS';
UPDATE events
   SET "classification.identifier" = 'openelasticsearch'
   WHERE "classification.identifier" = 'open-elasticsearch' AND "feed.name" = 'Open-Elasticsearch';
UPDATE events
   SET "classification.identifier" = 'dns-open-resolver', "feed.name" = 'DNS-Open-Resolvers'
   WHERE "classification.identifier" = 'opendns' AND "feed.name" = 'DNS-open-resolvers';
UPDATE events
   SET "classification.identifier" = 'ntp-monitor'
   WHERE "classification.identifier" = 'openntp' AND "feed.name" = 'NTP-Monitor';
UPDATE events
   SET "classification.identifier" = 'SSL-POODLE', "feed.name" = 'SSL-POODLE-Vulnerable-Servers'
   WHERE "classification.identifier" = 'SSL-Poodle' AND "feed.name" = 'SSL-Scan';
UPDATE events
   SET "feed.name" = 'SSL-FREAK-Vulnerable-Servers'
   WHERE "feed.name" = 'SSL-Freak-Scan';
UPDATE events
   SET "classification.identifier" = 'open-memcached'
   WHERE "classification.identifier" = 'openmemcached' AND "feed.name" = 'Open-Memcached';
UPDATE events
   SET "classification.identifier" = 'infected system', "feed.name" = 'Drone'
   WHERE "classification.identifier" = 'botnet' AND "feed.name" = 'Botnet-Drone-Hadoop';
UPDATE events
   SET "classification.identifier" = 'open-xdmcp'
   WHERE "classification.identifier" = 'openxdmcp' AND "feed.name" = 'Open-XDMCP';
UPDATE events
   SET "classification.identifier" = 'open-natpmp', "protocol.application" = 'natpmp'
   WHERE "classification.identifier" = 'opennatpmp' AND "feed.name" = 'Open-NATPMP' AND "protocol.application" = 'nat-pmp';
UPDATE events
   SET "classification.identifier" = 'open-netis'
   WHERE "classification.identifier" = 'opennetis' AND "feed.name" = 'Open-Netis';
UPDATE events
   SET "classification.identifier" = 'ntp-version'
   WHERE "classification.identifier" = 'openntpversion' AND "feed.name" = 'NTP-Version';
UPDATE events
   SET "classification.identifier" = 'sandbox-url'
   WHERE "classification.identifier" = 'sandboxurl' AND "feed.name" = 'Sandbox-URL';
UPDATE events
   SET "classification.identifier" = 'spam-url'
   WHERE "classification.identifier" = 'spamurl' AND "feed.name" = 'Spam-URL';
UPDATE events
   SET "classification.identifier" = 'open-ike'
   WHERE "classification.identifier" = 'openike' AND "feed.name" = 'Vulnerable-ISAKMP';
UPDATE events
   SET "classification.identifier" = 'open-rdp'
   WHERE "classification.identifier" = 'openrdp' AND "feed.name" = 'Accessible-RDP';
UPDATE events
   SET "classification.identifier" = 'open-ldap'
   WHERE "classification.identifier" = 'openldap' AND "feed.name" = 'Open-LDAP';
UPDATE events
   SET "classification.identifier" = 'blacklisted-ip'
   WHERE "classification.identifier" = 'blacklisted' AND "feed.name" = 'Blacklisted-IP';
UPDATE events
   SET "classification.identifier" = 'open-telnet'
   WHERE "classification.identifier" = 'opentelnet' AND "feed.name" = 'Accessible-Telnet';
UPDATE events
   SET "classification.identifier" = 'open-cwmp'
   WHERE "classification.identifier" = 'opencwmp' AND "feed.name" = 'Accessbile-CWMP';
UPDATE events
   SET "classification.identifier" = 'accessible-vnc'
   WHERE "classification.identifier" = 'accessiblevnc' AND "feed.name" = 'Accessible-VNC';
```

1.0.3 Bugfix release (unreleased)
---------------------------------

### Configuration
- `bots.parsers.cleanmx` removed CSV format support and now only supports XML format. Therefore, CleanMX collectors must define the `http_url` parameter with the feed url which points to XML format. See Feeds.md file on documentation section to get the correct URLs. Also, downloading the data from CleanMX feed can take a while, therefore, CleanMX collectors must overwrite the `http_timeout_sec` parameter with the value `120`.
- The classification mappings for the n6 parser have been corrected:

| n6 classification | Previous classification |  |  | Current classification |  |  | Notes |
|-|-|-|-|-|-|-|-|
|                   | taxonomy   | type   | identifier | taxonomy       | type    | identifier |
| dns-query         | Other      | other  | ignore me  | Other          | other   | dns-query  |
| proxy             | Vulnerable | proxy  | open proxy | Other          | proxy   | openproxy  |
| sandbox-url       | ignore     | ignore | ignore me  | malicious code | malware | sandboxurl | As this previous taxonomy did not exist, these events have been rejected |
| other             | Vulnerable | unknow | unknown    | Other          | other   | other      |

### Postgres databases
Use the following statement carefully to upgrade your database.
Adapt your feedname in the query to the one used in your setup.
```SQL
UPDATE events
   SET "classification.identifier" = "dns-query"
   WHERE "feed.name" = 'n6' AND "classification.taxonomy" = "Other" AND "classification.type" = "other" AND "classification.identifier" = "ignore me";
UPDATE events
   SET "classification.taxonomy" = "malicious code" AND "classification.type" = "malware" AND "classification.identifier" = "sandboxurl"
   WHERE "feed.name" = 'n6' AND "classification.taxonomy" = "Vulnerable" AND "classification.type" = "ignore" AND "classification.identifier" = "ignore me";
UPDATE events
   SET "classification.taxonomy" = "Other" AND "classification.type" = "other" AND "classification.identifier" = "other"
   WHERE "feed.name" = 'n6' AND "classification.taxonomy" = "Vulnerable" AND "classification.type" = "unknow" AND "classification.identifier" = "unknow";
```

1.0.2 Bugfix release
--------------------
No changes needed.

1.0.1 Bugfix release
--------------------
No changes needed.

1.0.0 Stable release
--------------------
### Configuration
- `bots.experts.ripencc_abuse_contact` now has the two additional parameters `query_ripe_stat_asn` and `query_ripe_stat_ip` instead of `query_ripe_stat`. The old parameter will be supported until version 1.1. An additional parameter `mode` has been introduced. See the bot's documentation for more details: docs/Bots.md#ripencc-abuse-contact
- `bots.experts.certat_contact` has been renamed to `bots.experts.national_cert_contact_certat` (#995)
- `bots.collectors.ftp` has been dropped (unused, unmaintained, #842)
- system.conf and startup.conf have been dropped entirely, use defaults.conf and runtime.conf instead
* Many bots have new/changed parameters
* Many bots have been renamed/moved or deleted. Please read the Bots section in the changelog and upgrade your configuration accordingly.

1.0.0.dev8
----------
### Configuration
- `http_timeout` has been renamed to `http_timeout_sec` and `http_timeout_max_tries` has been added.

### Configuration
Two new fields have been added to `defaults.conf` which are expected by the bots:
- `"log_processed_messages_count": 500` and
- `'log_processed_messages_seconds": 900`
Configure them in your setup and optionally adapt the values to your needs.

### Postgres databases
Use the following statement carefully to upgrade your database.
```SQL
ALTER TABLE events
   ADD COLUMN "output" json
```

1.0.0.dev7
----------

### Configuration
* The deduplicator expert requires a new parameter `filter_type`, the old previous default was `blacklist`. The key `ignore_keys` has been renamed to `filter_keys`.
* The tor_nodes expert has a new parameter `overwrite`, which is by default `false`.
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

### Libraries
The built-in Alienvault OTX API library has been removed, install the library from github instead. See the [README.md](intelmq/bots/collectors/alienvault_otx/README.md) for details.

### Postgres databases
Use the following statement carefully to upgrade your database.
Take care that no data will be lost, the statement may not be complete!

Also note that size constraints have changed!
```SQL
ALTER TABLE events
   ADD COLUMN "feed.documentation" text;

UPDATE events
   SET "source.local_hostname"="destination.local_hostname",
       "destination.local_hostname"=DEFAULT
   WHERE "feed.name"='Open-LDAP' AND "source.local_hostname" IS NULL;
UPDATE  events
   SET "feed.url" = substring("feed.url" from 1 for 37)
   WHERE SUBSTRING("feed.url" from 1 for 38) = 'https://prod.cyberfeed.net/stream?key='
UPDATE events
   SET "feed.url" = regexp_replace("feed.url", 'receipt=([^&])*', '')
   WHERE substring("feed.url" from 1 for 43) = 'https://lists.malwarepatrol.net/cgi/getfile'
UPDATE events
   SET "feed.url" = substring("feed.url" from 1 for 36)
   WHERE SUBSTRING("feed.url" from 1 for 37) = 'https://data.phishtank.com/data/'
UPDATE events
   SET "classification.taxonomy" = lower("classification.taxonomy")
   WHERE "classification.taxonomy" IS NOT NULL;
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

Syntax of runtime.conf has changed

### Postgres databases
```sql
ALTER TABLE events
   ADD COLUMN "misp.attribute_uuid" varchar(36),
   ADD COLUMN "malware.hash.sha256" text,
   ALTER COLUMN "misp.event_uuid" SET DATA TYPE varchar(36);

ALTER TABLE events   RENAME COLUMN "misp_uuid" TO "misp.event_uuid";

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
   SET "malware.hash.md5" = lower("malware.hash.md5");
UPDATE events
   SET "malware.hash.sha1" = lower("malware.hash.sha1");
UPDATE events
   SET "malware.hash.sha256" = lower("malware.hash.sha256");
UPDATE events
   SET "malware.hash.md5" = lower(substring("malware.hash" from 4))
   WHERE substring("malware.hash" from 1 for 3) = '$1$';
UPDATE events
   SET "malware.hash.sha1" = lower(substring("malware.hash" from 7))
   WHERE substring("malware.hash" from 1 for 6) = '$sha1$';
UPDATE events
   SET "malware.hash.sha256" = lower(substring("malware.hash" from 4))
   WHERE substring("malware.hash" from 1 for 3) = '$5$';
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
   ADD COLUMN "classification.identifier" text,
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
   DROP COLUMN "user_agent",
   DROP COLUMN "malware.hash";
```
