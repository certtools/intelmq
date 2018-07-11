CHANGELOG
==========


1.2.0 (unreleased)
------------------

### Core

### Harmonization

### Bots
#### Collectors

#### Parsers

#### Experts
- added `intelmq.bots.experts.recordedfuture_iprisk` (#1267).

#### Outputs

### Documentation

### Packaging

### Tests

### Contrib

### Known issues

1.1.0 (unreleased)
------------------
- Support for Python 3.3 has been dropped, it reached its end of life.
- The list of feeds docs/Feeds.md has now a machine-readable equivalent YAML file in intelmq/etc/feeds.yaml
  A tool to convert from yaml to md has been added.

### Tools
- `intelmq_gen_feeds_docs` add to bin directory, allows generating the Feeds.md documentation file from feeds.yaml
- `intelmq_gen_docs` merges both `intelmq_gen_feeds_docs` and `intelmq_gen_harm_docs` in one file and automatically updates the documentation files.

#### intelmqctl
- `intelmqctl start` prints the bot's last error messages if the bot failed to start (#1021).
- `intelmqctl start` message "is running" is printed every time. (Until now, it wasn't said when a bot was just starting.)
- `intelmqctl start/stop/restart/reload/status` now have a "--group" flag which allows you to specify the group of the bots that should be influenced by the command.
- `intelmqctl check` checks for defaults.conf completeness if the shipped file from the package can be found.
- `intelmqctl check` shows errors for non-importable bots.
- `intelmqctl list bots -q` only prints the IDs of enabled bots.
- `intelmqctl list queues-and-status` prints both queues and bots statuses (so that it can be used in eg. intelmq-manager).
- `intelmqctl run` parameter for showing a sent message.
- `intelmqctl run` if message is sent to a non-default path, it is printed out.
- `intelmqctl restart` bug fix; returned some half-nonsense, now returns return state of start and stop operation in a list (#1226).
- `intelmqctl check`: New parameter `--no-connections` to prevent the command from making connections e.g. to the redis pipeline.s


### Contrib
- tool `feeds-config-generator` to automatically generate the collector and parser runtime and pipeline configurations.
- `malware_name_mapping`: Download and convert tool for malware family name mapping has been added.
- Added a systemd script which creates systemd units for bots (#953).

### Core
- lib/bot
  - use SIGTERM instead of SIGINT to stop bots (#981).
  - Bots can specify a static method `check(parameters)` which can perform individual checks specific to the bot.
    These functions will be called by `intelmqctl check` if the bot is configured with the given parameters
  - top level bot parameters (description, group, module, name) are exposed as members of the class.
  - The parameter `feed` for collectors is deprecated for 2.0 and has been replaced by the more consistent `name` (#1144).
  - bug: allow path parameter for CollectorBot class.
- lib/message:
  - Subitems in fields of type `JSONDict` (see below) can be accessed directly. E.g. you can do:
    event['extra.foo'] = 'bar'
    event['extra.foo'] # gives 'bar'
    It is still possible to set and get the field as whole, however this may be removed or changed in the future:
    event['extra'] = '{"foo": "bar"}'
    event['extra'] # gives '{"foo": "bar"}'
    "Old" bots and configurations compatible with 1.0.x do still work.
    Also, the extra field is now properly exploded when exporting events, analogous to all other fields.
  - `Message.add`: The parameter `overwrite` accepts now three different values: `True`, `False` and `None` (new).
    True: An existing value will be overwritten
    False: An existing value will not be overwritten (previously an exception has been raised when the value was given).
    None (default): If the value exists an `KeyExists` exception is thrown (previously the same as False).
    This allows shorter code in the bots, as an 'overwrite' configuration parameter can be directly passed to the function.
  - The message class has now the possibility to return a default value for non-exisiting fields, see `Message.set_default_value`.
- Add `RewindableFileHandle` to utils making handling of CSV files more easy (optionally)
- lib/pipeline:
  * you may now define more than one destination queues path the bot should pass the message to, see [Pipelines](https://github.com/certtools/intelmq/blob/develop/docs/User-Guide.md#pipeline-configuration) (#1088, #1190).
  * the special path `"_on_error"` can be used to pass messages to different queues in case of processing errors (#1133).
- `lib/harmonization`: Accept `AS` prefix for ASN values (automatically stripped).

### Bots
- Removed print statements from various bots.
- Replaced various occurences of `self.logger.error()` + `self.stop()` with `raise ValueError`.

#### Collectors
- `bots.collectors.mail`:
  - New parameters; `sent_from`: filter messages by sender, `sent_to`: filter messages by recipient
  - More debug logs
- `bots.collectors.n6.collector_stomp`: renamed to `bots.collectors.stomp.collector` (#716)
- bots.collectors.rt:
  - New parameter `search_requestor` to search for field Requestor.
  - Empty strings and `null` as value for search parameters are ignored.
  - Empty parameters `attachment_regex` and `url_regex` handled.
- `bots.collectors.http.collector_http`: Ability to optionally use the current time in parameter `http_url`, added parameter `http_url_formatting`.
- `bots.collectors.stomp.collector`: Heartbeat timeout is now logged with log level info instead of warning.
- added `intelmq.bots.collectors.twitter.collector_twitter`
- added `intelmq.bots.collectors.tcp.collector` that can be bound to another IntelMQ instance by a TCP output
- `bots.collectors.microsoft.collector_interflow`: added for MS interflow API
  - Automatic ungzipping for .gz files.
- added `intelmq.bots.collectors.calidog.collector_certstream` for collecting certstream data (#1120).
- added `intelmq.bots.collectors.shodan.collector_stream` for collecting shodan stream data (#1096).

#### Parsers
- `bots.parsers.shadowserver`:
  - changed feednames . Please refer to it's README for the exact changes.
  - If the conversion function fails for a line, an error is raised and the offending line will be handled according to the error handling configuration.
    Previously errors like these were only logged and ignored otherwise.
  - add support for the feed `Accessible-Hadoop`
  - Remove deprecated parameter `override`, use `overwrite` instead (#1071).
- The Generic CSV Parser `bots.parsers.generic.parser_csv`:
  - It is possible to filter the data before processing them using the new parameters `filter_type` and `filter_text`.
  - It is possible to specify multiple columns using `|` character in parameter `columns`.
  - The parameter `time_format` now supports `'epoch_millis'` for seconds since the Epoch, milliseconds are supported but not used.
- renamed `bots.parsers.cymru_full_bogons.parser` to `bots.parsers.cymru.parser_full_bogons`, compatibility shim will be removed in version 2.0
- added `bots.parsers.cymru.parser_cap_program`
- added `intelmq.bots.parsers.zoneh.parser` for ZoneH feeds
- added `intelmq.bots.parsers.sucuri.parser`
- added `intelmq.bots.parsers.malwareurl.parser`
- added `intelmq.bots.parsers.threatminer.parser`
- added `intelmq.bots.parsers.webinspektor.parser`
- added `intelmq.bots.parsers.twitter.parser`
- added `intelmq.bots.parsers.microsoft.parser_ctip`
  * ignore the invalid IP '0.0.0.0' for the destination
  * fix the raw/dumped messages, did not contain the paling list previously.
  * use the new harmonization field `tlp` instead of `extra.tlp`.
- `bots.parsers.alienvault.parser_otx`: Save TLP data in the new harmonization field `tlp`.
- added `intelmq.bots.parsers.openphish.parser_commercial`
- added `intelmq.bots.parsers.microsoft.parser_bingmurls`
- added `intelmq.bots.parsers.calidog.parser_certstream` for parsing certstream data (#1120).
- added `intelmq.bots.parsers.shodan.parser` for parsing shodan data (#1096).

#### Experts
- Added sieve expert for filtering and modifying events (#1083)
 * capable of distributing the event to appropriate named queues
- `bots.experts.modify`
  * default rulesets: all malware name mappings have been migrated to the [Malware Name Mapping repository](https://github.com/certtools/malware_name_mapping) ruleset. See the new added contrib tool for download and conversion.
  * new parameter `case_sensitive` (default: True)
- Added wait expert for sleeping
- Added domain suffix expert to extract the TLD/Suffix from a domain name.
- `bots.experts.maxmind_geoip`: New (optional) parameter `overwrite`, by default false. The current default was to overwrite!
- `intelmq.bots.experts.ripencc_abuse_contact`: Remove deprecated parameter `query_ripe_stat`, use `query_ripe_stat_asn` and `query_ripe_stat_ip` instead (#1071).

#### Outputs
- `bots.outputs.file`:
  - String formatting can be used for file names with new parameter `format_filename`.
  - New parameter `single_key` to only save one field.

### Harmonization
- Renamed `JSON` to `JSONDict` and added a new type `JSON`. `JSONDict` saves data internally as JSON, but acts like a dictionary. `JSON` accepts any valid JSON.
- fixed regex for `protocol.transport` it previously allowed more values than it should have.
- New ASN type. Like integer but checks the range.
- added `destination.urlpath` and `source.urlpath` to harmonization.
- New field `tlp` for tlp level specification.
  - New TLP type. Allows all four tlp levels, removes 'TLP:' prefix and converts to upper case.
- Added new `classification.type` 'vulnerable client'
- Added `(destination|source).domain_suffix` to hold the TLD/domain suffix.
- New allowed value for `classification.type`: `infected system` for taxonomy `malicious code` (#1197).

### Requirements
- Requests is no longer listed as dependency of the core. For depending bots the requirement is noted in their REQUIREMENTS.txt file.

### Documentation
- Use Markdown for README again, as pypi now supports it.

### Tests
- Travis now correctly stops if a requirement could not be installed (#1257).
- New tests for validating `etc/feeds.yaml` and `bots/BOTS` using cerberus and schemes are added (#1166).
- New test for checking if `docs/Feeds.md` is up to date with `etc/feeds.yaml`.

### Known bugs
- `bots.experts.sieve` does not support textX (#1246).
- performance degradation for extra fields (#1117).
- Postgres output: support condensed JSONDicts (#1107).
- Bots started with IntelMQ-Manager stop when the webserver is restarted (#952).

1.0.6 Bugfix release (unreleased)
---------------------------------

### Core

### Harmonization

### Bots
#### Collectors

#### Parsers
- `bots.parsers.shadowserver`: if required fields do not exist in data, an exception is raised, so the line will be dumped and not further processed.

#### Experts
- Reverse DNS Expert: ignore all invalid results and use first valid one (#1264).

#### Outputs

### Documentation
- Bots: document redis cache parameters.

### Packaging

### Tests
- `intelmqctl list` now sorts the output of bots and queues (#1262).

### Contrib

### Known issues


1.0.5 Bugfix release (2018-06-21)
---------------------------------

### Core
- `lib/message`: `Report()` can now create a Report instance from Event instances (#1225).
- `lib/bot`:
  * The first word in the log line `Processed ... messages since last logging.` is now adaptable and set to `Forwarded` in the existing filtering bots (#1237).
  * Kills oneself again after proper shutdown if the bot is XMPP collector or output (#970). Previously these two bots needed two stop commands to get actually stopped.
- `lib/utils`: log: set the name of the `py.warnings` logger to the bot name (#1184).

### Harmonization
- Added new types `unauthorized-command` and `unauthorized-login` to `intrusions` taxonomy.

### Bots
#### Collectors
- `bots.collectors.mail.collector_mail_url`: handle empty downloaded reports (#988).
- `bots.collectos.file.collector_file`: handle empty files (#1244).

#### Parsers
- Shadowserver parser:
  * SSL FREAK: Remove optional column `device_serial` and add several new ones.
  * Fixed HTTP URL parsing for multiple feeds (#1243).
- Spamhaus CERT parser:
  * add support for `smtpauth`, `l_spamlink`, `pop`, `imap`, `rdp`, `smb`, `iotscan`, `proxyget`, `iotmicrosoftds`, `automatedtest`, `ioturl`, `iotmirai`, `iotcmd`, `iotlogin` and `iotuser` (#1254).
  * fix `extra.destination.local_port` -> `extra.source.local_port`.

#### Experts
- `bots.experts.filter`: Pre-compile regex at bot initialization.

### Tests
- Ensure that the bots did process all messages (#291).

### Tools
- `intelmqctl`:
  * `intelmqctl run` has a new parameter `-l` `--loglevel` to overwrite the log level for the run (#1075).
  * `intelmqctl run [bot-id] mesage send` can now send report messages (#1077).
- `intelmqdump`:
  * has now command completion for bot names, actions and queue names in interactive console.
  * automatically converts messages from events to reports if the queue the message is being restored to is the source queue of a parser (#1225).
  * is now capable to read messages in dumps that are dictionaries as opposed to serialized dicts as strings and does not convert them in the show command (#1256).
  * truncated messages are no longer used/saved to the file after being shown (#1255).
  * now again denies recovery of dumps if the corresponding bot is running. The check was broken (#1258).
  * now sorts the dump by the time of the dump. Previously, the list was in random order (#1020).

### Known issues
no known issues


1.0.4 Bugfix release (2018-04-20)
---------------------------------
- make code style compatible to pycodestyle 2.4.0
- fixed permissions of some files (they were executable but shouldn't be)

### Core
- lib/harmonization:
  * FQDN validation now handles None correctly (raised an Exception).
  * Fixed several sanitize() methods, the generic sanitation method were called by is_valid, not the sanitize methods (#1219).

### Bots
* Use the new pypi website at https://pypi.org/ everywhere.

#### Parsers
- Shadowserver parser:
  * The fields `url` and `http_url` now handle HTTP URL paths and HTTP requests for all feeds (#1204).
  * The conversion function `validate_fqdn` now handles empty strings correctly.
  * Feed 'drone (hadoop)':
    * Correct validation of field `cc_dns`, will now only be added as `destination.fqdn` if correct FQDN, otherwise ignored. Previously this field could be saved in extra containing an IP address.
    * Adding more mappings for added columns.
  * Added feeds:
    * Drone-Brute-Force
    * IPv6-Sinkhole-HTTP-Drone
  * A lot of newly added fields and fixed conversions.
  * Optional fields can now use one column multiple times.
  * Add newly added columns of `Ssl-Scan` feed to parser
- Spamhaus CERT parser:
  * fix parsing and classification for bot names 'openrelay', 'iotrdp', 'sshauth', 'telnetauth', 'iotcmd', 'iotuser', 'wpscanner', 'w_wplogin', 'iotscan'
    see the NEWS file - Postgresql section - for all changes.
- CleanMX phishing parser: handle FQDNs in IP column (#1162).

#### Experts
- `bots.experts.ripencc_abuse_contact`: Add existing parameter `mode` to BOTS file.

### Tools
- intelmqctl check: Fixed and extended message for 'run_mode' check.
- `intelmqctl start` botnet. When using `--type json`, no non-JSON information about wrong bots are output because that would confuse eg. intelmq-manager

### Tests
- lib/bot: No dumps will be written during tests (#934).
- lib/test: Expand regular expression on python version to match pre-releases (debian testing).

### Packaging
* Static data is now included in source tarballs, development files are excluded

### Known issues
- `bots.collectors/outputs.xmpp` must be killed two times (#970).
- When running bots with `intelmqctl run [bot-id]` the log level is always INFO (#1075).
- `intelmqctl run [bot-id] message send [msg]` does only support Events, not Reports (#1077).
- A warning issued by the python warnings module is logged without the bot-id (#1184).


1.0.3 Bugfix release (2018-02-05)
---------------------------------
### Contrib
* logrotate: use sudo for postrotate script
* cron-jobs: use the scripts in the bots' directories and link them (#1056, #1142)

### Core
- `lib.harmonization`: Handle idna encoding error in FQDN sanitation (#1175, #1176).
- `lib.bot`:
  - Bots stop when redis gives the error "OOM command not allowed when used memory > 'maxmemory'." (#1138).
  - warnings of bots are catched by the logger (#1074, #1113).
  - Fixed exitcodes 0 for graceful shutdowns .
  - better handling of problems with pipeline and especially it's initialization (#1178).
  - All parsers using `ParserBot`'s methods now log the sum of successfully parsed and failed lines at the end of each run (#1161).

### Harmonization
- Rule for harmonization keys is enforced (#1104, #1141).
- New allowed values for `classification.type`: `tor` & `leak` (see n6 parser below ).

### Bots
#### Collectors
- `bots.collectors.mail.collector_mail_attach`: Support attachment file parsing for imbox versions newer than 0.9.5 (#1134).
- `bots.outputs.smtp.output`: Fix STARTTLS, threw an exception (#1152, #1153).

#### Parsers
- All CSV parsers ignore NULL-bytes now, because the csv-library cannot handle it (#967, #1114).
- `bots.experts.modify` default ruleset: changed conficker rule to catch more spellings.
- `bots.parsers.shadowserver.parser`: Add Accessible Cisco Smart Install (#1122).
- `bots.parsers.cleanmx.parser`: Handle new columns `first` and `last`, rewritten for XML feed. See NEWS.md for upgrade instructions (#1131, #1136, #1163).
- `bots.parsers.n6.parser`: Fix classification mappings. See NEWS file for changes values (#738, #1127).

### Documentation
- `Release.md` add release procedure documentation
- `Bots.md`: fix example configuration for modify expert

### Tools
- intelmqctl now exits with exit codes > 0 when errors happened or the operation was not successful. Also, the status operation exits with 1, if bots are stopped, but enabled. (#977, #1143)
- `intelmctl check` checks for valid `run_mode` in runtime configuration (#1140).

### Tests
- `tests.lib.test_pipeline`: Redis tests clear all queues before and after tests (#1086).
- Repaired debian package build on travis (#1169).
- Warnings are not allowed by default, an allowed count can be specified (#1129).
- `tests.bots.experts.cymru_whois/abusix`: Skipped on travis because of ongoing problems.

### Packaging
* cron jobs: fix paths of executables

### Known issues
- `bots.collectors/outputs.xmpp` must be killed two times (#970).
- When running bots with `intelmqctl run [bot-id]` the log level is always INFO (#1075).
- `intelmqctl run [bot-id] message send [msg]` does only support Events, not Reports (#1077).
- `python3 setup.py sdist` does not include static files in the resulting tarballs (#1146).
- `bots.parsers.cleanmx.parser`: The cleanMX feed may have FQDNs as IPs in rare cases, such lines are dumped (#1162).

1.0.2 Bugfix release (2017-11-09)
---------------------------------

### Core
- `lib.message.add`: parameter force has finally been removed, should have been gone in 1.0.0.rc1 already

### Bots
- `collectors.mail.collector_mail_url`: Fix bug which prevented marking emails seen due to disconnects from server (#852).
- `parsers.spamhaus.parser_cert`: Handle/ignore 'AS?' in feed (#1111)

### Packaging
- The following changes have been in effect for the built packages already since version 1.0.0
- Support building for more distributions, now supported: CentOS 7, Debian 8 and 9, Fedora 25 and 26, RHEL 7, openSUSE Leap 42.2 and 42.3 and Tumbleweed, Ubuntu 14.04 and 16.04
- Use LSB-paths for created packages (/etc/intelmq/, /var/lib/intelmq/, /run/intelmq/) (#470). Does does not affect installations with setuptools/pip.
- Change the debian package format from native to quilt
- Fix problems in postint and postrm scripts
- Use systemd-tmpfile for creation of /run/intelmq/

### Documentation
- Add disclaimer on maxmind database in bot documentation and code and the cron-job (#1110)

1.0.1 Bugfix release (2017-08-30)
---------------------------------
### Documentation
- Feeds: use more https:// URLs
- minor fixes

### Bots
- bots/experts/ripencc_abuse_contact/expert.py: Use HTTPS URLs for rest.db.ripe.net
- bots/outputs/file/output.py: properly close the file handle on shutdown
- bots/parser/shadowserver: If conversion of a value via conversion function fails, only log the function name, not the representation string (#1157).

### Core
- lib/bot: Bots will now log the used intelmq version at startup

### Tools
- intelmqctl: To check the status of a bot, the command line of the running process is compared to the actual executable of the bot. Otherwise unrelated programs with the same PID are detected as running bot.
- intelmqctl: enable, disable, check, clear now support the JSON output

1.0.0 Stable release (2017-08-04)
---------------------------------
### Core
- Fixes a thrown FileNotFound exception when stopping bots started with `intelmqctl run ...`

### Harmonization
- leading dots in FQDNs are rejected and removed in sanitation (#1022, #1030)

### Bots
- shadowserver parser Accessible-SMB: smb_implant is converted to bool

1.0.0.rc1 Release candidate (2017-07-05)
----------------------------------------
### Core
- Changing the value of an existing field to `None` deletes the field.
- `Message.update` now behaves like `dict.update`. The old behavior is implemented in `Message.change`
- Deprecated `http_ssl_proxy` has been dropped, use `https_proxy` instead
- Deprecated `http_timeout` has been dropped, use `http_timeout_sec` instead
- Deprecated parameters force and ignore of `Message.add` have been removed
- Deprecated method `Message.contains` has been removed
- Drop support for deprecated configuration files `startup.conf` and `system.conf`

### Development
- We are now testing with and without optional libraries/lowest recommended versions and most current versions of required libraries
- Tests shadowserver with more data and checks for warnings and errors
- Tests: if bots log warnings this counts as failure if not allowed explicitly
- Tests: Bot preparation can be skipped

### Documentation
- The branching/releasing mechanism has been documented

### Bots
#### Collectors
- HTTP collectors: If http_username and http_password are both given and empty or null, 'None:None' has been used to authenticate. It is now checked that the username evaluates to non-false/null before adding the authentication. (fixes #1017)
- Dropped unmaintained and undocumented FTP(S) collectors `bots.collectors.ftp`. Also, the FTPS collector had a license conflict (#842).
- `bots.collectors.http.collector_http_stream`: drop deprecated parameter `url` in favor of `http_url`

#### Parsers
- Removed bots.parsers.openbl as the source is offline since end of may (#1018, https://twitter.com/sshblorg/status/854669263671615489)
- Removed bots.parsers.proxyspy as the source is offline (#1031)
- Shadowserver: Added Accessible SMB
- `bots.experts.ripencc_abuse_contact` now has the two additional parameters `query_ripe_stat_asn` and `query_ripe_stat_ip`.
  Deprecated parameter `query_ripe_stat`. New parameter `mode`.
- `bots.experts.certat_contact` has been renamed to `bots.experts.national_cert_contact_certat` (#995)
- `bots.experts.cymru_whois` ignores registry `other` (#996)
- `bots.parsers.alienvault.parser_otx`: handle timestamps without floating point seconds

### Experts
- bots.experts.deduplicator: New parameter `bypass` to deactivate deduplication, default: False

v1.0.0.dev8 Beta release (2017-06-14)
-------------------------------------

### General changes
- It's now configurable how often the bots are logging how much events they have sent, based on both the amount and time. (fixes #743)
- switch from pycodestyle to pep8

### Configuration
- Added `log_processed_messages_count` (500) and `log_processed_messages_seconds` (900) to defaults.conf.
- `http_timeout` has been renamed to `http_timeout_sec` and `http_timeout_max_tries` has been added.
   This setting is honored by bots.collectors.http.* and bots.collectors.mail.collector_mail_url, bots.collectors.rt (only `http_timeout_sec`), bots.outputs.restapi.output and bots.experts.ripencc_abuse_contact

### Documentation
- Minor fixes
- Dropped install scripts, see INSTALL.md for more detailed instructions and explanations
- Better structure of INSTALL.md
- Better documentation of packages

### Tools
- added a bot debugger (https://github.com/certtools/intelmq/pull/975)
- missing bot executable is detected and handled by intelmqctl (https://github.com/certtools/intelmq/pull/979)

### Core
- fix bug which prevented dumps to be written if the file did not exist (https://github.com/certtools/intelmq/pull/986)
- Fix reload of bots regarding logging
- type annotations for all core libraries

### Bots
- added bots.experts.idea, bots.outputs.files
- possibility to split large csv Reports into Chunks, currently possible for mail url and file collector
- elasticsearch output supports HTTP Basic Auth
- bots.collectors.mail.collector_mail_url and bots collectors.file.collector can split large reports (https://github.com/certtools/intelmq/pull/680)
- bots.parsers.shadowserver support the VNC feed
- handling of HTTP timeouts, see above https://github.com/certtools/intelmq/pull/859
- bots.parsers.bambenek saves the malware name
- bots.parsers.fraunhofer.parser_dga saves the malware name
- bots.parsers.shadowserver handles NULL bytes
- bots.parsers.abusech.parser_ransomware handles the IP 0.0.0.0 specially

### Harmonization
- New field named `output` to support export to foreign formats

v1.0.0.dev7 Beta release (2017-05-09)
-------------------------------------

### Documentation
- more verbose installation and upgrade instructions

### Bot changes
- added bots.experts.field_reducer, bots.outputs.smtp
- bots.collectors.alienvault_otx: OTX library has been removed, install it as package instead
- bots.experts.deduplicator: `ignore_keys` has been renamed to `filter_keys` and `filter_type` has been removed.
- bots.experts.modify: The configration is now list-based for a consistent ordering
- bots.experts.tor_node as an optional parameter `overwrite`
- API keys will be removed from feed.url if possible

### Harmonization
- New parameter and field named feed.documentation to link to documentation of the feed
- classification.taxonomy is lower case only

v1.0.0.dev6 Beta release (2017-01-11)
-------------------------------------

Changes between 0.9 and 1.0.0.dev6

### General changes
- Dropped support for Python 2, Python >= 3.3 is needed
- Dropped startup.conf and system.conf. Sections in BOTS can be copied directly to runtime.conf now.
- Support two run modes: 'stream' which is the current implementation and a new one 'scheduled' which allows scheduling via cron or systemd.
- Helper classes for parser bots
- moved intelmq/conf to intelmq/etc
- cleanup in code and repository
- All bots capable of reloading on SIGHUP
- packages
- pip wheel format instead of eggs
- unittests for library and bots
- bots/BOTS now contains only generic and specific collectors. For a list of feeds, see docs/Feeds.md

### executables
- DEV: intelmq_gen_harm_docs: added to generate Harmonization documentation
- intelmq_psql_initdb: creates a table for a postgresql database using the harmonization fields
- intelmqctl: reworked argument parsing, many bugfixes
- intelmqdump: added to inspect dumped messages and reinsert them into the queues
- DEV: rewrite_config_files: added to rewrite configuration files with consistent style


### Bot changes
#### Collectors
- added alienvault, alienvault otx, bitsight, blueiv, file, ftp, misp, n6, rtir, xmpp collector
- removed hpfeeds collector
- removed microsoft DCU collector
- renamed and reworked URL collector to HTTP
- reworked Mail collectors

#### Parsers
- source specific parsers added: abusech, alienvault, alienvault otx, anubisnetworks, autoshun, bambenek, bitcash, bitsight, blocklistde, blueliv, ci army, cleanmx, cymru_full_bogons, danger_rulez, dataplane, dshield (asn, block and domain), dyn, fraunhofer_dga, hphosts, malc0de, malwaredomains, misp, n6, netlab_360, nothink, openphish, proxyspy, spamhaus cert, taichung, turris, urlvir
- generic parsers added: csv, json
- specific parsers dropped: abusehelper (broken), arbor (source unavailable), bruteforceblocker, certeu, dragonresearchgroup parser (discontinued), hpfeeds, microsoft_dcu (broken), taichungcitynetflow, torexitnode parser
- renamed intelmq.bots.parsers.spamhaus.parser to intelmq.bots.parsers.spamhaus.parser_drop
  renamed intelmq.bots.parsers.malwarepatrol.parser-dansguardian to intelmq.bots.parsers.malwarepatrol.parser_dansguardian
- renamed intelmq.bots.parsers.taichungcitynetflow.parser to intelmq.bots.parsers.taichung.parser
- major rework of shadowserver parsers
- enhanced all parsers

#### Experts
- Added experts: asnlookup, cert.at contact lookup, filter, generic db lookup, gethostbyname, modify, reverse dns, rfc1918, tor_nodes, url2fqdn
- removed experts: contactdb, countrycodefilter (obsolete), sanitizer (obsolete)
- renamed intelmq.bots.expers.abusix.abusix to bots.expers.abusix.expert
  intelmq.bots.experts.asnlookup.asnlookup to intelmq.bots.experts.asn_lookup.expert
  intelmq.bots.experts.cymru.expert to intelmq.bots.experts.cymru_whois.expert
  intelmq.bots.experts.deduplicator.deduplicator to intelmq.bots.experts.deduplicator.expert
  intelmq.bots.experts.geoip.geopip to intelmq.bots.experts.maxmind_geoip.expert
  intelmq.bots.experts.ripencc.ripencc to intelmq.bots.experts.ripencc_abuse_contact.expert
  intelmq.bots.experts.taxonomy.taxonomy to intelmq.bots.experts.taxonomy.expert
- enhanced all experts
- changed configuration syntax for bots.experts.modify to a more simple variant

#### Outputs
- added: amqp, elasticsearch, redis, restapi, smtp, stomp, tcp, udp, xmpp
- removed: debug, intelmqmailer (broken), logcollector
- enhanced all outputs

### Bug fixes
- FIX: all bots handle message which are None
- FIX: various encoding issues resolved in core and bots
- FIX: time.observation is generated in collectors, not in parsers

### Other enhancements and changes
- TST: testing framework for core and tests. Newly introduced components should always come with proper unit tests.
- ENH: intelmqctl has shortcut parameters and can clear queues
- STY: code obeys PEP8, new code should always be properly formatted
- DOC: Updated user and dev guide
- Removed Message.contains, Message.update methods Message.add ignore parameter

### Configuration
- ENH: New parameter and field named accuracy to represent the accuracy of each feed
- Consistent naming "overwrite" to switch overwriting capabilities of bots (as opposed to override)
- Renamed `http_ssl_proxy` to `https_proxy`
- parameter `hierarchical_output` for many output bots
- deduplicator bot has a new required parameter to configure deduplication mode `filter_type`
- deduplicator bot key ignore_keys was renamed to filter_keys
- The tor_nodes expert has a new parameter `overwrite`, which is by default `false`.

### Harmonization
- ENH: Additional data types: integer, float and Boolean
- ENH: Added descriptions and matching types to all fields
- DOC: harmonization documentation has same fields as configuration, docs are generated from configuration
- BUG: FQDNs are only allowed in IDN representation
- ENH: Removed UUID Type (duplicate of String)
- ENH: New type LowercaseString and UppercaseString, doing automatic conversion
- ENH: Removed UUID Type (duplicate of String)
- ENH: FQDNs are converted to lowercase
- ENH: regex, iregex and length checks when data is added to messages

#### Most important changes:
- `(source|destination).bgp_prefix` is now `(source|destination).network`
- `(source|destination).cc` is now `(source|destination).geolocation.cc`
- `(source|destination).reverse_domain_name` is `(source|destination).reverse_dns`
- `(source|destination).abuse_contact` is lower case only
- `misp_id` changed to `misp.event_uuid`
- `protocol.transport` added, a fixed list of values is allowed
- `protocol.application` is lower case only
- `webshot_url` is now `screenshot_url`
- `additional_information` renamed to `extra`, must be JSON
- `os.name`, `os.version`, `user_agent` removed in favor of `extra`
- all hashes are lower case only
- added `malware.hash.(md5|sha1|sha256)`, removed `malware.hash`
- New parameter and field named feed.accuracy to represent the accuracy of each feed
- New parameter and field named feed.provider to document the name of the source of each feed
- New field `classification.identifier`
-`classification.taxonomy` is now lower case only

### Known issues
- Harmonization: hashes are not normalized and classified, see also issue #394 and pull #634

### Contrib
- ansible and vagrant scripts added
- bash-completion for shells add
- cron job scripts to update lookup data added
- logcheck example rules added
- logrotate configuration added


2016/06/18
----------

* improvements in pipeline:
  - PipelineFactory to give possibility to easily add a new broker (Redis, ZMQ, etc..)
  - Splitter feature: if this option is enable, will split the events in source queue to multiple destination queues
* add different messages support:
  - the system is flexible to define a new type of message like 'tweet' without change anything in bot.py, pipeline.py. Just need to add a new class in message.py and harmonization.conf
* add harmonization support
  - in harmonization.conf is possible to define the fields of a specific message in json format.
  - the harmonization.py has data types witch contains sanitize and validation methods that will make sure that the values are correct to be part of an event.
* Error Handling
 - multiple parameters in configuration which gives possibility to define how bot will handle some errors. Example of parameters:
   - `error_procedure` - retry or pass in case of error
   - `error_retry_delay` - time in seconds to retry
   - `error_max_retries` - number of retries
   - `error_log_message` - log or not the message in error log
   - `error_log_exception` - log or not the exception in error log
   - `error_dump_message` - log or not the message in dump log to be fixed and re-insert in pipeline
* Exceptions
  - custom exceptions for IntelMQ
* Defaults configurations
  - new configuration file to specify the default parameters which will be applied to all bots. Bots can overwrite the configurations.
* New bots/feeds


2015/06/03 (aaron)
------------------

* fixed the license to AGPL in setup.py
* moved back the documentation from the wiki repo to `docs/`. See #205.
* added python-zmq as a setup requirement in UserGuide . See #206
