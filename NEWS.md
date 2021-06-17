<!-- comment
   SPDX-FileCopyrightText: 2015-2021 Sebastian Wagner
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

NEWS
====

This file lists all changes which have an affect on the administration of IntelMQ and contains steps that you need to be aware off for the upgrade.
Please refer to the changelog for a full list of changes.

3.0.0 Major release (unreleased)
--------------------------------

### Requirements
IntelMQ now uses YAML for the runtime configuration and therefore needs the `ruamel.yaml` library.

### Tools

#### intelmqdump
The command `e` for deleting single entries by given IDs has been merged into the command `d` ("delete"), which can now delete either entries by ID or the whole file.
The command `v` for editing entries has been renamed to `e` ("edit").

#### Cronjobs
The deprecated shell scripts
- `update-asn-data`
- `update-geoip-data`
- `update-tor-nodes`
- `update-rfiprisk-data`
have been removed in favor of the built-in update-mechanisms (see the bots' documentation). A crontab file for calling all new update command can be found in `contrib/cron-jobs/intelmq-update-database`.

### Bots

Both the XMPP collector bot and the XMPP output bot were removed. This [was evaluated on the mailinglist](https://lists.cert.at/pipermail/intelmq-users/2020-October/000177.html)
and the XMPP bots were deprecated in 391d625.

#### Sieve expert
The Sieve expert bot has had major updates to its syntax. Breaking new changes:
* the removal of the `:notcontains` operator, which can be replaced using the newly added
 expression negation, e.g `! foo :contains ['.mx', '.zz']` rather than `foo :notcontains ['.mx', '.zz']`. 
* changed operators for comparisons against lists of values, e.g `source.ip :in ['127.0.0.5', '192.168.1.2']` rather than `source.ip == ['127.0.0.5', '192.168.1.2']`
  The "old" syntax with `==` on lists is no longer valid and raises an error.

New features:
* arbitrary nesting of if clauses + mixed conditionals and actions in the same level of nesting
* new matches on fields containing list values and boolean values
* new list-based actions
* negation of arbitrary expressions and expression groups separated by brackets through a prepended `!`, e.g `! src.port :in [80, 443]`
* non-string values accepted by `add`/`add!`/`update`

The [sieve bot documentation](https://intelmq.readthedocs.io/en/maintenance/user/bots.html#intelmq-bots-experts-sieve-expert) has been updated to reflect on these new changes.

### Harmonization
The classification scheme has been updated to better match the [Reference Security Incident Taxonomy (RSIT)](https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/). The following labels were renamed, deleted or merged into others:

| old taxonomy name | old type name | new taxonomy name | new type name |
|-|-|-|-|
| abusive content              |                    | abusive-content              |                                        |
| information content security |                    | information-content-security |                                        |
| information content security | leak               | information-content-security | data-leak                              |
| intrusion attempts           |                    | intrusion-attempts           |                                        |
| information gathering        |                    | information-gathering        |                                        |
| intrusions                   | compromised        | intrusions                   | system-compromise                      |
| intrusions                   | defacement         | information-content-security | unauthorised-information-modification  |
| intrusions                   | unauthorized-login | intrusions                   | system-compromise                      |
| intrusions                   | unauthorized-command | intrusions                 | system-compromise                      |
| malicious code               |                    | malicious-code               |                                        |
| malicious code               | c2server           | malicious-code               | c2-server                              |
| malicious code               | malware            | malicious-code               | infected-system / malware-distribution |
| malicious code               | dga domain         | other                        | dga-domain                             |
| malicious code               | malware            | other                        | malware                                |
| malicious code               | ransomware         | malicious-code               | infected-system                        |
| vulnerable                   | vulnerable client  | vulnerable                   | vulnerable-system                      |
| vulnerable                   | vulnerable service | vulnerable                   | vulnerable-system                      |
| other                        | unknown            | other                        | undetermined                           |

- For the taxonomy 'availability', the type `misconfiguration` is new.
- For the taxonomy 'intrusions', the type `system-compromise` is new.
- For the taxonomy 'other', the types `malware` and `undetermined` are new.

The old `classification.type` names can still be used in code, and they are automatically converted to the new names.
Existing data in databases and alike are *not* changed automatically.
See the section "Postgres databases" below for instructions to update existing data in databases.

#### "Malware"

The previously existing classification type "malware" under the taxonomy "malicious code" was removed, as this type does not exist in the RSIT.
Most of the usages were wrong anyway, and should have been infected-device, malware-distribution or something else anyway.
There is only one usage in IntelMQ, which can not be changed.
And that one is really about malware itself (or: the hashes of samples). For this purpose, the new type "malware" under the taxonomy "other" was created, *slightly* deviating from the RSIT in this respect, but "other" can be freely extended.

### Configuration

The `defaults.conf` file was removed. Settings that should effect all the bots are not part of the runtime.conf file and are configured in the `global` section in that file.
The `intelmqctl upgrade-config` command migrates the existing values from the `defaults.conf` file to the `runtime.conf` file under the `global` section and then deletes the `defaults.conf` file.
The `pipeline.conf` file was removed. The source- and destination-queues of the bots are now configured in the bot configuration itself, thus in the `runtime.conf` file.
The `intelmqctl upgrade-config` command migrates the existing configuration from the `pipeline.conf` file to the individual bot configurations in the `runtime.conf` configuration file.
The `runtime.conf` file was replaced by a `runtime.yaml` file. IntelMQ moves the file for you if it does not find a runtime.conf but a runtime.yaml file. When IntelMQ changes the file, it now writes YAML syntax.

#### Removal of deprecated bots and behaviour
- The bot `intelmq.bots.experts.ripencc_abuse_contact.expert` has been removed. It was replaced by `intelmq.bots.experts.ripe.expert` and marked as deprecated in 2.0.0.beta1.
- Modify expert: Compatibility with the deprecated configuration format (before 1.0.0.dev7) was removed.
- RT collector: compatibility with the deprecated parameter `unzip_attachment` (removed in 2.1.0) was removed.


### Libraries

### Postgres databases
The following statements optionally update existing data for the harmonization classification changes:
```SQL
UPDATE events
   SET "classification.taxonomy" = 'abusive-content'
   WHERE "classification.taxonomy" = 'abusive content';
UPDATE events
   SET "classification.taxonomy" = 'information-content-security'
   WHERE "classification.taxonomy" = 'information content security';
UPDATE events
   SET "classification.type" = 'data-leak'
   WHERE "classification.type" = 'leak' AND "classification.taxonomy" = 'information-content-security';
UPDATE events
   SET "classification.taxonomy" = 'intrusion-attempts'
   WHERE "classification.taxonomy" = 'intrusion attempts';
UPDATE events
   SET "classification.taxonomy" = 'information-gathering'
   WHERE "classification.taxonomy" = 'information gathering';
UPDATE events
   SET "classification.type" = 'system-compromise'
   WHERE "classification.type" IN ('compromised', 'unauthorized-login', 'unauthorized-command');
UPDATE events
   SET "classification.taxonomy" = 'information-content-security', "classification.type" = 'unauthorised-information-modification'
   WHERE "classification.taxonomy" = 'intrusions', "classification.type" = 'defacement'
UPDATE events
   SET "classification.taxonomy" = 'malicious-code'
   WHERE "classification.taxonomy" = 'malicious code';
UPDATE events
   SET "classification.type" = 'c2-server'
   WHERE "classification.taxonomy" = 'malicious-code' AND "classification.type" = 'c2server';
UPDATE events
   SET "classification.type" = 'vulnerable-system'
   WHERE "classification.taxonomy" = 'vulnerable' AND ("classification.type" = 'vulnerable service' OR "classification.type" = 'vulnerable client');
UPDATE events
   SET "classification.type" = 'undetermined'
   WHERE "classification.taxonomy" = 'other' AND "classification.type" = 'unknown';
UPDATE events
   SET "classification.taxonomy" = 'other', "classification.type" = 'dga-domain'
   WHERE "classification.taxonomy" = 'malicious-code' AND "classification.type" = 'dga domain';
```
Depending on the data (e.g. feed), the correct statement for the `malware` type deprecation may be either this:
```sql
UPDATE events
   SET "classification.type" = 'infected-system'
   WHERE "classification.taxonomy" = 'malicious-code' AND ("classification.type" = 'malware' OR "classification.type" = 'ransomware');
```
or this:
```sql
UPDATE events
   SET "classification.type" = 'malware-distribution'
   WHERE "classification.taxonomy" = 'malicious-code' AND ("classification.type" = 'malware' OR "classification.type" = 'ransomware');
```
or this:
```sql
UPDATE events
   SET "classification.taxonomy" = 'other'
   WHERE "classification.type" = 'malware';
```


2.3.3 Bugfix release (2021-05-31)
---------------------------------

### Configuration

#### Feodotracker Browse
The parameters required to parse the Abuse.ch Feodotracker Browse feed with the HTML Table parser have changed.
Old parameters:
- `columns`: `time.source,source.ip,malware.name,status,extra.SBL,source.as_name,source.geolocation.cc`
- `ignore_values`: `,,,,Not listed,,`
New parameters:
- `columns`: `time.source,source.ip,malware.name,status,source.as_name,source.geolocation.cc`
- `ignore_values`: `,,,,,`
The column with the SBL number has been removed.
These parameters remain unchanged:
- `skip_table_head`: `true`
- `type`: `c2server`

Please adapt the configuration of your configured bots.
The `intelmqctl upgrade-config` command automatically fixes a configuration if the parser for this feed is detected by the bot ID (name contains "feodo") and its parameters.

#### Shadowserver

Shadowserver changed some of their feeds, for more information see [Changes in Sinkhole and Honeypot Report Types and Formats](https://www.shadowserver.org/news/changes-in-sinkhole-and-honeypot-report-types-and-formats/). Support for the legacy feeds has not been removed yet.

The [Shadowserver Parser Bot documentation](https://intelmq.readthedocs.io/en/maintenance/user/bots.html#shadowserver-supported-reports) lists the supported feeds, as well as the legacy feeds.


2.3.2 Bugfix release (2021-04-27)
---------------------------------

No changes are required by administrators.


2.3.1 Bugfix release (2021-03-25)
---------------------------------

No changes are required by administrators.


2.3.0 Feature release (2021-03-04)
---------------------------------

The documentation is now available at [intelmq.readthedocs.io](https://intelmq.readthedocs.io/).

### Requirements
IntelMQ no longer supports Python 3.5 (and thus Debian 9 and Ubuntu 16.04), the minimum supported Python version is 3.6.
CentOS 7 (with EPEL) provides both Python 3.4 and Python 3.6. If IntelMQ was installed manually with Python 3.4, the code needs to be re-installed with Python 3.6 and removed for Python 3.4. Application data is compatible. To install the Python 3.6 packages, use: `yum install python36 python36-devel python36-requests`.

### Bots

#### Bot option `--update-database`
- Bots that require a database file (such as `maxmind_geoip`, `asn_lookup`, `tor_nodes` and `recordedfuture_iprisk`)
  have a new command line option `--update-database`. It is not necessary to specify a
  bot ID, the function automatically updates the database for all the bots of the same
  type and reloads them afterwards. Removes any external dependencies (such as curl or wget).
  This is a replacement for shell scripts such as `update-tor-nodes`, `update-asn-data`,
  `update-geoip-data`, `update-rfiprisk-data`.
  
  Usage:
  ```
  intelmq.bots.experts.asn_lookup.expert --update-database
  intelmq.bots.experts.maxmind_geoip.expert --update-database
  intelmq.bots.experts.recordedfuture_iprisk.expert --update-database
  intelmq.bots.experts.tor_nodes.expert --update-database
  ```
  The provided shell scripts use these new commands, however they are now deprecated and will be removed in version 3.0.
- `intelmqctl list queues` is now able to sum events over all queues with the `--sum`, `--count` or simple `-s` flag.

#### XMPP Bots
Both the XMPP output bot and the XMPP collector bot are deprecated.
The bots need to be migrate to another XMPP library (see [#1614](https://github.com/certtools/intelmq/issues/1614) for details) and a survey on the mailing listed revealed no users.
If you depend on this bot, please reach out to us via the mailing list or GitHub.
The bots are logging a deprecation warning now and the current plan is to remove them in IntelMQ version 3.0.

#### Shadowserver Bots
The Shadowserver Collector is now able to collect data from the [Shadowserver Reports API](https://intelmq.readthedocs.io/en/maintenance/user/bots.html#shadowserver-reports-api). Moreover the Shadowserver Parser now supports the JSON format used by the Reports API.

#### Sieve Expert
Sieve-Expert is now capable of basic math operations & you can do actions without any `if` statements.

1. How to use basic math in sieve, only with DateTimes currently:
```
add time.observation += '1 hour'
add time.observation -= '10 hours'
```
2. Actions can now be used without an `if` statement, just write the following into a `.sieve` file:
```
add comment = "Adding this to all computed events"
```
More details can be found in our [documentation](https://intelmq.readthedocs.io/en/maintenance/user/bots.html#sieve).

#### Kafka Collector
Now you're able to fetch data from Kafka with the [Kafka Collector](https://intelmq.readthedocs.io/en/maintenance/user/bots.html#kafka).

### Configuration
#### Abuse.ch URLHaus feed
The feed template for the URLHaus feed contained a spelling error:
The correct name for the parameter "delimeter" is "delimiter". Please fix your configured bots.
The `intelmqctl upgrade-config` command automatically fixes a configuration if the misspelling is detected.

#### IntelMQ-Manager -> IntelMQ-API
`IntelMQ-Manager` PHP backend is getting replaced by the newly developed `IntelMQ-API`. The `IntelMQ-Manager` release only contains the files for the web frontend. The `IntelMQ-Manager` packages now depend or recommend the installation of the `IntelMQ-API` package, therefore a normal upgrade should pull in the API. Follow the instructions in our [documentation](https://intelmq.readthedocs.io/en/maintenance/user/intelmq-api.html) to configure the API. It uses its own authentication backend now, how to setup users is described in the [documentation](https://intelmq.readthedocs.io/en/maintenance/user/intelmq-api.html#adding-a-user).

### Postgres databases
There was a spelling error in the Spamhaus CERT Parser's "event_description.text" texts.
The following statements optionally update existing data.
Please check if you did use these feed names and eventually adapt them for your setup!
```sql
UPDATE events
   SET "event_description.text" = 'The malicious client used a honeypot as proxy.'
   WHERE "event_description.text" = 'The malicous client used a honeypot as proxy.' AND "classification.taxonomy" = 'other' AND "classification.type" = 'other' AND "classification.identifier" = 'proxyget' AND "feed.name" = 'Spamhaus CERT';
UPDATE events
   SET "event_description.text" = 'The infected iot device logged in to a honeypot and issued malicious commands.'
   WHERE "event_description.text" = 'The infected iot device logged in to a honeypot and issued malicous commands.' AND "classification.taxonomy" = 'intrusions' AND "classification.type" = 'unauthorized-command' AND "classification.identifier" = 'iot' AND "feed.name" = 'Spamhaus CERT';
```

2.2.3 Bugfix release (2020-12-23)
---------------------------------

### Harmonization
A bug in the taxonomy expert did set the Taxonomy for the type `scanning` to `information gathering`
whereas for the type `sniffing` and `social-engineering`, the taxonomy was correctly set to `information-gathering`.
This inconsistency for the taxonomy `information-gathering` is now fixed, but the data eventually needs to fixed in data output (databases) as well.

There are still some inconsistencies in the naming of the classification taxonomies and types,
more fixes will come in version 3.0.0. See [issue #1409](https://github.com/certtools/intelmq/issues/1409).

### Postgres databases
The following statements optionally update existing data.
Please check if you did use these feed names and eventually adapt them for your setup!
```SQL
UPDATE events
   SET "classification.taxonomy" = 'information-gathering'
   WHERE "classification.taxonomy" = 'information gathering';
```

2.2.2 Bugfix release (2020-10-28)
---------------------------------

### Bots
#### Cymru Whois Lookup
The cache key calculation has been fixed. It previously led to duplicate keys for different IP addresses and therefore wrong results in rare cases. The cache key calculation is intentionally not backwards-compatible. Therefore, this bot may take longer processing events than usual after applying this update.
More details can be found in [issue #1592](https://github.com/certtools/intelmq/issues/1592).

### Harmonization
#### Shadowserver Feed/Parser
The feed "Blacklisted-IP" has been renamed by ShadowServer to "Blocklist". In IntelMQ, the old name can still be used in IntelMQ until version 3.0.


2.2.1 Bugfix release (2020-07-30)
----------------------------------

### Requirements
#### MaxMind GeoIP Expert Bot
The current python library versions of geoip (version 4) and maxminddb (version 2) no longer support Python 3.5. Keep older versions of these libraries if you are using this Python version.

### Configuration
#### Abuse.ch URLHaus

The current documented value for the `column` parameter was:
```json
['time.source', 'source.url', 'status', 'extra.urlhaus.threat_type', 'source.fqdn', 'source.ip', 'source.asn', 'source.geolocation.cc']
```
Better is:
```json
['time.source', 'source.url', 'status', 'classification.type|__IGNORE__', 'source.fqdn|__IGNORE__', 'source.ip', 'source.asn', 'source.geolocation.cc']
```

2.2.0 Feature release (2020-06-18)
----------------------------------

### Requirements
- IntelMQ no longer supports Python 3.4, Python `>=` 3.5 is required.
  CentOS 7 (with EPEL) provides both Python 3.4 and Python 3.6. If IntelMQ was installed with Python 3.4, the code needs to be re-installed with Python 3.6 and removed for Python 3.4. Application data is compatible. To install needed packages: `yum install python36 python36-devel python36-requests`.
- The *AMQP collector* requires the `pika` library minimum version 1.0.

### Configuration

#### ElasticSearch Output Bot
The ElasticSearch Output bot does no longer support (only) ElasticSearch version 5, but only version 7 (#1513).

#### Microsoft Azure Collector Bot
The Bot has been majorly changed to support the current Azure Python library `azure-storage-blob>=12.0.0`.
This also changes the required configuration parameters. The new required parameters are:

* `redis_cache_db`: 5
* `redis_cache_host`: `"127.0.0.1"`
* `redis_cache_password`: null, depending on your Redis server configuration
* `redis_cache_port`: 6379, depending on your Redis server configuration
* `redis_cache_ttl`: 864000 (10 days), depending on how old fast the data you are fetching is removed from the storage
* `connection_string`: connection string as given by Microsoft, includes endpoint and authentication information
* `container_name`: name of the container to connect to

The previous parameters `account_name`, `account_key` and `delete` are not supported anymore.

#### URLVir Feeds and Parser
All URLVir feeds have been discontinued. The URLVir Parser has been removed.
The `intelmqctl upgrade-config` command warns if you have these feed and the bot in use.


2.1.3 Bugfix release (2020-05-26)
---------------------------------

### Requirements
The python library `requests` is required by the core.

### Harmonization
The regular expression of the field `protocol.transport` has been updated to accommodate the value `nvp-ii`.
`intelmqctl upgrade-config` handles the change to automatically upgrade your configuration.

#### Taichung feed
The Taichung feed "Netflow (Recent 30)" with URL `https://www.tc.edu.tw/net/netflow/lkout/recent/30` is no longer available and gives an error 500.
As a drop-in replacement the Parser as well as the Feed documentation are now adapted to the full feed available at `https://www.tc.edu.tw/net/netflow/lkout/recent/`.
The `intelmqctl upgrade-config` command takes care of this change.

#### Abuse.ch Zeus Tracker Feed
The Abuse.ch Zeus Tracker has been discontinued on 2019-07-08. The `intelmqctl upgrade-config` command warns if you have this feed in use.

#### Abuse.ch Ransomware Tracker Feed
The Abuse.ch Ransomware Tracker has been discontinued on 2019-12-08. The `intelmqctl upgrade-config` command warns if you have this feed in use.

#### Bitcash.cz Feed
The Bitcash.cz Banned IPs / Blocklist feed previously available under `https://bitcash.cz/misc/log/blacklist` is no longer available. The `intelmqctl upgrade-config` command warns if you have this feed in use.

#### Fraunhofer DDoS Attack Feed
The Fraunhofer DDoS Attack feed previously available under `https://feed.caad.fkie.fraunhofer.de/ddosattackfeed/` is no longer available. The `intelmqctl upgrade-config` command warns if you have this feed in use.

#### Bambenek Feeds
Many Bambenek feeds require a license now and URLs have changed. See https://osint.bambenekconsulting.com/feeds/ for more information. The `intelmqctl upgrade-config` command also warns if you have previously documents feeds in use and migrates the URL for the DGA domain feed.

#### Nothink Feeds and Parser
All Nothink Honeypot feeds have been discontinued and current the data available covers the time until 2019. The Nothink Parser has been removed.
The `intelmqctl upgrade-config` command warns if you have these feed and the bot in use.


2.1.2 Bugfix release (2020-01-28)
---------------------------------

#### MaxMind GeoIP
MaxMind requires a registration before being able to download the GeoLite2 database starting with 2019-12-30: https://blog.maxmind.com/2019/12/18/significant-changes-to-accessing-and-using-geolite2-databases/
If the provided `update-geoip-data` script is used, the license key can now be set second parameter.

### Libraries
When using MISP integrations, make sure your currently installed PyMISP version supports the installed Python version. Any PyMISP version newer than 2.4.119.1 requires Python 3.6 or newer.


2.1.1 Bugfix release (2019-11-11)
---------------------------------

### Tools
`intelmqctl check` and `intelmqctl upgrade-config` checks/applies a generic harmonization upgrade, checking for it's completeness.

### Harmonization
In version 2.1.0 a new field `extra` has been added to *Reports*. You need to add this to the *report* section in your harmonization configuration, or run `intelmqctl upgrade-config`:
```json
        "extra": {
            "description": "All anecdotal information of the report, which cannot be parsed into the data harmonization elements. E.g. subject of mails, etc. This is data is not automatically propagated to the events.",
            "type": "JSONDict"
        },
```

### Configuration
#### Defaults
For AMQP brokers, the port 15671 was used as default for connecting to the management interface. But RabbitMQ's default is 15672. This was corrected in this version. If you changed the port in RabbitMQ or IntelMQ (`intelmqctl_rabbitmq_monitoring_url`), the settings needs to be adapted.


2.1.0 Feature release (2019-10-15)
----------------------------------

Run `intelmqctl upgrade-config` and `intelmqctl check` after the upgrade.

### Configuration
#### Shadowserver Parser

The Shadowserver Parser is now able to detect the feed base on the report's field `extra.file_name`, added by collectors. Have a look at their documentation for more details.

#### PostgreSQL Output
The PostgreSQL Output Bot has been integrated into the new and generic SQL Output Bot
* module name:
  * old: `intelmq.bots.outputs.postgresql.output`
  * new: `intelmq.bots.outputs.sql.output`
* parameters:
  * new: `engine` = `postgresql`
IntelMQ versions 2.x will be compatible with previous configurations. `intelmqctl upgrade-config` migrates configurations.


2.0.2 Bugfix release (2019-10-14)
---------------------------------

Run `intelmqctl upgrade-config` and `intelmqctl check` after the upgrade.

### Configuration
The deprecated parameter `feed` for collectors is again supported as the documentation as not properly updated. The support will be removed before version 2.2.

#### RIPE expert
In the upgrade function for version 1.1.0 (in effect in version 2.0.1) the addition of the parameter `query_ripe_stat_ip` was not correctly done and is maybe missing. A new upgrade function re-adds it with the value of `query_ripe_stat_ip`.

#### Cymru CAP Feed Migration

The Cymru CAP Feed is (being) migrated to a new URL with a different format and more data. Look at the feed's documentation for more information.

#### Cymru Whois Expert, Modify Expert & Reverse DNS Expert
These bots overwrite existing fields by default. A parameter `overwrite` has been added to make this optional, with the default value of `True` for backwards compatibility. If the parameter is not set, a warning is logged. The default value will change to `False` in version 3.0.0. The default for all new bots (in `BOTS`) is `False` already.


2.0.1 Bugfix release (2019-08-23)
---------------------------------

### Tools
intelmqctl has a new function `intelmqctl upgrade-config` to upgrade the configuration from previous installations. It is recommended to call this function after every upgrade.


2.0.0 Major release (2019-05-22)
--------------------------------

See also the news for 2.0.0.beta1 below.

### Harmonization
The allowed values for the `classification.type` field have been updated to the RSIT mapping. These values have changed and are automatically mapped:
  - `botnet drone` with `infected-system`
  - `infected system` with `infected-system`
  - `ids alert` with `ids-alert`
  - `c&c` with `c2server`
  - `malware configuration` with `malware-configuration`

### Configuration
Four new values have been introduced to configure the statistics database. Add them to your `defaults.conf` file:
* `statistics_database`: `3`,
* `statistics_host`: `"127.0.0.1"`,
* `statistics_password`: `null`,
* `statistics_port`: `6379`,

#### TCP Output
Version 1.1.2 broke the compatibility of the TCP Output with third-party counterparts like filebeat, but is more stable for a TCP Collector counterpart. A new parameter `counterpart_is_intelmq` has been introduced, it's default is `false` for backwards compatibility. If you use a TCP collector, set this to `true`, otherwise to `false`.

### Postgres databases
The following statements optionally update existing data.
Please check if you did use these feed names and eventually adapt them for your setup!
```SQL
UPDATE events
   SET "classification.type" = 'infected-system'
   WHERE "classification.type" = 'botnet drone';
UPDATE events
   SET "classification.type" = 'infected-system'
   WHERE "classification.type" = 'infected system';
UPDATE events
   SET "classification.type" = 'ids-alert'
   WHERE "classification.type" = 'ids alert';
UPDATE events
   SET "classification.type" = 'c2server'
   WHERE "classification.type" = 'c&c';
UPDATE events
   SET "classification.type" = 'malware-configuration'
   WHERE "classification.type" = 'malware configuration';
```

2.0.0.beta1 release (2019-04-10)
-------------------------------

There are some features considered as beta and marked as such in the documentation, do not use them in production yet.

### Configuration
The bot `intelmq.bots.experts.ripencc_abuse_contact.expert` has been renamed to `intelmq.bots.experts.ripe.expert`, the compatibility shim will be removed in version 3.0. Adapt your `runtime.conf` accordingly.


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
A new harmonization type `JSONDict` has been added specifically for the `extra` field. It is highly recommended to change the type of this field. The change is backwards compatible and the change is not yet necessary, IntelMQ 1.x.x works with the old configuration too.

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
- Some optional dependencies do not support Python 3.3 anymore. If your are still using this unsupported version consider upgrading. IntelMQ 1.0.x itself is compatible with Python 3.3.

### Postgres databases
Use the following statement carefully to upgrade your database.
Adapt your feedname in the query to the one used in your setup.
```SQL
UPDATE events
   SET "classification.taxonomy" = 'abusive content', "classification.type" = 'spam', "classification.identifier" = 'spamlink', "malware.name" = NULL, "event_description.text" = 'The URL appeared in a spam email sent by extra.spam_ip.', "source.url" = "destination.ip", "destination.ip" = NULL
   WHERE "malware.name" = 'l_spamlink' AND "feed.name" = 'Spamhaus CERT';
UPDATE events
   SET "classification.taxonomy" = 'other', "classification.type" = 'other', "classification.identifier" = 'proxyget', "malware.name" = NULL, "event_description.text" = 'The malicious client used a honeypot as proxy.'
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
| other             | vulnerable | unknown| unknown    | other          | other   | other      |

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
