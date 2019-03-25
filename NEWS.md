NEWS
====

See the changelog for a full list of changes.

1.1.2 Bugfix release (2019-03-25)
---------------------------------

### Configuration
#### Feodotracker
 * The URL of the "Feodo Tracker IPs" feed has changed. The new one is `https://feodotracker.abuse.ch/downloads/ipblocklist.csv`. If you are using this feed, adapt your configuration accordingly. The parser has been updated to support the new format.
 * The feed "Feodo Tracker Domains" has been discontinued.

1.1.1 Bugfix release (2019-01-15)
---------------------------------

### Configuration
In 1.1.0 the default value for the parameter `error_dump_message` was set to `false`. The recommended value, used in previous and future release is `true` to not loose any data in case of errors. Users are advised to check the values configured in their `defaults.conf` file.

### Postgres databases
The following statements optionally update existing data.
Please check if you did use these feed names and eventually adapt them for your setup!
```SQL
UPDATE events
   SET "classification.taxonomy" = 'abusive content', "classification.type" = 'spam', "classification.identifier" = 'spam', "malware.name" = NULL, "source.fqdn" = "source.reverse_dns", "source.reverse_dns" = NULL, "source.url" = "destination.url", "destination.url" = NULL
   WHERE "malware.name" = 'spam' AND "feed.name" = 'Drone';
```

In the section for 1.1.0 there was this command:
```
UPDATE events
   SET "classification.identifier" = 'open-portmapper',
       "protocol.application" = 'portmap'
   WHERE "classification.identifier" = 'openportmapper' AND "feed.name" = 'Open-Portmapper' AND "protocol.application" = 'portmapper';
```
`protocol.application` was incorrect. To fix it you can use:
```
UPDATE events
   SET "protocol.application" = 'portmapper'
   WHERE "classification.identifier" = 'open-portmapper' AND "feed.name" = 'Open-Portmapper' AND "protocol.application" = 'portmap';
```

### MongoDB databases
In previous version the MongoDB Output Bot saved the fields `time.observation` and `time.source` as strings in ISO format. But MongoDB does support saving datetime objects directly which are converted to its native date format, enabling certain optimizations and features. The MongoDB Output Bot now saves these values as datetime objects.

1.1.0 Feature release (2018-09-05)
----------------------------------
### Requirements
- Python 3.4 or newer is required.

### Tools
- `intelmqctl start` prints bot's error messages in stderr if it failed to start.
- `intelmqctl check` checks if all keys in the packaged defaults.conf are present in the current configuration.

### Contrib / Modify Expert
The malware name rules of the modify expert have been migrated to the [Malware Name Mapping repository](https://github.com/certtools/malware_name_mapping).
See `contrib/malware_name_mapping/` for download and conversion scripts as well as documentation.

### Shadowserver Parser
The classification type for malware has been changed from "botnet drone" to the more generic "infected system".
The classification identifiers have been harmonized too:

| old identifier | new identifier |
|-|-|
| openmdns | open-mdns |
| openchargen | open-chargen |
| opentftp | open-tftp |
| openredis | open-redis |
| openportmapper | open-portmapper |
| openipmi | open-ipmi |
| openqotd | open-qotd |
| openssdp | open-ssdp |
| opensnmp | open-snmp |
| openmssql | open-mssql |
| openmongodb | open-mongodb |
| opennetbios | open-netbios-nameservice |
| openelasticsearch | open-elasticsearch |
| opendns | dns-open-resolver |
| openntp | ntp-monitor |
| SSL-FREAK | ssl-freak |
| SSL-Poodle | ssl-poodle |
| openmemcached | open-memcached |
| openxdmcp | open-xdmcp |
| opennatpmp | open-natpmp |
| opennetis | open-netis |
| openntpversion | ntp-version |
| sandboxurl | sandbox-url |
| spamurl | spam-url |
| openike | open-ike |
| openrdp | open-rdp |
| opensmb | open-smb |
| openldap | open-ldap |
| blacklisted | blacklisted-ip |
| opentelnet | open-telnet |
| opencwmp | open-cwmp |
| accessiblevnc | open-vnc |

In the section Postgres databases you can find SQL statements for these changes.

Some feed names have changed, see the comment below in the section Configuration.

### Harmonization
You may want to update your harmonization configuration
- Newly added fields:
  - `destination.urlpath` and `source.urlpath`.
  - `destination.domain_suffix` and `source.domain_suffix`.
  - `tlp` with a new type TLP.
- Changed fields:
  - ASN fields now have a new type `ASN`.
- Classification:
  - New value for `classification.type`: `vulnerable client` with taxonomy `vulnerable`.
  - New value for `classification.type`: `infected system` with taxonomy `malicious code` as replacement for `botnet drone`.
- Renamed `JSON` to `JSONDict` and added a new type `JSON`. `JSONDict` saves data internally as JSON, but acts like a dictionary. `JSON` accepts any valid JSON.

Some bots depend on the three new harmonization fields.

### Configuration
A new harmonization type `JSONDict` has been added specifically for the `extra` field. It is highly recommended to change the type of this field. The change is backwards compatibile and the change is not yet necessary, IntelMQ 1.x.x works with the old configuration too.

The feed names in the shadowserver parser have been adapted to the current subjects. Old subjects will still work in IntelMQ 1.x.x. Change your configuration accordingly:
* `Botnet-Drone-Hadoop` to `Drone`
* `DNS-open-resolvers` to `DNS-Open-Resolvers`
* `Open-NetBIOS` to `Open-NetBIOS-Nameservice`
* `Ssl-Freak-Scan` to `SSL-FREAK-Vulnerable-Servers`
* `Ssl-Scan` to `SSL-POODLE-Vulnerable-Servers`

The Maxmind GeoIP expert did previously always overwrite existing data. A new parameter `overwrite` has been added,
which is by default set to `false` to be consistent with other bots.

The bot `bots.collectors.n6.collector_stomp` has been renamed to the new module `bots.collectors.stomp.collector`. Adapt your `runtime.conf` accordingly.

The parameter `feed` for collectors has been renamed to `name`, as it results in `feed.name`. Backwards compatibility is ensured until 2.0.

### Postgres databases
The following statements optionally update existing data.
Please check if you did use these feed names and eventually adapt them for your setup!
```SQL
ALTER TABLE events
   ADD COLUMN "destination.urlpath" text,
   ADD COLUMN "source.urlpath" text;
ALTER TABLE events
   ADD COLUMN "destination.domain_suffix" text,
   ADD COLUMN "source.domain_suffix" text;
ALTER TABLE events
   ADD COLUMN "tlp" text;
UPDATE events
   SET "classification.type" = 'infected system'
   WHERE "classification.type" = 'botnet drone';
UPDATE events
   SET "classification.identifier" = 'open-mdns'
   WHERE "classification.identifier" = 'openmdns' AND "feed.name" = 'Open-mDNS';
UPDATE events
   SET "classification.identifier" = 'open-chargen'
   WHERE "classification.identifier" = 'openchargen' AND "feed.name" = 'Open-Chargen';
UPDATE events
   SET "classification.identifier" = 'open-tftp'
   WHERE "classification.identifier" = 'opentftp' AND "feed.name" = 'Open-TFTP';
UPDATE events
   SET "classification.identifier" = 'open-redis'
   WHERE "classification.identifier" = 'openredis' AND "feed.name" = 'Open-Redis';
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
   SET "classification.identifier" = 'open-netbios-nameservice', "feed.name" = 'Open-NetBIOS-Nameservice'
   WHERE "classification.identifier" = 'opennetbios' AND "feed.name" = 'Open-NetBIOS';
UPDATE events
   SET "classification.identifier" = 'open-elasticsearch'
   WHERE "classification.identifier" = 'openelasticsearch' AND "feed.name" = 'Open-Elasticsearch';
UPDATE events
   SET "classification.identifier" = 'dns-open-resolver', "feed.name" = 'DNS-Open-Resolvers'
   WHERE "classification.identifier" = 'opendns' AND "feed.name" = 'DNS-open-resolvers';
UPDATE events
   SET "classification.identifier" = 'ntp-monitor'
   WHERE "classification.identifier" = 'openntp' AND "feed.name" = 'NTP-Monitor';
UPDATE events
   SET "classification.identifier" = 'ssl-poodle', "feed.name" = 'SSL-POODLE-Vulnerable-Servers'
   WHERE "classification.identifier" = 'SSL-Poodle' AND "feed.name" = 'Ssl-Scan';
UPDATE events
   SET "classification.identifier" = 'ssl-freak', "feed.name" = 'SSL-FREAK-Vulnerable-Servers'
   WHERE "classification.identifier" = 'SSL-FREAK' AND "feed.name" = 'Ssl-Freak-Scan';
UPDATE events
   SET "classification.identifier" = 'open-memcached'
   WHERE "classification.identifier" = 'openmemcached' AND "feed.name" = 'Open-Memcached';
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
   SET "classification.identifier" = 'open-smb'
   WHERE "classification.identifier" = 'opensmb' AND "feed.name" = 'Accessible-SMB';
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
   SET "classification.identifier" = 'open-vnc'
   WHERE "classification.identifier" = 'accessiblevnc' AND "feed.name" = 'Accessible-VNC';
```

1.0.6 Bugfix release (2018-08-31)
---------------------------------

### Libraries
- Some optional dependencies do not support Python 3.3 anymore. If your are still using this unsuported version consider upgrading. IntelMQ 1.0.x itself is compatible with Python 3.3.

### Postgres databases
Use the following statement carefully to upgrade your database.
Adapt your feedname in the query to the one used in your setup.
```SQL
UPDATE events
   SET "classification.taxonomy" = 'abusive content', "classification.type" = 'spam', "classification.identifier" = 'spamlink', "malware.name" = NULL, "event_description.text" = 'The URL appeared in a spam email sent by extra.spam_ip.', "source.url" = "destination.ip", "destination.ip" = NULL
   WHERE "malware.name" = 'l_spamlink' AND "feed.name" = 'Spamhaus CERT';
UPDATE events
   SET "classification.taxonomy" = 'other', "classification.type" = 'other', "classification.identifier" = 'proxyget', "malware.name" = NULL, "event_description.text" = 'The malicous client used a honeypot as proxy.'
   WHERE "malware.name" = 'proxyget' AND "feed.name" = 'Spamhaus CERT';
```


1.0.5 Bugfix release (2018-06-21)
---------------------------------
### Postgres databases
Use the following statement carefully to upgrade your database.
Adapt your feedname in the query to the one used in your setup.
```SQL
UPDATE events
    SET "extra" = json_build_object('source.local_port', "extra"->'destination.local_port')
    WHERE "feed.name" = 'Spamhaus CERT' AND "classification.type" = 'brute-force' AND "classification.identifier" = 'telnet';
```

1.0.4 Bugfix release (2018-04-20)
---------------------------------

### Postgres databases
Use the following statement carefully to upgrade your database.
Adapt your feedname in the query to the one used in your setup.
```SQL
UPDATE events
   SET "classification.taxonomy" = 'intrusion attempts', "classification.type" = 'brute-force', "classification.identifier" = 'rdp', "protocol.application" = 'rdp', "malware.name" = NULL
   WHERE "malware.name" = 'iotrdp' AND "feed.name" = 'Spamhaus CERT';
UPDATE events
   SET "classification.taxonomy" = 'vulnerable', "classification.type" = 'vulnerable service', "classification.identifier" = 'openrelay', "protocol.application" = 'smtp', "malware.name" = NULL
   WHERE "malware.name" = 'openrelay' AND "feed.name" = 'Spamhaus CERT';
UPDATE events
   SET "protocol.application" = 'portmapper'
   WHERE "classification.identifier" = 'openportmapper' AND "feed.name" = 'Open-Portmapper';
UPDATE events
   SET "protocol.application" = 'netbios-nameservice'
   WHERE "classification.identifier" = 'opennetbios' AND "feed.name" = 'Open-NetBIOS-Nameservice';
UPDATE events
   SET "protocol.application" = 'ipsec'
   WHERE "classification.identifier" = 'openike' AND "feed.name" = 'Vulnerable-ISAKMP';
UPDATE events
   SET "classification.taxonomy" = 'intrusion attempts', "classification.type" = 'brute-force', "classification.identifier" = 'ssh', "malware.name" = NULL, "protocol.application" = 'ssh'
   WHERE "malware.name" = 'sshauth' AND "feed.name" = 'Spamhaus CERT';
UPDATE events
   SET "classification.taxonomy" = 'intrusion attempts', "classification.type" = 'brute-force', "classification.identifier" = 'telnet', "malware.name" = NULL, "protocol.application" = 'telnet'
   WHERE ("malware.name" = 'telnetauth' OR "malware.name" = 'iotcmd' OR "malware.name" = 'iotuser') AND "feed.name" = 'Spamhaus CERT';
UPDATE events
   SET "classification.taxonomy" = 'information gathering', "classification.type" = 'scanner', "classification.identifier" = 'wordpress-vulnerabilities', "malware.name" = NULL, "event_description.text" = 'scanning for wordpress vulnerabilities', "protocol.application" = 'http'
   WHERE "malware.name" = 'wpscanner' AND "feed.name" = 'Spamhaus CERT';
UPDATE events
   SET "classification.taxonomy" = 'information gathering', "classification.type" = 'scanner', "classification.identifier" = 'wordpress-login', "malware.name" = NULL, "event_description.text" = 'scanning for wordpress login pages', "protocol.application" = 'http'
   WHERE "malware.name" = 'w_wplogin' AND "feed.name" = 'Spamhaus CERT';
UPDATE events
   SET "classification.taxonomy" = 'intrusion attempts', "classification.type" = 'scanner', "classification.identifier" = 'scanner-generic', "malware.name" = NULL, "event_description.text" = 'infected IoT device scanning for other vulnerable IoT devices'
   WHERE "malware.name" = 'iotscan' AND "feed.name" = 'Spamhaus CERT';
```

1.0.3 Bugfix release (2018-02-05)
---------------------------------

### Configuration
- `bots.parsers.cleanmx` removed CSV format support and now only supports XML format. Therefore, CleanMX collectors must define the `http_url` parameter with the feed url which points to XML format. See Feeds.md file on documentation section to get the correct URLs. Also, downloading the data from CleanMX feed can take a while, therefore, CleanMX collectors must overwrite the `http_timeout_sec` parameter with the value `120`.
- The classification mappings for the n6 parser have been corrected:

| n6 classification | Previous classification |  |  | Current classification |  |  | Notes |
|-|-|-|-|-|-|-|-|
|                   | taxonomy   | type   | identifier | taxonomy       | type    | identifier |
| dns-query         | other      | other  | ignore me  | other          | other   | dns-query  |
| proxy             | vulnerable | proxy  | open proxy | other          | proxy   | openproxy  |
| sandbox-url       | ignore     | ignore | ignore me  | malicious code | malware | sandboxurl | As this previous taxonomy did not exist, these events have been rejected |
| other             | vulnerable | unknow | unknown    | other          | other   | other      |

### Postgres databases
Use the following statement carefully to upgrade your database.
Adapt your feedname in the query to the one used in your setup.
```SQL
UPDATE events
   SET "classification.identifier" = 'dns-query'
   WHERE "feed.name" = 'n6' AND "classification.taxonomy" = 'other' AND "classification.type" = 'other' AND "classification.identifier" = 'ignore me';
UPDATE events
   SET "classification.taxonomy" = 'malicious code' AND "classification.type" = 'malware' AND "classification.identifier" = 'sandboxurl'
   WHERE "feed.name" = 'n6' AND "classification.taxonomy" = 'vulnerable' AND "classification.type" = 'ignore' AND "classification.identifier" = 'ignore me';
UPDATE events
   SET "classification.taxonomy" = 'other' AND "classification.type" = 'other' AND "classification.identifier" = 'other'
   WHERE "feed.name" = 'n6' AND "classification.taxonomy" = 'vulnerable' AND "classification.type" = 'unknow' AND "classification.identifier" = 'unknow';
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
