CHANGELOG
==========


2.1.0 (unreleased)
-----------------

### Configuration

### Core
- `intelmq.lib.harmonization`:
  - Use correct parent classes.
  - Add `DateTime.convert` as interface for all existing conversion functions.
  - add `DateTime.convert_from_format`.
  - add `DateTime.convert_from_format_midnight`.
  - add `DateTime.convert_fuzzy`.
- `intelmq.lib.pipeline`:
  - Redis: Use single connection client if calling bot is not multithreaded. Gives a small speed advantage.
  - Require the bot instance as parameter for all pipeline classes.
  - New internal variable `_has_message` to keep the state of the pipeline.
  - Split receive and acknowledge into public-facing and private methods.
  - Add `reject_message` method to the Pipeline class for explicit requeue of messages.
- `intelmq.lib.bot`:
  - Log message after successful bot initialization, no log message anymore for ready pipeline.
  - Use existing current message if receive is called and the current message still exists.
  - Fix handling of received messaged after a sighup that happend during a blocking receving connection using explicit rejection (#1438).
- `intelmq.lib.test`:
  - Fix the tests broker by providing the testing pipeline.
- `intelmq.lib.utils`:
  - `unzip`:
    - new parameter `return_names` to optionally return the file names.
    - support for zip
    - new parameters `try_zip`, `try_gzip` and `try_tar` to control which compressions are tried.
    - rewritten to an iterative approach

### Development

### Harmonization
- Add extra to reports.

### Bots
#### Collectors
- `intelmq.bots.collectors.http.collector_http`:
  - More extensive usage of `intelmq.lib.utils.unzip`.
  - Save the file names in the report if files have been extracted form an archive.
- `intelmq.bots.collectors.rt.collector_rt`: Save ticket information/metadata in the extra fields of the report.
  - Support for RT 3.8 and RT 4.4.
- `intelmq.bots.collectos.mail.*`: Save email information/metadata in the extra fields of the report.

#### Parsers
- `intelmq.bot.parsers.html_table.parser`:
  * New parameter "html_parser".
  * Use time conversion functions directly from `intelmq.lib.harmonization.DateTime.convert`.
  - Limit lxml dependency on 3.4 to < 4.4.0 (incompatibility).
- `intelmq.bots.parsers.netlab_360.parser`: Add support for hajime scanners.

#### Experts
- Add geohash expert.
- `intelmq.bot.experts.generic_db_lookup.expert`
    * got required parameter "engine"
    * engine can be set to "postgresql" to drop-in replacement for previous functionality
    * can be set to sqlite to search via this engine

#### Outputs
- `intelmq.bot.outputs.postgresql.output`
    * renamed to SQL (`intelmq.bot.outputs.sql.output`)
    * got required parameter "engine" 
    * engine can be set to "postgresql" to drop-in replacement for previous functionality
    * can be set to sqlite to output via this engine 
    * The previous module is a compatibility shim and will be available in the 2.x series.

### Documentation
- Feeds: Add ViriBack feed.
- `intelmq.tests.bots.outputs.amqptopic.test_output`: Added.

### Packaging

### Tests
- Travis:
  - Use UTC timezone.
- Tests for `utils.unzip`.
- Add a new asset: Zip archive with two files, same as with tar.gz archive.

### Tools
- intelmqctl:
  - Use green and red text color for some interactive output to indicate obvious errors or the absence of them.
- intelmqdump:
  - New edit action `v` to modify a message saved in the dump (#1284).

### Contrib
* malware name mapping:
  * Add support for MISP treat actors data, see it's README for more information.
    * And handle empty synonyms in misp's galxies data.
  * Move apply-Script to the new EventDB directory
* EventDB: Scripts for applying malware name mapping and domain suffixes to an EventDB.

### Known issues

2.0.2 (unreleased)
-----------------

### Configuration

### Core

### Development

### Harmonization

### Bots
#### Collectors
- `intelmq.bots.collectors.api.collector_api`:
  - Handle non-existing IO loop in shutdown.
  - Close socket on shutdown, fixes reloading.
  - Marked as non-threadable.

#### Parsers

#### Experts

#### Outputs

### Documentation

### Packaging
- Rules:
  - Exclude intelmqsetup tool in packages
  - Include update-rfiprisk-data in packages

### Tests

### Tools
- intelmqctl:
  - More and more precise logging messages for botnet starting and restarting, enable and disable.
  - No error message for disabled bots on botnet reload.
  - Fix `upgrade-conf` is state file is empty or not existing.

### Contrib
- Check MK Statistics Cronjob:
  - Use `statistics_*` parameters.
  - Make file executable

### Known issues


2.0.1 (2019-08-23)
------------------

### Core
- `intelmq.lib.harmonization`:
  - `IPAddress`: Remove Scope/Zone IDs for IPv6 addresses in sanitation.
  - All types: Handle `None` for validation and sanitation gracefully.
- `intelmq.lib.bot`:
  - fix parameters of ParserBot and CollectorBot constructors, allowing `intelmqctl run` with these bots again (#1414).
  - Also run `rate_limit` after retry counter reset (#1431).
- `__version_info__`:
  - is now available in the top level module.
  - uses integer values now instead of strings for numerical version parts
- Also provide (empty) `ROOT_DIR` for non-pip installations.
- `intelmq.lib.upgrades`: New library file `upgrades` with upgrade functions.
- `intelmq.lib.utils`:
  - New function `setup_list_logging` for intelmqctl check an possibly others.
    - Fix return values (#1423).
  - New function `version_smaller` for version comparisons.
  - New function `lazy_int` for version conversions.
  - `parse_logline`: Handle thread IDs.
  - `log` takes a new argument `logging_level_stream` for the logging level of the console handler.
  - New constant `LOG_FORMAT_SIMPLE`, used by intelmqctl.
  - New function `write_configuration` to write dicts to files in the correct json formatting.
  - New function `create_request_session_from_bot`.
- `intelmq.lib.pipeline`:
  - AMQP:
    - Actually use `source/destination_pipeline_amqp_virtual_host` parameter.
    - Support for SSL with `source/destination_pipeline_ssl` parameter.
  - pipeline base class: add missing dummy methods.
  - Add missing return types.
  - Redis: Evaluate return parameter of queue/key deletion.
- Variable `STATE_FILE_PATH` added.

### Development
- `intelmq.bin.intelmq_gen_docs`: For yaml use `safe_load` instead of unsafe `load`.

### Harmonization
- IPAddress type: Remove Scope/Zone IDs for IPv6 addresses in sanitation.
- TLP: Sanitation handles now more cases: case-insensitive prefixes and arbitrary whitespace between the prefix and the value (#1420).

### Bots
#### Collectors
- `intelmq.bots.collectors.http.collector_http`: Use `utils.create_request_session_from_bot`.
- `intelmq.bots.collectors.http.collector_http_stream`: Use `utils.create_request_session_from_bot` and thus fix some retries on connection timeouts.
- `intelmq.bots.collectors.mail.collector_mail_url`: Use `utils.create_request_session_from_bot`.
- `intelmq.bots.collectors.microsoft.collector_interflow`: Use `utils.create_request_session_from_bot` and thus fix retries on connection timeouts.
- `intelmq.bots.collectors.rt.collector_rt`: Use `utils.create_request_session_from_bot` and thus fix retries on connection timeouts.
- `intelmq.bots.collectors.twitter.collector_twitter`: Use `utils.create_request_session_from_bot` and thus fix retries on connection timeouts for non-twitter connections.

#### Parsers
- `intelmq.bots.parsers.n6.parser_n6stomp`: use `malware-generic` instead of `generic-n6-drone` for unknown infected system events.
- `intelmq.bots.parsers.abusech.parser_ip`: Support LastOnline column in feodo feed (#1400) and use it for `time.source` if available.
  - Use lower case malware names as default, should not make a difference in practice.
  - Fix handling of CSV header for feodotracker (#1417, #1418).
- `intelmq.bots.parsers.netlab_360.parser`: Detect feeds with `https://` too.

#### Experts
- `intelmq.bots.experts.generic_db_lookup`: Recommend psycopg2-binary package.
- `intelmq.bots.experts.modify.expert`:
  - Compile regular expressions (all string rules) at initialization, improves the speed.
  - Warn about old configuration style deprecation.
- `intelmq.bots.experts.do_portal.expert`:
  - Use `utils.create_request_session_from_bot` and thus fix retries on connection timeouts (#1432).
  - Treat "502 Bad Gateway" as timeout which can be retried.
- `intelmq.bots.experts.ripe.expert`: Use `utils.create_request_session_from_bot` and thus fix retries on connection timeouts.
- `intelmq.bots.experts.url2fqdn.expert`: Support for IP addresses in hostnames (#1416).
- `intelmq.bots.experts.national_cert_contact_certat.expert`: Use `utils.create_request_session_from_bot` and thus fix retries on connection timeouts.

#### Outputs
- `intelmq.bots.outputs.postgresql`: Recommend psycopg2-binary package.
- `intelmq.bots.outputs.amqptopic`:
  - Shutdown: Close connection only if connection exists.
  - Add support for pika > 1. Pika changed the way it indicates (Non-)Acknowledgments of sent messages.
  - Gracefully handle unroutable messages and give advice.
  - Support for connections without authentication.
  - Replace deprecated parameter `type` with `exchange_type` for `exchange_declare`, supporting pika >= 0.11 (#1425).
  - New parameters `message_hierarchical_output`, `message_with_type`, `message_jsondict_as_string`.
  - New parameter `use_ssl` for SSL connections.
  - New parameter `single_key` for sending single fields instead of the full event.
- `intelmq.bots.outputs.mongodb.output`: Support for pymongo >= 3.0.0 (#1063, PR#1421).
- `intelmq.bots.outputs.file`: `time.*` field serialization: support for microseconds.
- `intelmq.bots.outputs.mongodb.output`: Support for authentication in pymongo >= 3.5 (#1062).
- `intelmq.bots.outputs.restapi.output`: Use `utils.create_request_session_from_bot` and thus fix retries on connection timeouts.

### Documentation
- Add certbund-contact to the ecosystem document.
- Rename the IDEA expert to "IDEA Converter".
- Add the new configuration upgrade function to the docs.
- User Guide:
  - Clarify on Uninstallation

### Packaging
- Do not execute the tcp collector tests during debian and ubuntu builds as they fail there.

### Tests
- `intelmq.lib.test`: Disable statistics for test runs of bots.
- `contrib.malware_name_mapping`: Added tests.
- Travis: Also run tests of contrib.

### Tools
- `intelmqsetup`: Only change directory ownerships if necessary.
- `intelmqctl`:
  - Provide new command `upgrade-conf` to uprade configuration to a newer version.
    - Makes backups of configurations files on its own.
    - Also checks for previously skipped or new functions of older versions and catches up.
  - Provides logging level on class layer.
  - Fix `-q` flag for `intelmqctl list queues` by renaming its alternative name to `--non-zero` to avoid a name collision with the global `--quiet` parameter.
  - For console output the string `intelmqctl: ` at the beginning of each line is no longer present.
  - `check`: Support for the state file added. Checks if it exists and all upgrade functions have been executed successfully.
  - Waits for up to 2 seconds when stopping a bot (#1434).
  - Exits early on restart when stopping a bot did not work (#1434).
  - `intelmqctl run process -m` debugging: Mock acknowledge method if incoming message is mocked too, otherwise a different message is acknowledged.
  - Queue listing for AMQP: Support non-default monitoring URLs, see User-Guide.

### Contrib
* logcheck rules: Adapt ignore rule to cover the instance IDs of bot names.
* malware name mapping:
  - Ignore lines in mapping starting with '#'.
  - Optionally include malpedia data.
  - Fix command line parsing for not arguments (#1427).
- bash-completion: Support for `intelmqctl upgrade-config` added.

### Known issues
- http stream collector: retry on regular connection problems? (#1435)
- tests: capture logging with context manager (#1342)
- Bots started with IntelMQ-Manager stop when the webserver is restarted. (#952)
- n6 parser: mapping is modified within each run (#905)
- reverse DNS: Only first record is used (#877)
- Corrupt dump files when interrupted during writing (#870)


2.0.0 (2019-05-22)
------------------

See also the changelog for 2.0.0.beta1 below.

### Configurations
- Defaults: New parameters `statistics_host`, `statistics_port`, `statistics_databasae`, `statistics_password` for statistics redis database (#1402).

### Core
- Add more and fix some existing type annotations.
- `intelmq.lib.bot`:
  - Use `statistics_*` parameters for bot's statistics (#1402).
  - Introduce `collector_empty_process` for collectors with an empty `process()` method, hardcoded 1s minimum sleep time, preventing endless loops, causing high load (#1364).
  - Allow to disable multithreading by initialization parameter, used by intelmqctl / the bot debugger (#1403).
- `intelmq.lib.pipeline`: redis: OOM can also be low memory, add this to log message (#1405).
- `intelmq.lib.harmonization`: ClassificationType: Update RSIT mapping (#1380):
  - replace `botnet drone` with `infected-system`
  - replace `infected system` with `infected-system`
  - replace `ids alert` with `ids-alert`
  - replace `c&c` with `c2server`
  - replace `malware configuration` with `malware-configuration`
  - sanitize replaces these values on the fly
- Allow using non-opt/ (LSB) paths with environment variable `INTELMQ_PATHS_NO_OPT`.
- Disable/disallow threading for all collectors and some other bots.

### Development
- Applied isort to all core files and core-related test files, sorting the imports there (every thing except bots and bots' tests).

### Harmonization
- See the Core section for the changes in the allowed values for `classification.type`.

### Bots
- Use the new RSIT types in several types, see above

#### Parsers
- `intelmq.bots.parsers.spamhaus.parser_cert`: Added support for `extortion` events.

#### Experts
- added `intelmq.bots.experts.do_portal.expert`.

#### Outputs
- `intelmq.bots.outputs.elasticsearch.output`: Support for TLS added (#1406).
- `intelmq.bots.outputs.tcp.output`: Support non-intelmq counterparts again. New parameter `counterpart_is_intelmq`, see NEWS.md for more information (#1385).

### Packaging
- Update IntelMQ path fix patch after `INTELMQ_PATHS_NO_OPT` introduction, provide `INTELMQ_PATHS_OPT` environment variable for packaged instances.

### Tests
- `test_conf`: For yaml use `safe_load` instead of unsafe `load`.
- Travis: Switch distribution from trusty to xenial, adapt scripts.
  - Add Python 3.7 to tests.
- Don't use Cerberus 1.3 because of https://github.com/pyeve/cerberus/issues/489
- Add tests for `intelmqctl.lib.upgrades`.

### Tools
- intelmqdump: Fix creation of pipeline object by providing a logger.
- intelmqctl: Disable multithreading for interactive runs / the bot debugger (#1403).

### Known issues
- tests: capture logging with context manager (#1342)
- pymongo 3.0 deprecates used insert method  (#1063)
- pymongo >= 3.5: authentication changes  (#1062)
- Bots started with IntelMQ-Manager stop when the webserver is restarted. (#952)
- n6 parser: mapping is modified within each run (#905)
- reverse DNS: Only first record is used (#877)
- Corrupt dump files when interrupted during writing (#870)


2.0.0.beta1 (2019-04-10)
------------------------
There are some features considered as beta and marked as such in the documentation, do not use them in production yet.

### Removals of deprecated code:
- Removed compatibility shim `intelmq.bots.collectors.n6.collector_stomp`, use `intelmq.bots.collectors.stomp.collector` instead (see #1124).
- Removed compatibility shim `intelmq.bots.parsers.cymru_full_bogons.parser`, use `intelmq.bots.parsers.cymru.parser_full_bogons` instead.
- Removed compatibility shim handling deprecated parameter `feed` for collectors. Use `name` instead.
- Removed deprecated and unused method `intelmq.lib.pipeline.Pipeline.sleep`.
- Removed support for deprecated parameter `query_ripe_stat` in `intelmq.bots.experts.ripe.expert`, use `query_ripe_stat_asn` and `query_ripe_stat_ip` instead (#1291).
- Removed deprecated and unused function `intelmq.lib.utils.extract_tar`.

### Core
- `lib/pipeline`:
  - Allow setting the broker of source and destination independently.
  - Support for a new AMQP broker. See User Guide for configuration. (#1179)
- `lib/bot`:
  - Dump messages locks the dump file using unix file locks (#574).
  - Print idle/rate limit time also in human readable format (#1332).
  - `set_request_parameters`: Use `{}` as default proxy value instead of `None`. Allows updating of existing proxy dictionaries.
  - Bots drop privileges if they run as root.
  - Save statistics on successfully and failed processed messages in the redis database 3.
- `lib/utils`
  - Function `unzip` to extract files from gzipped and/or tar-archives.
  - New class `ListHandler`: new handler for logging purpose which saves the messages in a list.
  - Add function `seconds_to_human`.
  - Add function `drop_privileges`.
  - `parse_relative`: Strip string before parsing.
  - `parse_logline`: Do not convert the timestamps to UTC, leave them as is.
- `lib/cache`:
  - Allow ttl to be None explicitly.
  - Overwrite existing cache keys in the database instead of discarding the new data.
- `lib/bot`:
  - Basic, but easy-to-configure multi-threading using python's `threading` library. See the User-Guide for more information (#111, #186).
- `bin/intelmqctl`:
  - Support for Supervisor as process manager (#693, #1360).

### Development
- upgraded all files to python3-only syntax, e.g. use `super()` instead of `super(..., ...)` in all files. Migration from old to new string formatting has not been applied if the resulting code would be longer.

### Bots
#### Collectors
- added `intelmq.bots.parsers.opendxl.collector` (#1265).
- added `intelmq.bots.collectors.api`: collecting data using an HTTP API (#123, #1187).
- added `intelmq.bots.collectors.rsync` (#1286).
- `intelmq.bots.collectors.http.collector_http`:
  - Add support for uncompressing of gzipped-files (#1270).
  - Add time-delta support for time formatted URLs (#1366).
- `intelmq.collectors.blueliv.collector_crimeserver`: Allow setting the API URL by parameter (#1336).
- `intelmq.collectors.mail`:
  - Use internal lib for functionality.
  - Add `intelmq.bots.collectors.mail.collector_mail_body`.
  - Support for `ssl_ca_certificate` parameter (#1362).

#### Parsers
- added `intelmq.bots.parsers.mcafee.parser_atd` (#1265).
- `intelmq.bots.parsers.generic.parser_csv`:
  - New parameter `columns_required` to optionally ignore parse errors for columns.
- added `intelmq.bots.parsers.cert_eu.parser_csv` (#1287).
  - Do not overwrite the local `time.observation` with the data from the feed. The feed's field 'observation time' is now saved in the field `extra.cert_eu_time_observation`.
  - Fix parsing of `asn` (renamed to `source asn`, `source.asn` internally) and handle existing `feed.accuracy` for parsing `confidence`.
  - Update columns and mapping to current (2019-04-02) data.
- added `intelmq.bots.parsers.surbl.surbl`
- added `intelmq.bots.parsers.html_table` (#1381).
- `intelmq.bot.parsers.netlab_360.parser`: Handle empty lines containing blank characters (#1393).
- `intelmq.bots.parsers.n6.parser_n6stomp`: Handle events without IP addresses.
- `intelmq.bots.parsers.cymru.parser_cap_program`: Handle new feed format.
- `intelmq.bots.parsers.shadowserver`:
  - Add support for the `Accessible-FTP` feed (#1391).
- `intelmq.bots.parsers.dataplane.parser`:
  - Fix parse errors and log more context (#1396).
- added `intelmq.bots.parsers.fraunhofer.parser_ddosattack_cnc.py` and `intelmq.bots.parsers.fraunhofer.parser_ddosattack_target.py` (#1373).

#### Experts
- added `intelmq.bots.experts.recordedfuture_iprisk` (#1267).
- added `intelmq.bots.experts.mcafee.expert_mar` (1265).
- renamed `intelmq.bots.experts.ripencc_abuse_contact.expert` to `intelmq.bots.experts.ripe.expert`, compatibility shim will be removed in version 3.0.
  - Added support for geolocation information in ripe expert with a new parameter `query_ripe_stat_geolocation` (#1317).
  - Restructurize the expert and code de-duplicataion (#1384).
  - Handle '?' in geolocation country data (#1384).
- `intelmq.bots.experts.ripe.expert`:
  - Use a requests session (#1363).
  - Set the requests parameters once per session.
- `intelmq.bots.experts.maxmind_geoip.expert`: New parameter `use_registered` to use the registered country (#1344).
- `intelmq.bots.experts.filter.expert`: Support for paths (#1208).

#### Outputs
- added `intelmq.bots.experts.mcafee.output_esm` (1265).
- added `intelmq.bots.outputs.blackhole` (#1279).
- `intelmq.bots.outputs.restapi.expert`:
  - Set the requests parameters once per session.
- `intelmq.bots.outputs.redis`:
  - New parameter `hierarchichal_output` (#1388).
  - New parameter `with_type`.
- `intelmq.bots.outputs.amqptopic.output`: Compatibility with pika 1.0.0 (#1084, #1394).

### Documentation
- added documentation for feeds
  - CyberCrime Tracker
  - Feodo Tracker Latest
- Feeds: Document abuse.ch URLhaus feed (#1379).
- Install and Upgrading: Use `intelmqsetup` tool.
- Added an ecosystem overview document describing related software.

### Tests
- Add tests of AMQP broker.
- Travis: Change the ownership of `/opt/intelmq` to the current user.

### Tools
- `intelmqctl check`: Now uses the new `ListHandler` from utils to handle the logging in JSON output mode.
- `intelmqctl run`: The message that a running bot has been stopped, is not longer a warning, but an informational message. No need to inform sysadmins about this intended behaviour.
- `intelmqdump`: Inspecting dumps locks the dump file using unix file locks (#574).
- `intelmqctl`:
  - After the check if the program runs as root, it tries to drop privileges. Only if this does not work, a warning is shown.
- `intelmqsetup`: New tool for initializing an IntelMQ environment.

### Contrib
- `malware_name_mapping`:
  - Added the script `apply_mapping_eventdb.py` to apply the mapping to an eventdb.
  - Possibility to add local rules using the download tool.
- `check_mk`:
  - Added scripts for monitoring queues and statistics.

### Known issues
- Multi-threaded bots require multiple SIGTERMs (#1403)
- Stats can't be saved with AMQP if redis is password-protected (#1402)
- Update taxonomies to current RSIT and vice-versa (#1380)
- stomp collector bot constantly uses 100% of CPU (#1364)
- tests: capture logging with context manager (#1342)
- Consistent message counter log messages for all kind of bots (#1278)
- pymongo 3.0 deprecates used insert method  (#1063)
- pymongo >= 3.5: authentication changes  (#1062)
- Bots started with IntelMQ-Manager stop when the webserver is restarted. (#952)
- n6 parser: mapping is modified within each run (#905)
- reverse DNS: Only first record is used (#877)
- Corrupt dump files when interrupted during writing (#870)


1.1.2 (2019-03-25)
------------------

### Core
- `intelmq.lib.bot`:
  - `Bot.__handle_sighup`: Handle exceptions in `shutdown` method of bots.

### Harmonization
- FQDN: Disallow `:` in FQDN values to prevent values like '10.0.0.1:8080' (#1235).

### Bots
#### Collectors
- `intelmq.bots.collectors.stomp.collector`
  - Fix name of shutdown method, was ineffective in the past.
  - Ignore `NotConnectedException` errors on disconnect during shutdown.
- `intelmq.bots.collectors.mail.collector_mail_url`: Decode body if it is bytes (#1367).
- `intelmq.bots.collectors.tcp.collector`: Timeout added. More stable version.

#### Parsers
- `intelmq.bots.parsers.shadowserver`:
  - Add support for the `Amplification-DDoS-Victim`, `HTTP-Scanners`, `ICS-Scanners` and `Accessible-Ubiquiti-Discovery-Service` feeds (#1368, #1383)
- `intelmq.bots.parsers.microsoft.parser_ctip`:
  - Workaround for mis-formatted data in `networkdestinationipv4` field (since 2019-03-14).
  - Ignore "hostname" ("destination.fqdn") if it contains invalid data.
- `intelmq.bots.parsers.shodan.parser`:
  - In `minimal_mode`:
    - Fix the parsing, previously only `source.geolocation.cc` and `extra.shodan` was correctly filled with information.
    - Add a `classification.type` = 'other' to all events.
    - Added tests for this mode.
  - Normal mode:
    - Fix the parsing of `timestamp` to `time.source in the normal mode, previously no timezone information has been added and thus every event raised an exception.
    - ISAKMP: Ignore `isakmp.aggressive`, as the content is same as `isakmp` or less.
- `intelmq.bots.parsers.abusech.parser_ip`: Re-structure the bot and support new format of the changed "Feodo Tracker Domains" feed.
- `intelmq.bots.parsers.n6.parser`:
  - Add parsing for fields "confidence", "expires" and "source".
  - Add support for type "bl-other" (category "other").

#### Experts
- `intelmq.bots.experts.sieve.expert`: Fix key definition to allow field names with numbers (`malware.hash.md5`/`sha1`, #1371).

#### Outputs
- `intelmq.bots.outputs.tcp.output`: Timeout added. When no separator used, awaits that every message is acknowledged by a simple "Ok" string to ensure more stability.

### Documentation
- Install: Update operating system versions
- Sieve Expert: Fix `elsif` -> `elif`.
- Rephrase the description of `time.*` fields.
- Feeds: New URL and format of the "Feodo Tracker IPs" feed. "Feodo Tracker Domains" has been discontinued.

### Packaging

### Tests
- Add missing `__init__.py` files in 4 bot's test directories. Previously these tests have never been executed.
- `intelmq.lib.test`: Allow bot test class names with an arbitrary postfix separated by an underscore. E.g. `TestShodanParserBot_minimal`.

### Tools
- intelmqctl:
  - status: Show commandline differences if a program with the expected PID could be found, but they do not match (previous output was `None`).
  - Use logging level from defauls configuration if possible, otherwise intelmq's internal default. Previously, DEBUG was used unconditionally.

### Known issues
- Bots started with IntelMQ-Manager stop when the webserver is restarted (#952).
- stomp collector bot constantly uses 100% of CPU (#1364).


1.1.1 (2019-01-15)
------------------

### Core
- `lib/harmonization.py`: Change `parse_utc_isoformat` of `DateTime` class from private to public (related to #1322).
- `lib/utils.py`: Add new function `object_pair_hook_bots`.
- `lib.bot.py`:
  - `ParserBot`'s method `recover_line_csv` now also handles given `tempdata`.
  - `Bot.acknowledge_message()` deletes `__current_message` to free the memory, saves memory in idling parsers with big reports.
  - `start()`: Warn once per run if `error_dump_message` is set to false.
  - `Bot.start()`, `ParserBot.process()`: If errors happen on bots without destination pipeline, the `on_error` path has been queried and lead to an exception being raised.
  - `start()`: If `error_procedure` is pass and on pipeline errors, the bot retries forever (#1333).
- `lib/message.py`:
  - Fix add('extra', ..., overwrite=True): old extra fields have not been deleted previously (#1335).
  - Do not ignore empty or ignored (as defined in `_IGNORED_VALUES`) values of `extra.*` fields for backwards compatibility (#1335).
- `lib/pipeline.py` (`Redis.receive`): Wait in 1s steps if redis is busy loading its snapshot from disk (#1334).

### Default configuration
- Set `error_dump_message` to true by default in `defaults.conf`.
- Fixed typo in `defaults.conf`: `proccess_manager` -> `process_manager`

### Development
- `bin/rewrite_config_files.py`: Fix ordering of BOTS file (#1327).

### Harmonization
Update allowed classification fields to 2018-09-26 version (#802, #1350, #1380). New values for `classification.type` are per taxonomy:
- Taxonomy 'intrusions':
  - "application-compromise"
  - "burglary"
  - "privileged-account-compromise"
  - "unprivileged-account-compromise"
- Taxonomy 'fraud':
  - "copyright"
  - "masquerade"
  - "unauthorized-use-of-resources"
- Taxonomy 'information content security':
  - "data-loss"
- Taxonomy 'vulnerable':
  - "ddos-amplifier"
  - "information-disclosure"
  - "potentially-unwanted-accessible"
  - "vulnerable-system"
  - "weak-crypto"
- Taxonomy 'availability':
  - "dos"
  - "outage"
  - "sabotage"
- Taxonomy 'abusive-content':
  - "harmful-speech"
  - "violence"
- Taxonomy 'malicious code':
  - "malware-distribution"
- Taxonomy 'information-gathering':
  - "social-engineering"
  - "sniffing"
- Taxonomy 'information content security':
  - "Unauthorised-information-access"
  - "Unauthorised-information-modification"

### Bots
#### Collectors
- `intelmq.bots.collectors.http.collector_http`:
  - Fix parameter name `extract_files` in BOTS (#1331).
  - Fix handling of `extract_files` parameter if the value is an empty string.
  - Handle not installed dependency library `requests` gracefully.
  - Explain `extract_files` parameter in docs and use a sane default in BOTS file.
- `intelmq.bots.collectors.mail.collector_mail_url`:
  - Handle HTTP status codes != 2xx the same as HTTP timeouts: No exception, but graceful handling.
  - Handle HTTP errors (bad status code and timeouts) with `error_procedure` == 'pass' but marking the mail as read and logging the error.
  - Handle not installed dependency library `requests` gracefully.
- `intelmq.bots.collectors.http.collector_http_stream`:
  - Handle not installed dependency library `requests` gracefully.
- `intelmq.bots.collectors.microsoft.collector_interflow`:
  - Handle not installed dependency library `requests` gracefully.
- `intelmq.bots.collectors.rt.collector_rt`:
  - Handle not installed dependency library `requests` gracefully.
- added `intelmq.bots.collectors.shodan.collector_stream` for collecting shodan stream data (#1096).
  - Correctly check the version of the shodan library, it resulted in wrong comparisons with two digit numbers.
- `intelmq.bots.collectors.microsoft.collector_interflow`:
  - Add check if Cache's TTL is big enough compared to `not_older_than` and throw an error otherwise.

#### Parsers
- `intelmq.bots.parsers.misp`: Fix Object attribute (#1318).
- `intelmq.bots.parsers.cymru.parser_cap_program`:
  - Add support for new format (extra data about botnet of 'bots').
  - Handle AS number 0.
- `intelmq.bots.parsers.shadowserver`:
  - Spam URL reports: remove `src_naics`, `src_sic` columns.
  - fix parsing of 'spam' events in ShadowServer's 'Botnet Drone Hadoop' Report (#1271).
  - Add support in parser to ignore some columns in config file by using `False` as intelmq key.
  - Add support for the `Outdated-DNSSEC-Key` and `Outdated-DNSSEC-Key-IPv6` feeds.
  - Add support for the `Accessible-Rsync` feed.
  - Document support for the `Open-LDAP-TCP` feed.
  - Add support for `Accessible-HTTP` and `Open-DB2-Discovery-Service` (#1349).
  - Add support for `Accessible-AFP` (#1351).
  - Add support for `Darknet` (#1353).
- `intelmq.bots.parsers.generic.parser_csv`: If the `skip_header` parameter was set to `True`, the header was not part of the `raw` field as returned by the `recover_line` method. The header is now saved and handled correctly by the fixed recovery method.
- `intelmq.bots.parsers.cleanmx.parser`: Use field `first` instead of `firsttime` for `time.source` (#1329, #1348).
- `intelmq.bots.parsers.twitter.parser`: Support for `url-normalize` >= 1.4.1 and recommend it. Added new optional parameter `default_scheme`, passed to `url-normalize` (#1356).

#### Experts
- `intelmq.bots.experts.national_cert_contact_certat.expert`:
  - Handle not installed dependency library `requests` gracefully.
- `intelmq.bots.experts.ripencc_abuse_contact.expert`:
  - Handle not installed dependency library `requests` gracefully.
- `intelmq.bots.experts.sieve.expert`:
  - check method: Load missing harmonization, caused an error for every check.
  - Add text and more context to error messages.
  - README: Fix 'modify' to 'update' (#1340).
  - Handle empty rules file (#1343).
- `intelmq.bots.experts.idea.expert`: Add mappings for new harmonization `classification.type` values, see above.

#### Outputs
- `intelmq.bots.outputs.redis`:
  - Fix sending password to redis server.
  - Fix for redis-py >= 3.0.0: Convert Event to string explicitly (#1354).
  - Use `Redis` class instead of deprecated `StrictRedis` for redis-py >= 3.0.0 (#1355).
- `intelmq.bots.outputs.mongodb`:
  - New parameter `replacement_char` (default: `'_'`) for non-hierarchical output as dots in key names are not allowed (#1324, #1322).
  - Save value of fields `time.observation` and `time.source` as native datetime object, not as string (#1322).
- `intelmq.bots.outputs.restapi.output`:
  - Handle not installed dependency library `requests` gracefully.

### Documentation
- FAQ
  - Explanation and solution on orphaned queues.
  - Section on how and why to remove `raw` data.
- Add or fix the tables of contents for all documentation files.
- Feeds:
  - Fix Autoshun Feed URL (#1325).
  - Add parameters `name` and `provider` to `intelmq/etc/feeds.yaml`, `docs/Feeds.md` and `intelmq/bots/BOTS` (#1321).
- Add SECURITY.md file.

### Packaging
- Change the maintainer from Sasche Wilde to Sebastian Wagner (#1320).

### Tests
- `intelmq.tests.lib.test_bot`: Skip `test_logging_level_other` on python 3.7 because of unclear behavior related to copies of loggers (#1269).
- `intelmq.tests.bots.collectors.rt.test_collector`: Remove test because the REST interface of the instance has been closed (see also https://github.com/CZ-NIC/python-rt/issues/28).

### Tools
- `intelmqctl check`: Shows more detailed information on orphaned queues.
- `intelmqctl`:
  - Correctly determine the status of bots started with `intelmqctl run`.
  - Fix output of errors during bot status determination, making it compatible to IntelMQ Manager.
  - `check` subcommand: Show bot ID for messages also in JSON output.
  - `run [bot-id] process -m [message]` works also with bots without a configured source pipeline (#1307).

### Contrib
- elasticsearch/elasticmapper: Add tlp field (#1308).
- `feeds-config-generator/intelmq_gen_feeds_conf`:
  - Add parameters to write resulting configuration directly to files (#1321).
  - Handle collector's `feed.name` and `feed.provider` (#1314).

### Known issues
- Bots started with IntelMQ-Manager stop when the webserver is restarted (#952).
- Tests: capture logging with context manager (#1342).
- stomp collector bot constantly uses 100% of CPU (#1364).


1.1.0 (2018-09-05)
------------------
- Support for Python 3.3 has been dropped in IntelMQ and some dependencies of it. Python 3.3 reached its end of life and Python 3.4 or newer is a hard requirement now.
- The list of feeds docs/Feeds.md has now a machine-readable equivalent YAML file in intelmq/etc/feeds.yaml
  A tool to convert from yaml to md has been added.

### Tools
- `intelmq_gen_feeds_docs` addded to bin directory, allows generating the Feeds.md documentation file from feeds.yaml
- `intelmq_gen_docs` merges both `intelmq_gen_feeds_docs` and `intelmq_gen_harm_docs` in one file and automatically updates the documentation files.

#### intelmqctl
- `intelmqctl start` prints the bot's last error messages if the bot failed to start (#1021).
- `intelmqctl start` message "is running" is printed every time. (Until now, it wasn't said when a bot was just starting.)
- `intelmqctl start/stop/restart/reload/status` now has a "--group" flag which allows you to specify the group of the bots that should be influenced by the command.
- `intelmqctl check` checks for defaults.conf completeness if the shipped file from the package can be found.
- `intelmqctl check` shows errors for non-importable bots.
- `intelmqctl list bots -q` only prints the IDs of enabled bots.
- `intelmqctl list queues-and-status` prints both queues and bots statuses (so that it can be used in eg. intelmq-manager).
- `intelmqctl run` parameter for showing a sent message.
- `intelmqctl run` if message is sent to a non-default path, it is printed out.
- `intelmqctl restart` bug fix; returned some half-nonsense, now returns return state of start and stop operation in a list (#1226).
- `intelmqctl check`: New parameter `--no-connections` to prevent the command from making connections e.g. to the redis pipeline.s
- `intelmqctl list queues`: don't display named paths amongst standard queues.
- The process status test failed if the PATH did not include the bot executables and the `which` command failed. Then the proccess's command line could not be compared correctly. The fix warns of this and adds a new status 'unknown' (#1297).


### Contrib
- tool `feeds-config-generator` to automatically generate the collector and parser runtime and pipeline configurations.
- `malware_name_mapping`: Download and convert tool for malware family name mapping has been added.
- Added a systemd script which creates systemd units for bots (#953).
- `contrib/cron-jobs/update-asn-data`, `contrib/cron-jobs/update-geoip-data`, `contrib/cron-jobs/update-tor-nodes`: Errors produce proper output.

### Core
- lib/bot
  - use SIGTERM instead of SIGINT to stop bots (#981).
  - Bots can specify a static method `check(parameters)` which can perform individual checks specific to the bot.
    These functions will be called by `intelmqctl check` if the bot is configured with the given parameters
  - top level bot parameters (description, group, module, name) are exposed as members of the class.
  - The parameter `feed` for collectors is deprecated for 2.0 and has been replaced by the more consistent `name` (#1144).
  - bug: allow path parameter for CollectorBot class.
  - Handle errors better when the logger could not be initialized.
  - `ParserBot`:
    - For the csv parsing methods, `ParserBot.csv_params` is now used for all these methods.
    - `ParserBot.parse_csv_dict` now saves the field names in `ParserBot.csv_fieldnames`.
    - `ParserBot.parse_csv_dict` now saves the raw current line in `ParserBot.current_line`.
    - `ParserBot.recover_line_csv_dict` now uses the raw current line.
- lib/message:
  - Subitems in fields of type `JSONDict` (see below) can be accessed directly. E.g. you can do:
    event['extra.foo'] = 'bar'
    event['extra.foo'] # gives 'bar'
    It is still possible to set and get the field as whole, however this may be removed or changed in the future:
    event['extra'] = '{"foo": "bar"}'
    event['extra'] # gives '{"foo": "bar"}'
    "Old" bots and configurations compatible with 1.0.x do still work.
    Also, the extra field is now properly exploded when exporting events, analogous to all other fields.
    The `in` operator works now for both - the old and the new - behavior.
  - `Message.add`: The parameter `overwrite` accepts now three different values: `True`, `False` and `None` (new).
    True: An existing value will be overwritten
    False: An existing value will not be overwritten (previously an exception has been raised when the value was given).
    None (default): If the value exists an `KeyExists` exception is thrown (previously the same as False).
    This allows shorter code in the bots, as an 'overwrite' configuration parameter can be directly passed to the function.
  - The message class has now the possibility to return a default value for non-existing fields, see `Message.set_default_value`.
  - Message.get behaves the same like `Message.__getitem__` (#1305).
- Add `RewindableFileHandle` to utils making handling of CSV files more easy (optionally)
- lib/pipeline:
  - you may now define more than one destination queues path the bot should pass the message to, see [Pipelines](https://github.com/certtools/intelmq/blob/develop/docs/User-Guide.md#pipeline-configuration) (#1088, #1190).
  - the special path `"_on_error"` can be used to pass messages to different queues in case of processing errors (#1133).
- `lib/harmonization`: Accept `AS` prefix for ASN values (automatically stripped).
- added `intelmq.VAR_STATE_PATH` for variable state data of bots.

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
  - Add proxy support.
  - Fix handling of parameter `countries`.

#### Parsers
- `bots.parsers.shadowserver`:
  - changed feednames. Please refer to it's README for the exact changes.
  - If the conversion function fails for a line, an error is raised and the offending line will be handled according to the error handling configuration.
    Previously errors like these were only logged and ignored otherwise.
  - add support for the feeds
    - `Accessible-Hadoop` (#1231)
    - `Accessible ADB` (#1285)
  - Remove deprecated parameter `override`, use `overwrite` instead (#1071).
  - The `raw` values now are exactly the input with quotes unchanged, the ParserBot methods are now used directly (#1011).
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
  - ignore the invalid IP '0.0.0.0' for the destination
  - fix the raw/dumped messages, did not contain the paling list previously.
  - use the new harmonization field `tlp` instead of `extra.tlp`.
- `bots.parsers.alienvault.parser_otx`: Save TLP data in the new harmonization field `tlp`.
- added `intelmq.bots.parsers.openphish.parser_commercial`
- added `intelmq.bots.parsers.microsoft.parser_bingmurls`
- added `intelmq.bots.parsers.calidog.parser_certstream` for parsing certstream data (#1120).
- added `intelmq.bots.parsers.shodan.parser` for parsing shodan data (#1096).
- change the classification type from 'botnet drone' to 'infected system' in various parses.
- `intelmq.bots.parsers.spamhaus.parser_cert`: Added support for all known bot types.

#### Experts
- Added sieve expert for filtering and modifying events (#1083)
  - capable of distributing the event to appropriate named queues
- `bots.experts.modify`
  - default rulesets: all malware name mappings have been migrated to the [Malware Name Mapping repository](https://github.com/certtools/malware_name_mapping) ruleset. See the new added contrib tool for download and conversion.
  - new parameter `case_sensitive` (default: True)
- Added wait expert for sleeping
- Added domain suffix expert to extract the TLD/Suffix from a domain name.
- `bots.experts.maxmind_geoip`: New (optional) parameter `overwrite`, by default false. The current default was to overwrite!
- `intelmq.bots.experts.ripencc_abuse_contact`:
  - Extend deprecated parameter compatibility `query_ripe_stat` until 2.0 because of a logic bug in the compatibility code, use `query_ripe_stat_asn` and `query_ripe_stat_ip` instead (#1071, #1291).
  - Handle HTTP status code 404 for DB AS queries.
  - Add caching capability.
- `intelmq/bots/experts/asn_lookup/update-asn-data`: Errors produce proper output on stdout/stderr.
- `intelmq/bots/experts/maxmind_geoip/update-geoip-data`: Errors produce proper output on stdout/stderr.
- `intelmq/bots/experts/tor_nodes/update-tor-nodes`: Errors produce proper output on stdout/stderr.

#### Outputs
- `bots.outputs.file`:
  - String formatting can be used for file names with new parameter `format_filename`.
  - New parameter `single_key` to only save one field.
  - New parameter `encoding_errors_mode` with default value `'strict'` to handle encoding errors for the files written.

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
- Developers Guide: Add instructions for pre-release testing.

### Packaging
- Add logcheck configuration to the packages.
- Fix packaging of bash completion script.

### Tests
- Travis now correctly stops if a requirement could not be installed (#1257).
- New tests for validating `etc/feeds.yaml` and `bots/BOTS` using cerberus and schemes are added (#1166).
- New test for checking if `docs/Feeds.md` is up to date with `etc/feeds.yaml`.

### Known bugs
- contrib: feeds-config-generator does not add feed name as parameter (#1314).
- bot debugger requires configured source pipeline (#1307).
- shadowserver parser: drone feed has spam events (#1271).
- debug log level on python 3.7 not applied (#1269).
- `bots.experts.sieve` does not support textX (#1246).
- Bots started with IntelMQ-Manager stop when the webserver is restarted (#952).

1.0.6 Bugfix release (2018-08-31)
---------------------------------

### Bots
#### Collectors
- `bots.collectors.rt.collector_rt`: Log ticket id for downloaded reports.

#### Parsers
- `bots.parsers.shadowserver`:
  - if required fields do not exist in data, an exception is raised, so the line will be dumped and not further processed.
  - fix a bug in the parsing of column `cipher_suite` in ssl poodle reports (#1288).

#### Experts
- Reverse DNS Expert: ignore all invalid results and use first valid one (#1264).
- `intelmq/bots/experts/tor_nodes/update-tor-nodes`: Use check.torproject.org as source as internet2.us is down (#1289).

#### Outputs
- `bots.output.amqptopic`:
  - The default exchange must not be declared (#1295).
  - Unencodable characters are prepended by backslashes by default. Otherwise Unicode characters can't be encoded and sent (#1296).
  - Gracefully close AMQP connection on shutdown of bot.

### Documentation
- Bots: document redis cache parameters.
- Installation documentation: Ubuntu needs universe repositories.

### Packaging
- Dropped support for Ubuntu 17.10, it reached its End of Life as of 2018-07-19.

### Tests
- Drop tests for Python 3.3 for the mode with all requirements, as some optional dependencies do not support Python 3.3 anymore.
- `lib.test`: Add parameter `compare_raw` (default: `True`) to `assertMessageEqual`, to optionally skip the comparison of the raw field.
- Add tests for RT collector.
- Add tests for Shadowserver Parser:
  - SSL Poodle Reports.
  - Helper functions.

### Tools
- `intelmqctl list` now sorts the output of bots and queues (#1262).
- `intelmqctl`: Correctly handle the corner cases with collectors and outputs for getting/sending messages in the bot debugger (#1263).
- `intelmqdump`: fix ordering of dumps in a file in runtime. All operations are applied to a sorted list (#1280).

### Contrib
- `cron-jobs/update-tor-nodes`: Use check.torproject.org as source as internet2.us is down (#1289).

### Known issues
- shadowserver parser: drone feed has spam events (#1271).


1.0.5 Bugfix release (2018-06-21)
---------------------------------

### Core
- `lib/message`: `Report()` can now create a Report instance from Event instances (#1225).
- `lib/bot`:
  - The first word in the log line `Processed ... messages since last logging.` is now adaptable and set to `Forwarded` in the existing filtering bots (#1237).
  - Kills oneself again after proper shutdown if the bot is XMPP collector or output (#970). Previously these two bots needed two stop commands to get actually stopped.
- `lib/utils`: log: set the name of the `py.warnings` logger to the bot name (#1184).

### Harmonization
- Added new types `unauthorized-command` and `unauthorized-login` to `intrusions` taxonomy.

### Bots
#### Collectors
- `bots.collectors.mail.collector_mail_url`: handle empty downloaded reports (#988).
- `bots.collectors.file.collector_file`: handle empty files (#1244).

#### Parsers
- Shadowserver parser:
  - SSL FREAK: Remove optional column `device_serial` and add several new ones.
  - Fixed HTTP URL parsing for multiple feeds (#1243).
- Spamhaus CERT parser:
  - add support for `smtpauth`, `l_spamlink`, `pop`, `imap`, `rdp`, `smb`, `iotscan`, `proxyget`, `iotmicrosoftds`, `automatedtest`, `ioturl`, `iotmirai`, `iotcmd`, `iotlogin` and `iotuser` (#1254).
  - fix `extra.destination.local_port` -> `extra.source.local_port`.

#### Experts
- `bots.experts.filter`: Pre-compile regex at bot initialization.

### Tests
- Ensure that the bots did process all messages (#291).

### Tools
- `intelmqctl`:
  - `intelmqctl run` has a new parameter `-l` `--loglevel` to overwrite the log level for the run (#1075).
  - `intelmqctl run [bot-id] mesage send` can now send report messages (#1077).
- `intelmqdump`:
  - has now command completion for bot names, actions and queue names in interactive console.
  - automatically converts messages from events to reports if the queue the message is being restored to is the source queue of a parser (#1225).
  - is now capable to read messages in dumps that are dictionaries as opposed to serialized dicts as strings and does not convert them in the show command (#1256).
  - truncated messages are no longer used/saved to the file after being shown (#1255).
  - now again denies recovery of dumps if the corresponding bot is running. The check was broken (#1258).
  - now sorts the dump by the time of the dump. Previously, the list was in random order (#1020).

### Known issues
no known issues


1.0.4 Bugfix release (2018-04-20)
---------------------------------
- make code style compatible to pycodestyle 2.4.0
- fixed permissions of some files (they were executable but shouldn't be)

### Core
- lib/harmonization:
  - FQDN validation now handles None correctly (raised an Exception).
  - Fixed several sanitize() methods, the generic sanitation method were called by is_valid, not the sanitize methods (#1219).

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

#### Parsers
- All CSV parsers ignore NULL-bytes now, because the csv-library cannot handle it (#967, #1114).
- `bots.parsers.shadowserver.parser`: Add Accessible Cisco Smart Install (#1122).
- `bots.parsers.cleanmx.parser`: Handle new columns `first` and `last`, rewritten for XML feed. See NEWS.md for upgrade instructions (#1131, #1136, #1163).
- `bots.parsers.n6.parser`: Fix classification mappings. See NEWS file for changes values (#738, #1127).

#### Experts
- `bots.experts.modify` default ruleset: changed conficker rule to catch more spellings.

#### Outputs
- `bots.outputs.smtp.output`: Fix STARTTLS, threw an exception (#1152, #1153).

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

### Bots
#### Collectors
- bots.collectors.alienvault_otx: OTX library has been removed, install it as package instead

#### Parsers
- API keys will be removed from feed.url if possible
- `intelmq.bots.parsers.shadowserver.config`:
  - Added support for Compromised-Website, Open-Netis, NTP-Version, Sandbox-URL, Spam-URL, Vulnerable-ISAKMP, Botnet-CCIP, Accessible-RDP, Open-LDAP, Blacklisted-IP, Accessible-Telnet, Accessible-CWMP (#748).

#### Experts
- added bots.experts.field_reducer, bots.outputs.smtp
- bots.experts.deduplicator: `ignore_keys` has been renamed to `filter_keys` and `filter_type` has been removed.
- bots.experts.modify: The configration is now list-based for a consistent ordering
- bots.experts.tor_node as an optional parameter `overwrite`

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

### Tools
- DEV: intelmq_gen_harm_docs: added to generate Harmonization documentation
- intelmq_psql_initdb: creates a table for a postgresql database using the harmonization fields
- intelmqctl: reworked argument parsing, many bugfixes
- intelmqdump: added to inspect dumped messages and reinsert them into the queues
- DEV: rewrite_config_files: added to rewrite configuration files with consistent style


### Bots
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
