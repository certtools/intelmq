<!-- comment
   SPDX-FileCopyrightText: 2015-2021 Sebastian Wagner
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

CHANGELOG
==========

3.0.2 (2021-09-10)
------------------

### Core
- `intelmq.lib.bot.CollectorBot`: Fixed an issue with within the `new_report` function, which re-loads the harmonization file after a new incoming dataset, which leads to CPU drain and decreased performance (PR#2106 by Sebastian Waldbauer, fixes #2098).
- `intelmq.lib.bot.Bot`: Make private members `__is_multithreadable` and `__collector_empty_process` protected members `_is_multithreadable` and `_collector_empty_process` to make them easily modifiable by Bot classes (PR#2109 by Sebastian Wagner, fixes #2108).
  Also affected and adapted bots by this change are:
  - `intelmq.bots.collectors.api.collector_api`
  - `intelmq.bots.collectors.stomp.collector`
  - `intelmq.bots.experts.splunk_saved_search.expert`
  - `intelmq.bots.experts.threshold.expert`
  - `intelmq.bots.outputs.file.output`
  - `intelmq.bots.outputs.misp.output_api`
  - `intelmq.bots.outputs.misp.output_feed`
  - `intelmq.bots.outputs.tcp.output`
  - `intelmq.bots.outputs.udp.output`
- `intelmq.lib.cache`: Do not create the Cache class if the host is null, allows deactivating the bot statistics (PR#2104 by Sebastian Waldbauer, fixes #2103).

### Bots
#### Experts
- `intelmq.bots.experts.domain_suffix.expert`: Only print skipped database update message if verbose mode is active (PR#2107 by Sebastian Wagner, fixes #2016).

### Documentation
- Add configuration upgrade steps for 3.0 to NEWS (PR#2101 by Sebastian Wagner).

### Known issues
See [open bug reports](https://github.com/certtools/intelmq/issues?q=is%3Aissue+is%3Aopen+label%3Abug) for a more detailed list.
- ParserBot: erroneous raw line recovery in error handling (#1850).


3.0.1 (2021-09-02)
------------------

### Configuration

### Core
- `intelmq.lib.bot_debugger`: Fix accessing the bot's destination queues (PR#2027 by Mikk Margus Möll).
- `intelmq.lib.pipeline`: Fix handling of `load_balance` parameter (PR#2027 by Mikk Margus Möll).
- `intelmq.lib.bot`: Fix handling of parameter `destination_queues` if value is an empty dictionary (PR#2051 by Sebastian Wagner, fixes #2034).

### Bots
#### Collectors
- `intelmq.bots.collectors.shodan.collector_stream`: Fix access to parameters, the bot wrongly used `self.parameters` (PR#2020 by Mikk Margus Möll).
- `intelmq.bots.collectors.mail.collector_mail_attach`: Add attachment file name as `extra.file_name` also if the attachment is not compressed (PR#2021 by Alex Kaplan).
- `intelmq.bots.collectors.http.collector_http_stream`: Fix access to parameters, the bot wrongly used `self.parameters` (by Sebastian Wagner).

#### Parsers
- `intelmq.bots.parsers.microsoft.parser_ctip`: Map `Payload.domain` to `destination.fqdn` instead of `extra.payload.domain` as it matches to `destination.ip` from `DestinationIp` (PR#2023 by Sebastian Wagner).
- Removed `intelmq.bots.parsers.malwaredomains` because the upstream data source (malwaredomains.com) does not exist anymore (PR#2026 by Birger Schacht, fixes #2024).
- `intelmq.bots.parsers.shadowserver.config`:
  - Add support for feed "Vulnerable SMTP Server" (PR#2037 by Mikk Margus Möll).
  - Fix differentiation between feeds "Accessible HTTP" and "Vulnerable HTTP" (PR#2037 by Mikk Margus Möll, fixes #1984).
  - Add support for the new feeds *Microsoft Sinkhole Events Report*, *Microsoft Sinkhole HTTP Events Report* (PR#2036 by Birger Schacht).
  - Complement feed mappings and documentation for feeds with IPv4 and IPv6 variants (PR#2046 by Mikk Margus Möll and Sebastian Wagner).
   - Feed names with and without the optional IPv4/IPv6 postfix can be used now consistently.
  - Add support for feed "Honeypot HTTP Scan" (PR#2047 by Mikk Margus Möll).
  - Update filename mapping for changed filename of feed "Accessible-MSRDPUDP" (PR#2060 by abr4xc).

#### Experts
- `intelmq.bots.experts.gethostbyname.expert`: Handle numeric values for the `gaierrors_to_ignore` parameter (PR#2073 by Sebastian Wagner, fixes #2072).
- `intelmq.bots.experts.filter.expert`: Fix handling of empty-string parameters `not_after` and `not_before` (PR#2075 by Sebastian Wagner, fixes #2074).

#### Outputs
- `intelmq.bots.outputs.mcafee.output_esm_ip`: Fix access to parameters, the bot wrongly used `self.parameters` (by Sebastian Wagner).
- `intelmq.bots.outputs.misp.output_api`: Fix access to parameters, the bot wrongly used `self.parameters` (by Sebastian Wagner).
- `intelmq.bots.outputs.smtp.output`: Add `Content-Disposition`-header to the attachment, fixing the display in Mail Clients as actual attachment (PR#2052 by Sebastian Wagner, fixes #2018).

### Documentation
- Various formatting fixes (by Sebastian Wagner).
- Removed the malwaredomains feed from the feeds list because the upstream data source (malwaredomains.com) does not exist anymore (PR#2026 by Birger Schacht, fixes #2024).
- Update Docker installation instructions (PR#2035 by Sebastian Waldbauer).

### Packaging
- intelmq-update-database crontab: Add missing `recordedfuture_iprisk` update call (by Sebastian Wagner).

### Tests
- Replace calls to deprecated/undocumented `logging.warn` with `logging.warning` (by Sebastian Wagner, fixes #2013).
- `intelmq.tests.bots.experts.rdap.test_expert`: Declare cache use, fixes build failures (by Sebastian Wagner, fixes #2014).
- `intelmq.tests.bots.collectors.mail.test_collector_attach`: Test text attachment (by Sebastian Wagner).

### Tools
- `intelmqctl`:
  - Also honour parameters from environment variables (PR#2068 by Sebastian Wagner, fixes #2063).
  - Fix management actions (start/stop/status/reload/restart) for groups (PR#2086 by Sebastian Wagner, fixes #2085).
  - Do not use hardcoded logging path in `/opt/intelmq`, use the internal default instead (PR#2092 by Sebastian Wagner, fixes #2091).

### Known issues
See [open bug reports](https://github.com/certtools/intelmq/issues?q=is%3Aissue+is%3Aopen+label%3Abug) for a more detailed list.
- ParserBot: erroneous raw line recovery in error handling (#1850).


3.0.0 (2021-07-02)
------------------

### Configuration
- The `BOTS` file is no longer used and has been removed (by Sebastian Wagner).
- The `defaults.conf` file is no longer used and has been removed (PR#1814 by Birger Schacht).
- The `pipeline.conf` file is no longer used and has been removed (PR#1849 by Birger Schacht).
- The `runtime.conf` was renamed to `runtime.yaml` and is now in YAML format (PR#1812 by Birger Schacht).

### Core
- `intelmq.lib.harmonization`:
  - New class `ClassificationTaxonomy` with fixed list of taxonomies and sanitiation (by Sebastian Wagner).
- `intelmq.lib.bot`:
  - Handle `InvalidValue` exceptions upon message retrieval by dumping the message instead of repeating endlessly (#1765, PR#1766 by Filip Pokorný).
  - Rewrite of the parameter loading and handling, getting rid of the `parameters` member (PR#1729 by Birger Schacht).
  - The pipeline is now initialized before the call of `init` to allow bots accessing data directly on startup/initialization for cleanup or maintenance tasks (PR#1982 by Sebastian Wagner).
- `intelmq.lib.exceptions`:
  - `InvalidValue`: Add optional parameter `object` (PR#1766 by Filip Pokorný).
- `intelmq.lib.utils`:
  - New function `list_all_bots` to list all available/installed bots as replacement for the BOTS file (#368, #552, #644, #757, #1069, #1750, PR#1751 by Sebastian Waldbauer).
  - New function `get_bots_settings` to return the effective bot parameters, with global parameters applied (PR#1928 by Sebastian Wagner, #1927).
  - Removed deprecated function `create_request_session_from_bot` (PR#1997 by Sebastian Wagner, #1404).
  - `parse_relative`: Add support for parsing minutes and seconds (PR#1857 by Sebastian Wagner).
- `intelmq.lib.bot_debugger`:
  - Set bot's `logging_level` directly in `__init__` before the bot's initialization by changing the default value (by Sebastian Wagner).
  - Rewrite `load_configuration_patch` by adapting it to the parameter and configuration rewrite (by Sebastian Wagner).
  - Do not rely on the runtime configuration's `group` setting of bots to determine the required message type of messages given on the command line (PR#1949 by Sebastian Wagner).

### Development
- `rewrite_config_files.py`: Removed obsolete BOTS-file-related rewriting functionality (by Sebastian Wagner, #1543).
- A GitHub Action that checks for [reuse compliance](https://reuse.software) of all the license and copyright headers was added (PR#1976 by Birger Schacht).
- PyYAML is no longer a required dependency for development environments, all calls to it have been replaced by ruamel.yaml (by Sebastian Wagner).

### Data Format
The IntelMQ Data Harmonization ("DHO") is renamed to IntelMQ Data Format ("IDF"). Internal files remain and work the same as before (PR#1818 by Sebastian Waldbauer, fixes 1810).
Update allowed classification fields to version 1.3 (2021-05-18) (by Sebastian Wagner, fixes #1409, #1476).
- The taxonomy `abusive content` has been renamed to `abusive-content`.
- The taxonomy `information content security` has been renamed to `information-content-security`.
  - The validation of type `unauthorised-information-access` has been fixed, a bug prevented the use of it.
  - The validation of type `unauthorised-information-modification` has been fixed, a bug prevented the use of it.
  - The type `leak` has been renamed to `data-leak`.
  - The type `dropzone` has been removed. Taxonomy `other` with type `other` and identifier `dropzone` can be used instead. Ongoing discussion in the RSIT WG.
- The taxonomy `intrusion attempts` has been renamed to `intrusion-attempts`.
- For the taxonomy intrusions (PR#1993 by Sebastian Wagner, addresses #1409):
  - The type `compromised` has been renamed to `system-compromise`.
  - The type `unauthorized-command` has been merged into `system-compromise`.
  - The type `unauthorized-login` has been merged into `system-compromise`.
  - The type `backdoor` has been merged into `system-compromise` (PR#1995 by Sebastian Wagner, addresses #1409).
  - The type `defacement` has been merged into taxonomy `information-content-security`, type `unauthorised-information-modification` (PR#1994 by Sebastian Wagner, addresses #1409).
- The taxonomy `information gathering` has been rename to `information-gathering`.
- The taxonomy `malicious code` has been renamed to `malicious-code`.
  - The type `c2server` has been renamed to `c2-server`.
  - The type `malware` has been integrated into `infected-system` and `malware-distribution`, respectively (PR#1917 by Sebastian Wagner addresses #1409).
  - The type `ransomware` has been integrated into `infected-system`.
  - The type `dga domain` has been moved to the taxonomy `other` renamed `dga-domain` (PR#1992 by Sebastian Wagner fixes #1613).
- For the taxonomy 'availability', the type `misconfiguration` is new.
- For the taxonomy 'other', the type `unknown` has been renamed to `undetermined`.
- For the taxonomy 'vulnerable':
  - The type `vulnerable client` has been renamed to `vulnerable-system`.
  - The type `vulnerable service` has been renamed to `vulnerable-system`.

### Bots
- The parameters handling of numerous bots has been refactored (PR#1751, PR#1729, by Birger Schacht, Sebastian Wagner, Sebastian Waldbauer).

#### Collectors
- Remove `intelmq.bots.collectors.xmpp`: one of the dependencies of the bot was deprecated and according to a short survey on the IntelMQ
  users mailinglist, the bot is not used by anyone. (https://lists.cert.at/pipermail/intelmq-users/2020-October/000177.html, PR#1761 by Birger Schacht, closes #1614).
- `intelmq.bots.collectors.mail._lib`: Added parameter `mail_starttls` for STARTTLS in all mail collector bots (PR#1831 by Marius Karotkis, fixes #1128).
- Added `intelmq.bots.collectors.fireeye`: A bot that collects indicators from Fireeye MAS appliances (PR#1745 by Christopher Schappelwein).
- `intelmq.bots.collectors.api.collector_api` (PR#1987 by Mikk Margus Möll, fixes #1986):
  - Added UNIX socket capability.
  - Correctly close the IOLoop in the shutdown method to fix reload.
- `intelmq.bots.collectors.rt.collector_rt` (PR#1997 by Sebastian Wagner, #1404):
  - compatibility with the deprecated parameter `unzip_attachment` (removed in 2.1.0) was removed.

#### Parsers
- Added `intelmq.bots.parsers.fireeye`: A bot that parses hashes and URLs from Fireeye MAS indicators (PR#1745 by Christopher Schappelwein).
- `intelmq.bots.parsers.shadowserver._config`:
  - Improved the feed-mapping and all conversion functions (PR#1971 by Mikk Margus Möll).
- `intelmq.bots.parsers.generic.parser_csv`:
  - Fix handling of empty string values for parameter `time_format` (by Sebastian Wagner).

#### Experts
- `intelmq.bots.experts.domain_suffix.expert`:
  - Added `--update-database` option to update domain suffix database (by Sebastian Wagner).
  - Fix `check` method: load database with UTF-8 encoding explicitly (by Sebastian Wagner).
- Added `intelmq.bots.experts.http.expert_status`: A bot that fetches the HTTP Status for a given URI and adds it to the message (PR#1789 by Birger Schacht, fixes #1047 partly).
- Added `intelmq.bots.experts.http.expert_content`: A bot that fetches an HTTP resource and checks if it contains a specific string (PR#1811 by Birger Schacht).
- Added `intelmq.bots.experts.lookyloo.expert`: A bot that sends requests to a lookyloo instance & adds `screenshot_url` to the event (PR#1844 by Sebastian Waldbauer, fixes #1048).
- Added `intelmq.bots.experts.rdap.expert`: A bot that checks the rdap protocol for an abuse contact for a given domain (PR#1881 by Sebastian Waldbauer and Sebastian Wagner).
- `intelmq.bots.experts.sieve.expert`:
  - Add operators for comparing lists and sets (PR#1895 by Mikk Margus Möll):
    - `:equals`
    - `:overlaps`
    - `:supersetof`
    - `:subsetof`
    - `:equals`
  - Add support for comparing boolean values (PR#1895 by Mikk Margus Möll).
  - Add support for rule negation with `!` (PR#1895, PR#1923 by Mikk Margus Möll).
  - Add support for values types float, int, bool and string for all lists items (PR#1895 by Mikk Margus Möll).
  - Add actions for lists (PR#1895 by Mikk Margus Möll).
    - `append`
    - `append!` (forced/overwriting)
  - Rewrite the rule-processing and operator-handling code to make it more comprehensible and extensible (PR#1895, PR#1923 by Mikk Margus Möll).
  - Nested if statements, plus mixed actions and actions in the same scope (PR #1923 by Mikk Margus Möll).
  - The attribute manipulation actions add, add! and update support non-string (bool/int/float) values (PR #1923 by Mikk Margus Möll).
  - Drop the `:notcontains` operator, as it made is redundant by generic negation: `! foo :contains 'x'` instead of `foo :notcontains 'x'` (PR#1957 by Mikk Margus Möll).
  - Split string and numeric matches into single- and multivalued variants, with the relevant new operators `:in`, `:containsany` and `:regexin` for string lists, and `:in` for numeric value lists (PR#1957 by Mikk Margus Möll).
    - Removed the `==` operator for lists, with the previous meaning of `:in`. Have a look at the NEWS.md for more information.
- Added `intelmq.bots.experts.uwhoisd`: A bot that fetches the whois entry from a uwhois-instance (PR#1918 by Raphaël Vinot).
- Removed deprecated `intelmq.bots.experts.ripencc_abuse_contact.expert`. It was replaced by `intelmq.bots.experts.ripe.expert` and marked as deprecated in 2.0.0.beta1 (PR#1997 by Sebastian Wagner, #1404).
- `intelmq.bots.experts.modify.expert`:
  - Removed compatibility with deprecated configuration format before 1.0.0.dev7 (PR#1997 by Sebastian Wagner, #1404).
- Added `intelmq.bots.experts.aggregate`: A bot that aggregate events based upon given fields & a timespan (PR#1959 by Sebastian Waldbauer).
- Added `intelmq.bots.experts.tuency`: A bot that queries the IntelMQ API of a tuency instance (PR#1857 by Sebastian Wagner, fixes #1856).

#### Outputs
- Remove `intelmq.bots.outputs.xmpp`: one of the dependencies of the bot was deprecated and according to a short survey on the IntelMQ
  users mailinglist, the bot is not used by anyone. (https://lists.cert.at/pipermail/intelmq-users/2020-October/000177.html, PR#1761 by Birger Schacht, closes #1614)
- `intelmq.bots.outputs.smtp`: Add more debug logging (PR#1949 by Sebastian Wagner).
- Added new bot `intelmq.bots.outputs.templated_smtp` (PR#1901 by Karl-Johan Karlsson).

### Documentation
- Updated user and developer documentation to reflect the removal of the BOTS file (PR#1780 by Birger Schacht).
- Bots documentation:
  - Added anchors to all bot sections derived from the module names for easier linking (PR#1943 by Sebastian Wagner fixes part of certtools/intelmq-api#4).
- License and copyright information was added to all the bots (PR#1976 by Birger Schacht).
- Added documentation on the EventDB (PR#1955 by Birger Schacht, PR#1985 by Sebastian Wagner).
- Added TimescaleDB for time-series documentation (PR#1990 by Sebastian Waldbauer).
- Improved n6 interoperability documentation by adding more graphs and illustrations (PR#1991 by Sebastian Wagner).
- Feed documentation generation: fix and simplify formatting of parameters of types lists, non-string values have been ill-treated (by Sebastian Wagner).
- Added documentation on abuse-contact look-ups (PR#2021 by Sebastian Waldbauer and Sebastian Wagner).

### Packaging
- Docker images tagged with `certat/intelmq-full:develop` are built and published on every push to the develop branch (PR#1753 by Sebastian Waldbauer).
- Adapt packaging to IntelMQ 3.0 changes: ruamel.yaml dependency, changed configuration, updated database-update scripts (by Birger Schacht and Sebastian Wagner).

### Tests
- `intelmq.tests.lib.test_bot`:
  - Add test case for a raised `InvalidValue` exception upon message retrieval (#1765, PR#1766 by Filip Pokorný and Sebastian Wagner).
- `intelmq.lib.test`:
  - Compare content of the `output` field as dictionaries, not as string in `assertMessageEqual` (PR#1975 by Karl-Johan Karlsson).
  - Support multiple calls to `run_bot` from test cases (PR#1989 by Sebastian Wagner).
    - Split `prepare_source_queue` out of `prepare_bot`.
    - Added new optional parameter `stop_bot` to `run_bot`.

### Tools
- intelmqdump (PR#1997 by Sebastian Wagner, #1404):
  - The command `e` for deleting single entries by given IDs has been merged into the command `d` ("delete"), which can now delete either entries by ID or the whole file.
  - The command `v` for editing entries has been renamed to `e` ("edit").

### Contrib
- eventdb:
  - Added `separate-raws-table.sql` (PR#1985 by Sebastian Wagner).
- cron-jobs: Removed the deprecated update scripts (PR#1997 by Sebastian Wagner, #1404):
  - `update-asn-data`
  - `update-geoip-data`
  - `update-tor-nodes`
  - `update-rfiprisk-data`
  in favor of the built-in update-mechanisms (see the bots' documentation). A crontab file for calling all new update command can be found in `contrib/cron-jobs/intelmq-update-database`.

### Known issues
- ParserBot: erroneous raw line recovery in error handling (#1850).
- ruamel.yaml loader and dumper: human readability bug / support for comments (#2003).


2.3.3 (2021-05-31)
------------------

### Core
- `intelmq.lib.upgrade`:
  - Added `v233_feodotracker_browse` for Abuse.ch Feodotracker Browse parser configuration adaption (PR#1941 by Sebastian Wagner).

### Bots
#### Parsers
- `intelmq.bots.parsers.microsoft.parser_ctip`:
  - Add support for new field `SourceIpInfo.SourceIpv4Int` (PR#1940 by Sebastian Wagner).
  - Fix mapping of "ConnectionType" fields, this is not `protocol.application`. Now mapped to `extra.*.connection_type` (PR#1940 by Sebastian Wagner).
- `intelmq.bots.parsers.shadowserver._config`:
  - Add support for the new feeds *Honeypot-Amplification-DDoS-Events*, *Honeypot-Brute-Force-Events*, *Honeypot-Darknet*, *IP-Spoofer-Events*, *Sinkhole-Events*, *Sinkhole-HTTP-Events*, *Vulnerable-Exchange-Server*, *Sinkhole-Events-HTTP-Referer* (PR#1950, PR#1952, PR#1953, PR#1954, PR#1970 by Birger Schacht and Sebastian Wagner, PR#1971 by Mikk Margus Möll).

#### Experts
- `intelmq.bots.experts.splunk_saved_search.expert`:
  - fixed erroneous string formatting (PR#1960 by Karl-Johan Karlsson).

#### Outputs
- `intelmq.bots.outputs.smtp.output`:
  - Handle empty "fieldnames" parameter by sending no attachment (PR#1932 by Sebastian Wagner).

### Documentation
- `dev/data-harmonization` renamed to `dev/data-format` (by Sebastian Waldbauer)
- Feeds:
  - Fixed Abuse.ch Feodotracker Browse parser configuration (PR#1941 by Sebastian Wagner fixes #1938).

### Tests
- `intelmq.bots.parsers.html_table`:
  - Added testcase for Abuse.ch Feodotracker Browse (PR#1941 by Sebastian Wagner).

### Tools
- intelmqsetup:
  - Set ownershop of state file path and its parent directory (PR#1911 by Sebastian Wagner).

### Known issues
- ParserBot: erroneous raw line recovery in error handling (#1850).


2.3.2 (2021-04-27)
------------------

### Core
- `intelmq.lib.harmonization`:
  - `TLP` type: accept value "yellow" for TLP level AMBER.

### Bots
#### Collectors
- `intelmq.bots.collectors.shadowserver.collector_reports_api`:
  - Handle timeouts by logging the error and continuing to next report (PR#1852 by Marius Karotkis and Sebastian Wagner, fixes #1823).

#### Parsers
- `intelmq.bots.parsers.shadowserver.config`:
  - Parse and harmonize field `end_time` as date in Feeds "Drone-Brute-Force" and "Amplification-DDoS-Victim" (PR#1833 by Mikk Margus Möll).
  - Add conversion function `convert_date_utc` which assumes UTC and sanitizes the data to datetime (by Sebastian Wagner, fixes #1848).
- `intelmq.bots.parsers.shadowserver.parser_json`:
  - Use the overwrite parameter for optionally overwriting the "feed.name" field (by Sebastian Wagner).
- `intelmq.bots.parsers.microsoft.parser_ctip`:
  - Handle fields `timestamp`, `timestamp_utc`, `source_ip`, `source_port`, `destination_ip`, `destination_port`, `computer_name`, `bot_id`, `asn`, `geo` in `Payload` of CTIP Azure format (PR#1841, PR#1851 and PR#1879 by Sebastian Wagner).
- `intelmq.bots.parsers.shodan.parser`:
  - Added support for unique keys and verified vulns (PR#1835 by Mikk Margus Möll).
- `intelmq.bots.parsers.cymru.parser_cap_program`:
  - Fix parsing in whitespace edge case in comments (PR#1870 by Alex Kaplan, fixes #1862).

#### Experts
- `intelmq.bots.experts.modify`:
  - Add a new rule to the example configuration to change the type of malicious-code events to `c2server` if the malware name indicates c2 (PR#1854 by Sebastian Wagner).
- `intelmq.bots.experts.gethostbyname.expert`:
  - Fix handling of parameter `gaierrors_to_ignore` with value `None` (PR#1890 by Sebastian Wagner, fixes #1886).

#### Outputs
- `intelmq.bots.outputs.elasticsearch`: Fix log message on required elasticsearch library message (by Sebastian Wagner).

### Documentation
- `dev/data-harmonization`: Fix taxonomy name "information gathering" should be "information-gathering" (by Sebastian Wagner).

### Tests
- `intelmq.tests.bots.parsers.microsoft.test_parser_ctip_azure`:
  - Add test case for TLP level "YELLOW".

### Known issues
- ParserBot: erroneous raw line recovery in error handling (#1850).


2.3.1 (2021-03-25)
------------------

### Configuration

### Core
- `intelmq.lib.utils`:
  - `log`: Handle null value for logging parameter `logging_max_size` (PR#1786 by Sebastian Wagner, fixes #1778).
- `intelmq.lib.pipeline`:
  - `Amqp._get_queues`: Check virtual host when retrieving queue sizes. Fixes output of `intelmqctl check` for orphaned queues if AMQP is used and the AMQP user has access to more virtual hosts (PR#1830 by Sebastian Wagner, fixes #1746).

### Bots
#### Collectors
- `intelmq.bots.collectors.shadowserver.collector_reports_api`: Added debug logging to show number of downloaded reports and download size (PR#1826 by Sebastian Wagner, partly addresses #1688 and #1823).

#### Parsers
- `intelmq.bots.parsers.cymru.parser_cap_program`:
  - Adapt parser to new upstream format for events of category "bruteforce" (PR#1795 by Sebastian Wagner, fixes 1794).
- `intelmq.bots.parsers.shodan.parser`:
  - Support nested conversions, improved protocol detection and extended Shodan parser mappings (PR#1821 by Mikk Margus Möll).

### Documentation
- Add missing newlines at end of `docs/_static/intelmq-manager/*.png.license` files (PR#1785 by Sebastian Wagner, fixes #1777).
- Ecosystem: Revise sections on intelmq-cb-mailgen and fody (PR#1792 by Bernhard Reiter).
- intelmq-api: Add documentation about necessary write permission for the session database file (PR#1798 by Birger Schacht, fixes intelmq-api#23).
- FAQ: Section on redis socket permissions: set only minimal necessary permissions (PR#1809 by Sebastian Wagner).
- Add document on hardware requirements (PR#1811 by Sebastian Wagner).
- Feeds: Added Shodan Country Stream (by Sebastian Wagner).

### Tests
- Add missing newlines at end of various test input files (PR#1785 by Sebastian Wagner, fixes #1777).
- `intelmq.tests.bots.parsers.shodan.test_parser`: Add test cases for new code (PR#1821 by Mikk Margus Möll).
- `intelmq.tests.lib.test_harmonization.test_datetime_convert`: Only run this test in timezone UTC (PR#1825 by Sebastian Wagner).

### Tools
- `intelmqsetup`:
  - Also cover required directory layout and file permissions for `intelmq-api` (PR#1787 by Sebastian Wagner, fixes #1783).
  - Also cover webserver and sudoers configuration for `intelmq-api` and `intelmq-manger` (PR#1805 by Sebastian Wagner, fixes #1803).
- `intelmqctl`:
  - Do not log an error message if logging to file is explicitly disabled, e.g. in calls from `intelmsetup`. The error message would not be useful for the user and is not necessary.

### Known issues
- Bots started with IntelMQ-API/Manager stop when the webserver is restarted (#952).
- Corrupt dump files when interrupted during writing (#870).
- CSV line recovery forces Windows line endings (#1597).
- intelmqdump: Honor logging_path variable (#1605).
- Timeout error in mail URL fetcher (#1621).
- Shadowserver Parser: Drone feed has (also?) application protocol in type field (mapped to transport protocol) (#1763).


2.3.0 (2021-03-04)
------------------

IntelMQ no longer supports Python 3.5 (and thus Debian 9 and Ubuntu 16.04), the minimum supported Python version is 3.6.

### Configuration

### Core
- `intelmq.lib.bot`:
  - `ParserBot.recover_line_json_stream`: Make `line` parameter optional, as it is not needed for this method (by Sebastian Wagner).
  - `Bot.argparser`: Added class method `_create_argparser` (returns `argparse.ArgumentParser`) for easy command line arguments parsing (PR#1586 by Filip Pokorný).
  - Runtime configuration does not necessarily need a parameter entry for each block. Previously at least an empty block was required (PR#1604 by Filip Pokorný).
  - Allow setting the pipeline host and the Redis cache host by environment variables for docker usage (PR#1669 by Sebastian Waldbauer).
  - Better logging message for SIGHUP handling if the handling of the signal is not delayed (by Sebastian Wagner).
- `intelmq.lib.upgrades`:
  - Add upgrade function for removal of *HPHosts Hosts file* feed and `intelmq.bots.parsers.hphosts` parser (#1559, by Sebastian Wagner).
- `intelmq.lib.exceptions`:
  - `PipelineError`: Remove unused code to format exceptions (by Sebastian Wagner).
- `intelmq.lib.utils`:
  - `create_request_session_from_bot`:
    - Changed bot argument to optional, uses defaults.conf as fallback, renamed to `create_request_session`. Name `create_request_session_from_bot` will be removed in version 3.0.0 (PR#1524 by Filip Pokorný).
    - Fixed setting of `http_verify_cert` from defaults configuration (PR#1758 by Birger Schacht).
  - `log`: Use `RotatingFileHandler` for allow log file rotation without external tools (PR#1637 by Vasek Bruzek).
- `intelmq.lib.harmonization`:
  - The `IPAddress` type sanitation now accepts integer IP addresses and converts them to the string representation (by Sebastian Wagner).
  - `DateTime.parse_utc_isoformat`: Add parameter `return_datetime` to return `datetime` object instead of string ISO format (by Sebastian Wagner).
  - `DateTime.convert`: Fix `utc_isoformat` format, it pointed to a string and not a function, causing an exception when used (by Sebastian Wagner).
  - `DateTime.from_timestamp`: Ensure that time zone information (`+00:00`) is always present (by Sebastian Wagner).
  - `DateTime.__parse` now handles OverflowError exceptions from the dateutil library, happens for large numbers, e.g. telehpone numbers (by Sebastian Wagner).
- `intelmq.lib.upgrades`:
  - Added upgrade function for CSV parser parameter misspelling (by Sebastian Wagner).
  - Check for existence of collector and parser for the obsolete Malware Domain List feed and raise warning if found (#1762, PR#1771 by Birger Schacht).

### Development
- `intelmq.bin.intelmq_gen_docs`:
  - Add bot name to the resulting feed documentation (PR#1617 by Birger Schacht).
  - Merged into `docs/autogen.py` (PR#1622 by Birger Schacht).

### Bots
#### Collectors
- `intelmq.bots.collectors.eset.collector`: Added (PR#1554 by Mikk Margus Möll).
- `intelmq.bots.collectors.http.collector_http`:
  - Added PGP signature check functionality (PR#1602 by sinus-x).
  - If status code is not 2xx, the request's and response's headers and body are logged in debug logging level (#1615, by Sebastian Wagner).
- `intelmq.bots.collectors.kafka.collector`: Added (PR#1654 by Birger Schacht, closes #1634).
- `intelmq.bots.collectors.xmpp.collector`: Marked as deprecated, see https://lists.cert.at/pipermail/intelmq-users/2020-October/000177.html (#1614, PR#1685 by Birger Schacht).
- `intelmq.bots.collectors.shadowserver.collector_api`:
  - Added (#1683, PR#1700 by Birger Schacht).
  - Change file names in the report to `.json` instead of the original and wrong `.csv` (PR#1769 by Sebastian Wagner).
- `intelmq.bots.collectors.mail`: Add content of the email's `Date` header as `extra.email_date` to the report in all email collectors (PR#1749 by aleksejsv and Sebastian Wagner).
- `intelmq.bots.collectors.http.collector_http_stream`: Retry on common connection issues without raising exceptions (#1435, PR#1747 by Sebastian Waldbauer and Sebastian Wagner).
- `intelmq.bots.collectors.shodan.collector_stream`: Retry on common connection issues without raising exceptions (#1435, PR#1747 by Sebastian Waldbauer and Sebastian Wagner).
- `intelmq.bots.collectors.twitter.collector_twitter`:
  - Proper input validation in URLs using urllib. CWE-20, found by GitHub's CodeQL (PR#1754 by Sebastian Wagner).
  - Limit replacement ("pastebin.com", "pastebin.com/raw") to a maximum of one (PR#1754 by Sebastian Wagner).

#### Parsers
- `intelmq.bots.parsers.eset.parser`: Added (PR#1554 by Mikk Margus Möll).
  - Ignore invalid "NXDOMAIN" IP addresses (PR#1573 by Mikk Margus Möll).
- `intelmq.bots.parsers.hphosts`: Removed, feed is unavailable (#1559, by Sebastian Wagner).
- `intelmq.bots.parsers.cznic.parser_haas`: Added (PR#1560 by Filip Pokorný and Edvard Rejthar).
- `intelmq.bots.parsers.cznic.parser_proki`: Added (PR#1599 by sinus-x).
- `intelmq.bots.parsers.key_value.parser`: Added (PR#1607 by Karl-Johan Karlsson).
- `intelmq.bots.parsers.generic.parser_csv`: Added new parameter `compose_fields` (by Sebastian Wagner).
- `intelmq.bots.parsers.shadowserver.parser_json`: Added (PR#1700 by Birger Schacht).
- `intelmq.bots.parsers.shadowserver.config`:
  - Fixed mapping for Block list feed to accept network ranges in CIDR notation (#1720, PR#1728 by Sebastian Waldbauer).
  - Added mapping for new feed MSRDPUDP, Vulnerable-HTTP, Sinkhole DNS (#1716, #1726, #1733, PR#1732, PR#1735, PR#1736 by Sebastian Waldbauer).
  - Ignore value `0` for `source.asn` and `destination.asn` in all mappings to avoid parsing errors (PR#1769 by Sebastian Wagner).
- `intelmq.bots.parsers.abusech.parser_ip`: Adapt to changes in the Feodo Tracker Botnet C2 IP Blocklist feed (PR#1741 by Thomas Bellus).
- `intelmq.bots.parsers.malwaredomainlist`: Removed, as the feed is obsolete (#1762, PR#1771 by Birger Schacht).

#### Experts
- `intelmq.bots.experts.rfc1918.expert`:
  - Add support for ASNs (PR#1557 by Mladen Markovic).
  - Speed improvements.
  - More output in debug logging mode (by Sebastian Wagner).
  - Checks parameter length on initialization and in check method (by Sebastian Wagner).
- `intelmq.bots.experts.gethostbyname.expert`:
  - Added parameter `fallback_to_url` and set to True (PR#1586 by Edvard Rejthar).
  - Added parameter `gaierrors_to_ignore` to optionally ignore other `gethostbyname` errors (#1553).
  - Added parameter `overwrite` to optionally overwrite existing IP addresses (by Sebastian Wagner).
- `intelmq.bots.experts.asn_lookup.expert`:
  - Added `--update-database` option (PR#1524 by Filip Pokorný).
  - The script `update-asn-data` is now deprecated and will be removed in version 3.0.
- `intelmq.bots.experts.maxmind_geoip.expert`:
  - Added `--update-database` option (PR#1524 by Filip Pokorný).
  - Added `license_key` parameter (PR#1524 by Filip Pokorný).
  - The script `update-geoip-data` is now deprecated and will be removed in version 3.0.
- `intelmq.bots.experts.tor_nodes.expert`:
  - Added `--update-database` option (PR#1524 by Filip Pokorný).
  - The script `update-tor-nodes` is now deprecated and will be removed in version 3.0.
- `intelmq.bots.experts.recordedfuture_iprisk.expert`:
  - Added `--update-database` option (PR#1524 by Filip Pokorný).
  - Added `api_token` parameter (PR#1524 by Filip Pokorný).
  - The script `update-rfiprisk-data` is now deprecated and will be removed in version 3.0.
- Added `intelmq.bots.experts.threshold` (PR#1608 by Karl-Johan Karlsson).
- Added `intelmq.bots.experts.splunk_saved_search.expert` (PR#1666 by Karl-Johan Karlsson).
- `intelmq.bots.experts.sieve.expert`:
  - Added possibility to give multiple queue names for the `path` directive (#1462, by Sebastian Wagner).
  - Added possibility to run actions without filtering expression (#1706, PR#1708 by Sebastian Waldbauer).
  - Added datetime math operations (#1680, PR#1696 by Sebastian Waldbauer).
- `intelmq.bots.experts.maxmind_geoip.expert`:
  - Fixed handing over of `overwrite` parameter to `event.add` (PR#1743 by Birger Schacht).

#### Outputs
- `intelmq.bots.outputs.rt`: Added Request Tracker output bot (PR#1589 by Marius Urkis).
- `intelmq.bots.outputs.xmpp.output`: Marked as deprecated, see https://lists.cert.at/pipermail/intelmq-users/2020-October/000177.html (#1614, PR#1685 by Birger Schacht).
- `intelmq.bots.outputs.smtp.output`: Fix sending to multiple recipients when recipients are defined by event-data (#1759, PR#1760 by Sebastian Waldbauer and Sebastian Wagner).

### Documentation
- Feeds:
  - Add ESET URL and Domain feeds (by Sebastian Wagner).
  - Remove unavailable *HPHosts Hosts file* feed (#1559 by Sebastian Wagner).
  - Added CZ.NIC HaaS feed (PR#1560 by Filip Pokorný and Edvard Rejthar).
  - Added CZ.NIC Proki feed (PR#1599 by sinus-x).
  - Updated Abuse.ch URLhaus feed (PT#1572 by Filip Pokorný).
  - Added CERT-BUND CB-Report Malware infections feed (PR#1598 by sinus-x and Sebastian Wagner).
  - Updated Turris Greylist feed with PGP verification information (by Sebastian Wagner).
  - Fixed parsing of the `public` field in the generated feeds documentation (PR#1641 by Birger Schacht).
  - Change the `rate_limit` parameter of some feeds from 2 days (129600 seconds) to one day (86400 seconds).
  - Update the cAPTure Ponmocup Domains feed documentation (PR#1574 by Filip Pokorný and Sebastian Wagner).
  - Added Shadowserver Reports API (by Sebastian Wagner).
  - Change the `rate_limit` parameter for many feeds from 2 days to the default one day (by Sebastian Wagner).
  - Removed Malware Domain List feed, as the feed is obsolete (#1762, PR#1771 by Birger Schacht).
- Bots:
  - Enhanced documentation of RFC1918 Expert (PR#1557 by Mladen Markovic and Sebastian Wagner).
  - Enhanced documentation of SQL Output (PR#1620 by Edvard Rejthar).
  - Updated documentation for MaxMind GeoIP, ASN Lookup, TOR Nodes and Recorded Future experts to reflect new `--update-database` option (PR#1524 by Filip Pokorný).
  - Added documentation for Shadowserver API collector and parser (PR#1700 by Birger Schacht and Sebastian Wagner).
- Add n6 integration documentation (by Sebastian Wagner).
- Moved 'Orphaned Queues' section from the FAQ to the intelmqctl documentation (by Sebastian Wagner).
- Generate documentation using Sphinx (PR#1622 by Birger Schacht).
  - The documentation is now available at https://intelmq.readthedocs.io/en/latest/
  - Refactor documentation and fix broken syntax (#1639, PRs #1638 #1640 #1642 by Birger Schacht).
- Integrate intelmq-manager and intelmq-api user documentation to provide unified documentation place (PR#1714 & PR#1714 by Birger Schacht).

### Packaging
- Fix paths in the packaged logcheck rules (by Sebastian Wagner).
- Build the sphinx documentation on package build (PR#1701 by Birger Schacht).
- Ignore non-zero exit-codes for the `intelmqctl check` call in postinst (#1748, by Sebastian Wagner).

### Tests
- Added tests for `intelmq.lib.exceptions.PipelineError` (by Sebastian Wagner).
- `intelmq.tests.bots.collectors.http_collector.test_collector`: Use `requests_mock` to mock all requests and do not require a local webserver (by Sebastian Wagner).
- `intelmq.tests.bots.outputs.restapi.test_output`:
  - Use `requests_mock` to mock all requests and do not require a local webserver (by Sebastian Wagner).
  - Add a test for checking the response status code (by Sebastian Wagner).
- `intelmq.tests.bots.collectors.mail.test_collector_url`: Use `requests_mock` to mock all requests and do not require a local webserver (by Sebastian Wagner).
- `intelmq.tests.bots.experts.ripe.test_expert`: Use `requests_mock` to mock all requests and do not require a local webserver (by Sebastian Wagner).
- The test flag (environment variable) `INTELMQ_TEST_LOCAL_WEB` is no longer used (by Sebastian Wagner).
- Added tests for `intelmq.harmonization.DateTime.parse_utc_isoformat` and `convert_fuzzy` (by Sebastian Wagner).
- Move from Travis to GitHub Actions (PR#1707 by Birger Schacht).
- `intelmq.lib.test`:
  - `test_static_bot_check_method` checks the bot's static `check(parameters)` method for any exceptions, and a valid formatted return value (#1505, by Sebastian Wagner).
  - `setUpClass`: Skip tests if cache was requests with `use_cache` member, but Redis is deactivated with the environment variable `INTELMQ_SKIP_REDIS` (by Sebastian Wagner).
- `intelmq.tests.bots.experts.cymru_whois.test_expert`:
  - Switch from `example.com` to `ns2.univie.ac.at` for hopefully more stable responses (#1730, PR#1731 by Sebastian Waldbauer).
  - Do not test for exact expected values in the 6to4 network test, as the values are changing regularly (by Sebastian Wagner).
- `intelmq.tests.bots.parsers.abusech`: Remove tests cases of discontinued feeds (PR#1741 by Thomas Bellus).
- Activate GitHub's CodeQL Code Analyzing tool as GitHub Action (by Sebastian Wagner).

### Tools
- `intelmqdump`:
    - Check if given queue is configured upon recovery (#1433, PR#1587 by Mladen Markovic).
- `intelmqctl`:
  - `intelmq list queues`: `--sum`, `--count`, `-s` flag for showing total count of messages (#1408, PR#1581 by Mladen Markovic).
  - `intelmq check`: Added a possibility to ignore queues from the orphaned queues check (by Sebastian Wagner).
  - Allow setting the pipeline host by environment variables for docker usage (PR#1669 by Sebastian Waldbauer).

### Contrib
- EventDB:
  - Add SQL script for keeping track of the oldest inserted/update "time.source" information (by Sebastian Wagner).
- Cron Jobs: The script `intelmq-update-data` has been renamed to `intelmq-update-database` (by Filip Pokorný).
- Dropped utterly outdated contrib modules (by Sebastian Wagner):
  - ansible
  - vagrant
  - vagrant-ansible
- logrotate:
  - Do not use the deprecated "copytruncate" option as intelmq re-opens the log anyways (by Sebastian Wagner).
  - Set file permissions to `0644` (by Sebastian Wagner).

### Known issues
- Bots started with IntelMQ-API/Manager stop when the webserver is restarted (#952).
- Corrupt dump files when interrupted during writing (#870).
- CSV line recovery forces Windows line endings (#1597).
- intelmqdump: Honor logging_path variable (#1605).
- Timeout error in mail URL fetcher (#1621).
- AMQP pipeline: get_queues needs to check vhost of response (#1746).

2.2.3 (2020-12-23)
------------------

### Documentation
- Bots/Sieve expert: Add information about parenthesis in if-expressions (#1681, PR#1687 by Birger Schacht).

### Harmonization
- See NEWS.md for information on a fixed bug in the taxonomy expert.

### Bots
#### Collectors
- `intelmq.bots.rt.collector_rt`: Log the size of the downloaded file in bytes on debug logging level.

#### Parsers
- `intelmq.bots.parsers.cymru.parser_cap_program`:
  - Add support for protocols 47 (GRE) and 59 (IPv6-NoNxt).
  - Add support for field `additional_asns` in optional information column.
- `intelmq.bots.parsers.microsoft.parser_ctip`:
  - Fix mapping of `DestinationIpInfo.DestinationIpConnectionType` field (contained a typo).
  - Explicitly ignore field `DestinationIpInfo.DestinationIpv4Int` as the data is already in another field.
- `intelmq.bots.parsers.generic.parser_csv`:
  - Ignore line having spaces or tabs only or comment having leading tabs or spaces (PR#1669 by Brajneesh).
  - Data fields containing `-` are now ignored and do not raise an exception anymore (#1651, PR#74 by Sebastian Waldbauer).

#### Experts
- `intelmq.bots.experts.taxonomy.expert`: Map type `scanner` to `information-gathering` instead of `information gathering`. See NEWS file for more information.

### Tests
- Travis: Deactivate tests with optional requirements on Python 3.5, as the build fails because of abusix/querycontacts version conflicts on dnspython.

### Known issues
- Bots started with IntelMQ-Manager stop when the webserver is restarted. (#952).
- Corrupt dump files when interrupted during writing (#870).


2.2.2 (2020-10-28)
------------------

### Core
- `intelmq.lib.upgrades`:
  - Add upgrade function for renamed Shadowserver feed name "Blacklisted-IP"/"Blocklist".

### Bots
#### Parsers
- `intelmq.bots.parsers.shadowserver`:
  - Rename "Blacklisted-IP" feed to "Blocklist", old name is still valid until IntelMQ version 3.0 (PR#1588 by Thomas Hungenberg).
  - Added support for the feeds `Accessible Radmin` and `CAIDA IP Spoofer` (PR#1600 by sinus-x).
- `intelmq.bots.parsers.anubisnetworks.parser`: Fix parsing error where `dst.ip` was not equal to `comm.http.host`.
- `intelmq/bots/parsers/danger_rulez/parser`: correctly skip malformed rows by defining variables before referencing (PR#1601 by Tomas Bellus).
- `intelmq.bots.parsers.misp.parser: Fix MISP Event URL (#1619, PR#1618 by Nedfire23).
- `intelmq.bots.parsers.microsoft.parser_ctip`:
  - Add support for `DestinationIpInfo.*` and `Signatures.Sha256` fields, used by the `ctip-c2` feed (PR#1623 by Mikk Margus Möll).
  - Use `extra.payload.text` for the feed's field `Payload` if the content cannot be decoded (PR#1610 by Giedrius Ramas).

#### Experts
- `intelmq.bots.experts.cymru_whois`:
  - Fix cache key calculation which previously led to duplicate keys and therefore wrong results in rare cases. The cache key calculation is intentionally not backwards-compatible (#1592, PR#1606).
  - The bot now caches and logs (as level INFO) empty responses from Cymru (PR#1606).

### Documentation
- README:
  - Add Core Infrastructure Initiative Best Practices Badge.
- Bots:
  - Generic CSV Parser: Add note on escaping backslashes (#1579).
  - Remove section of non-existing "Copy Extra" Bot.
  - Explain taxonomy expert.
  - Add documentation on n6 parser.
  - Gethostbyname expert: Add documentation how errors are treated.
- Feeds:
  - Fixed bot modules of Calidog CertStream feed.
  - Add information on Microsoft CTIP C2 feed.

### Packaging
- In Debian packages, `intelmqctl check` and `intelmqctl upgrade-config` are executed in the "postinst" step (#1551, PR#1624 by Birger Schacht).
- Require `requests<2.26` for Python 3.5, as 2.25.x will be the last release series of the requests library with support for Python 3.5.

### Tests
- `intelmq.tests.lib.test_pipeline`: Skip `TestAmqp.test_acknowledge` on Travis with Python 3.8.
- `intelmq.tests.bots.outputs.elasticsearch.test_output`: Refresh index `intelmq` manually to fix random test failures (#1593, PR#1595 by Zach Stone).

### Tools
- `intelmqctl check`:
  - For disabled bots which do not have any pipeline connections, do not raise an error, but only warning.
  - Fix check on source/destination queues for bots as well the orphaned queues.

### Contrib
- Bash completion scripts: Check both `/opt/intelmq/` as well as LSB-paths (`/etc/intelmq/` and `/var/log/intelmq/`) for loading bot information (#1561, PR#1628 by Birger Schacht).

### Known issues
- Bots started with IntelMQ-Manager stop when the webserver is restarted. (#952).
- Corrupt dump files when interrupted during writing (#870).


2.2.1 (2020-07-30)
------------------

### Core
- `intelmq.lib.upgrades`:
  - Add upgrade function for changed configuration of the feed "Abuse.ch URLhaus" (#1571, PR#1572 by Filip Pokorný).
  - Add upgrade function for removal of *HPHosts Hosts file* feed and `intelmq.bots.parsers.hphosts` parser (#1559).
  - `intelmq.lib.harmonization`:
    - For IP Addresses, explicitly reject IPv6 addresses with scope ID (due to changed behavior in Python 3.9, #1550).

### Development
- Ignore line length (E501) in code-style checks altogether.

### Bots
#### Collectors
- `intelmq.bots.collectors.misp`: Fix access to actual MISP object (PR#1548 by Tomas Bellus @tomas321)
- `intelmq.bots.collectors.stomp`: Remove empty `client.pem` file.

#### Parsers
- `intelmq.bots.parsers.shadowserver.config`:
  - Add support for Accessible-CoAP feed (PR #1555 by Thomas Hungenberg).
  - Add support for Accessible-ARD feed (PR #1584 by Tomas Bellus @tomas321).
- `intelmq.bots.parser.anubisnetworks.parser`: Ignore "TestSinkholingLoss" events, these are not intended to be sent out at all.
- `intelmq.bots.parsers.generic.parser_csv`: Allow values of type dictionary for parameter `type_translation`.
- `intelmq.bots.parsers.hphosts`: Removed, feed is unavailable (#1559).
- `intelmq.bots.parsers.cymru.parser_cap_program`: Add support for comment "username" for "scanner" category.
- `intelmq.bots.parsers.malwareurl.parser`: Check for valid FQDN and IP address in URL and IP address columns (PR#1585 by Marius Urkis).

#### Experts
- `intelmq.bots.experts.maxmind_geoip`: On Python < 3.6, require maxminddb < 2, as that version does no longer support Python 3.5.

#### Outputs
- `intelmq.bot.outputs.udp`: Fix error handling on sending, had a bug itself.

### Documentation
- Feeds:
  - Update documentation of feed "Abuse.ch URLhaus" (#1571, PR#1572 by Filip Pokorný).
- Bots:
  - Overhaul of all bots' description fields (#1570).
- User-Guide:
  - Overhaul pipeline configuration section and explain named queues better (#1577).

### Tests
- `intelmq.tests.bots.experts.cymru`: Adapt `test_empty_result`, remove `test_unicode_as_name` and `test_country_question_mark` (#1576).

### Tools
- `intelmq.bin.intelmq_gen_docs`: Format parameters of types lists with double quotes around values to produce conform JSON, ready to copy and paste the value into the IntelMQ Manager's bot parameter form.
- `intelmq.bin.intelmqctl`:
  - `debug`: In JSON mode, use dictionaries instead of lists.
  - `debug`: Add `PATH` to the paths shown.
  - `check`: Show `$PATH` environment variable if executable cannot be found.

### Contrib
- `malware_name_mapping`: Change MISP Threat Actors URL to new URL (branch master -> main) in download script.

### Known issues
- Bots started with IntelMQ-Manager stop when the webserver is restarted. (#952).
- Corrupt dump files when interrupted during writing (#870).
- Bash completion scripts search in wrong directory in packages (#1561).
- Cymru Expert: Wrong Cache-Key Calculation (#1592).


2.2.0 (2020-06-18)
------------------
Dropped support for Python 3.4.

### Core
- `__init__`: Changes to the path-handling, see [User Guide, section _/opt and LSB paths_](docs/User-Guide.md#opt-and-lsb-paths) for more information
  - The environment variable `INTELMQ_ROOT_DIR` can be used to set custom root directories instead of `/opt/intelmq/` (#805) in case of non LSB-path installations.
  - The environment variable `ROOT_DIR` can be used to set custom root directories instead of `/` (#805) in case of LSB-path installations.
- `intelmq.lib.exceptions`: Added `MissingDependencyError` for show error messages about a missing library and how to install it (#1471).
  - Added optional parameter `installed` to show the installed version.
  - Added optional parameter `additional_text` to show arbitrary text.
- Adding more type annotations for core libraries.
- `intelmq.lib.pipeline.Pythonlist.sleep`: Drop deprecated method.
- `intelmq.lib.utils`: `write_configuration`: Append a newline at end of configuration/file to allow proper comparisons & diffs.
- `intelmq.lib.test`: `BotTestCase` drops privileges upon initialization (#1489).
- `intelmq.lib.bot`:
  - New class `OutputBot`:
    - Method `export_event` to format/export events according to the parameters given by the user.
  - `ParserBot`: New methods `parse_json_stream` and `recover_line_json_stream`.
  - `ParserBot.recover_line_json`: Fix format by adding a list around the line data.
  - `Bot.send_message`: In debugging log level, the path to which the message is sent is now logged too.

### Bots
- Bots with dependencies: Use of `intelmq.lib.exceptions.MissingDependencyError`.

#### Collectors
- `intelmq.bots.collectors.misp.collector`: Deprecate parameter `misp_verify` in favor of generic parameter `http_verify_cert`.
- `intelmq.bots.collectors.tcp.collector`: Drop compatibility with Python 3.4.
- `intelmq.bots.collectors.stomp.collector`:
  - Check the stomp.py version and show an error message if it does not match.
  - For stomp.py versions `>= 5.0.0` redirect the `stomp.PrintingListener` output to debug logging.
- `intelmq.bots.collectors.microsoft.collector_azure`: Support current Python library `azure-storage-blob>= 12.0.0`, configuration is incompatible and needs manual change. See NEWS file and bot's documentation for more details.
- `intelmq.bots.collectors.amqp.collector_amqp`: Require `pika` minimum version 1.0.
- `intelmq.bots.collectors.github_api.collector_github_contents_api`: Added (PR#1481).

#### Parsers
- `intelmq.bots.parsers.autoshun.parser`: Drop compatibility with Python 3.4.
- `intelmq.bots.parsers.html_table.parser`: Drop compatibility with Python 3.4.
- `intelmq.bots.parsers.shadowserver.parser`: Add support for MQTT and Open-IPP feeds (PR#1512, PR#1544).
- `intelmq.bots.parsers.taichung.parser`:
  - Migrate to `ParserBot`.
  - Also parse geolocation information if available.
- `intelmq.bots.parsers.cymru.parser_full_bogons`:
  - Migrate to `ParserBot`.
  - Add last updated information in raw.
- `intelmq.bots.parsers.anubisnetworks.parser`: Add new parameter `use_malware_familiy_as_classification_identifier`.
- `intelmq.bots.parsers.microsoft.parser_ctip`: Compatibility for new CTIP data format used provided by the Azure interface.
- `intelmq.bots.parsers.cymru.parser_cap_program`: Support for `openresolver` type.
- `intelmq.bots.parsers.github_feed.parser`: Added (PR#1481).
- `intelmq.bots.parsers.urlvir.parser`: Removed, as the feed is discontinued (#1537).

#### Experts
- `intelmq.bots.experts.csv_converter`: Added as converter to CSV.
- `intelmq.bots.experts.misp`: Added (PR#1475).
- `intelmq.bots.experts.modify`: New parameter `maximum_matches`.

#### Outputs
- `intelmq.bots.outputs.amqptopic`:
  - Use `OutputBot` and `export_event`.
  - Allow formatting the routing key with event data by the new parameter `format_routing_key` (boolean).
- `intelmq.bots.outputs.file`: Use `OutputBot` and `export_event`.
- `intelmq.bots.outputs.files`: Use `OutputBot` and `export_event`.
- `intelmq.bots.outputs.misp.output_feed`: Added, creates a MISP Feed (PR#1473).
- `intelmq.bots.outputs.misp.output_api`: Added, pushes to MISP via the API (PR#1506, PR#1536).
- `intelmq.bots.outputs.elasticsearch.output`: Dropped ElasticSearch version 5 compatibility, added version 7 compatibility (#1513).

### Documentation
- Document usage of the `INTELMQ_ROOT_DIR` environment variable.
- Added document on MISP integration possibilities.
- Feeds:
  - Added "Full Bogons IPv6" feed.
  - Remove discontinued URLVir Feeds (#1537).

### Packaging
- `setup.py` do not try to install any data to `/opt/intelmq/` as the behavior is inconsistent on various systems and with `intelmqsetup` we have a tool to create the structure and files anyway.
- `debian/rules`:
  - Provide a blank state file in the package.
- Patches:
  - Updated `fix-intelmq-paths.patch`.

### Tests
- Travis: Use `intelmqsetup` here too.
  - Install required build dependencies for the Debian package build test.
  - This version is no longer automatically tested on Python `<` 3.5.
  - Also run the tests on Python 3.8.
  - Run the Debian packaging tests on Python 3.5 and the code-style test on 3.8.
- Added tests for the new bot `intelmq.bots.outputs.misp.output_feed` (#1473).
- Added tests for the new bot `intelmq.bots.experts.misp.expert` (#1473).
- Added tests for `intelmq.lib.exceptions`.
- Added tests for `intelmq.lib.bot.OutputBot` and `intelmq.lib.bot.OutputBot.export_event`.
- Added IPv6 tests for `intelmq.bots.parsers.cymru.parser_full_bogons`.
- Added tests for `intelmq.lib.bot.ParserBot`'s new methods `parse_json_stream` and `recover_line_json_stream`.
- `intelmq.tests.test_conf`: Set encoding to UTF-8 for reading the `feeds.yaml` file.

### Tools
- `intelmqctl`:
  - `upgrade-config`:
    - Allow setting the state file location with the `--state-file` parameter.
    - Do not require a second run anymore, if the state file is newly created (#1491).
    - New parameter `no_backup`/`--no-backup` to skip creation of `.bak` files for state and configuration files.
  - Only require `psutil` for the `IntelMQProcessManager`, not for process manager independent calls like `upgrade-config` or `check`.
  - Add new command `debug` to output some information for debugging. Currently implemented:
    - paths
    - environment variables
  - `IntelMQController`: New argument `--no-file-logging` to disable logging to file.
  - If dropping privileges does not work, `intelmqctl` will now abort (#1489).
- `intelmqsetup`:
  - Add argument parsing and an option to skip setting file ownership, possibly not requiring root permissions.
  - Call `intelmqctl upgrade-config` and add argument for the state file path (#1491).
- `intelmq_generate_misp_objects_templates.py`: Tool to create a MISP object template (#1470).
- `intelmqdump`: New parameter `-t` or `--truncate` to optionally give the maximum length of `raw` data to show, 0 for no truncating.

### Contrib
- Added `development-tools`.
- ElasticSearch: Dropped version 5 compatibility, added version 7 compatibility (#1513).
- Malware Name Mapping Downloader:
  - New parameter `--mwnmp-ignore-adware`.
  - The parameter `--add-default` supports an optional parameter to define the default value.

### Known issues
- Bots started with IntelMQ-Manager stop when the webserver is restarted. (#952).
- Corrupt dump files when interrupted during writing (#870).


2.1.3 (2020-05-26)
------------------

### Requirements
- The python library `requests` is (again) listed as dependency of the core (#1519).

### Core
- `intelmq.lib.upgrades`:
  - Harmonization upgrade: Also check and update regular expressions.
  - Add function to migrate the deprecated parameter `attach_unzip` to `extract_files` for the mail attachment collector.
  - Add function to migrate changed Taichung URL feed.
  - Check for discontinued Abuse.CH Zeus Tracker feed.
- `intelmq.lib.bot`:
  - `ParserBot.recover_line`: Parameter `line` needs to be optional, fix usage of fallback value `self.current_line`.
  - `start`: Handle decoding errors in the pipeline different so that the bot is not stuck in an endless loop (#1494).
  - `start`: Only acknowledge a message in case of errors, if we actually had a message to dump, which is not the case for collectors.
  - `_dump_message`: Dump messages with encoding errors base64 encoded, not in JSON format as it's not possible to decode them (#1494).
- `intelmq.lib.test`:
  - `BotTestCase.run_bot`: Add parameters `allowed_error_count` and `allowed_warning_count` to allow set the number per run, not per test class.
  - Set `source_pipeline_broker` and `destination_pipeline_broker` to `pythonlist` instead of the old `broker`, fixes `intelmq.tests.lib.test_bot.TestBot.test_pipeline_raising`.
  - Fix test for (allowed) errors and warnings.
- `intelmq.lib.exceptions`:
  - `InvalidKey`: Add `KeyError` as parent class.
  - `DecodingError`: Added, string representation has all relevant information on the decoding error, including encoding, reason and the affected string (#1494).
- `intelmq.lib.pipeline`:
  - Decode messages in `Pipeline.receive` not in the implementation's `_receive` so that the internal counter is correct in case of decoding errors (#1494).
- `intelmq.lib.utils`:
  - `decode`: Raise new `DecodingError` if decoding fails.

### Harmonization
- `protocol.transport`: Adapt regular expression to allow the value `nvp-ii` (protocol 11).

### Bots
#### Collectors
- `intelmq.bots.collectors.mail.collector_mail_attach`:
  - Fix handling of deprecated parameter name `attach_unzip`.
  - Fix handling of attachments without filenames (#1538).
- `intelmq.bots.collectors.stomp.collector`: Fix compatibility with stomp.py versions `> 4.1.20` and catch errors on shutdown.
- `intelmq.bots.collectors.microsoft`:
  - Update `REQUIREMENTS.txt` temporarily fixing deprecated Azure library (#1530, PR#1532).
  - `intelmq.bots.collectors.microsoft.collector_interflow`: Add method for printing the file list.

#### Parsers
- `intelmq.bots.parsers.cymru.parser_cap_program`: Support for protocol 11 (`nvp-ii`) and `conficker` type.
- `intelmq.bots.parsers.taichung.parser`: Support more types/classifications:
  - Application Compromise: Apache vulnerability & SQL injections
  - Brute-force: MSSQL & SSH password guess attacks; Office 365, SSH & SIP attacks
  - C2 Sever: Attack controller
  - DDoS
  - DoS: DNS, DoS, Excess connection
  - IDS Alert / known vulnerability exploitation: backdoor
  - Malware: Malware Proxy
  - Warn on new unknown types.
- `intelmq.bots.parsers.bitcash.parser`: Removed as feed is discontinued.
- `intelmq.bots.parsers.fraunhofer.parser_ddosattack_cnc` and `intelmq.bots.parsers.fraunhofer.parser_ddosattack_target`: Removed as feed is discontinued.
- `intelmq.bots.parsers.malwaredomains.parser`: Correctly classify `C&C` and `phishing` events.
- `intelmq.bots.parsers.shadowserver.parser`: More verbose error message for missing report specification (#1507).
- `intelmq.bots.parsers.n6.parser_n6stomp`: Always add n6 field `name` as `malware.name` independent of `category`.
- `intelmq.bots.parsers.anubisnetworks`: Update parser with new data format.
- `intelmq.bots.parsers.bambenek`: Add new feed URLs with Host `faf.bambenekconsulting.com` (#1525, PR#1526).
- `intelmq.bots.parsers.abusech.parser_ransomware`: Removed, as the feed is discontinued (#1537).
- `intelmq.bots.parsers.nothink.parser`: Removed, as the feed is discontinued (#1537).
- `intelmq.bots.parsers.n6.parser`: Remove not allowed characters in the name field for `malware.name` and write original value to `event_description.text` instead.

#### Experts
- `intelmq.bots.experts.cymru_whois.lib`: Fix parsing of AS names with Unicode characters.

#### Outputs
- `intelmq.bots.outputs.mongodb`:
  - Set default port 27017.
  - Use different authentication mechanisms per MongoDB server version to fix compatibility with server version >= 3.4 (#1439).

### Documentation
- Feeds:
  - Remove unavailable feed Abuse.CH Zeus Tracker.
  - Remove the field `status`, offline feeds should be removed.
  - Add a new field `public` to differentiate between private and public feeds.
  - Adding documentation URLs to nearly all feeds.
  - Remove unavailable Bitcash.cz feed.
  - Remove unavailable Fraunhofer DDos Attack feeds.
  - Remove unavailable feed Abuse.CH Ransomware Tracker (#1537).
  - Update information on Bambenek Feeds, many require a license now (#1525).
  - Remove discontinued Nothink Honeypot Feeds (#1537).
- Developers Guide: Fix the instructions for `/opt/intelmq` file permissions.

### Packaging
- Patches: `fix-logrotate-path.patch`: also include path to rotated file in patch.
- Fix paths from `/opt` to LSB for `setup.py` and `contrib/logrotate/intelmq` in build process (#1500).
- Add runtime dependency `debianutils` for the program `which`, which is required for `intelmqctl`.

### Tests
- Dropping Travis tests for 3.4 as required libraries dropped 3.4 support.
- `intelmq.tests.bots.experts.cymru_whois`:
  - Drop missing ASN test, does not work anymore.
  - IPv6 to IPv4 test: Test for two possible results.
- `intelmq.lib.test`: Fix compatibility of logging capture with Python >= 3.7 by reworking the whole process (#1342).
- `intelmq.bots.collectors.tcp.test_collector`: Removing custom mocking and bot starting, not necessary anymore.
- Added tests for `intelmq.bin.intelmqctl.IntelMQProcessManager._interpret_commandline`.
- Fix and split `tests.bots.experts.ripe.test_expert.test_ripe_stat_error_json`.
- Added tests for invalid encodings in input messages in `intelmq.tests.lib.test_bot` and `intelmq.tests.lib.test_pipeline` (#1494).
- Travis: Explicitly enable RabbitMQ management plugin.
- `intelmq.tests.lib.test_message`: Fix usage of the parameter `blacklist` for Message hash tests (#1539).

### Tools
- `intelmqsetup`: Copy missing BOTS file to IntelMQ's root directory (#1498).
- `intelmq_gen_docs`: Feed documentation generation: Handle missing/empty parameters.
- `intelmqctl`:
  - `IntelMQProcessManager`: For the status of running bots also check the bot ID of the commandline and ignore the path of the executable (#1492).
  - `IntelMQController`: Fix exit codes of `check` command for JSON output (now 0 on success and 1 on error, was swapped, #1520).
- `intelmqdump`:
  - Handle base64-type messages for show, editor and recovery actions.

### Contrib
- `intelmq/bots/experts/asn_lookup/update-asn-data`: Use `pyasn_util_download.py` to download the data instead from RIPE, which cannot be parsed currently (#1517, PR#1518, https://github.com/hadiasghari/pyasn/issues/62).

### Known issues
- HTTP stream collector: retry on regular connection problems? (#1435).
- Bots started with IntelMQ-Manager stop when the webserver is restarted. (#952).
- Reverse DNS: Only first record is used (#877).
- Corrupt dump files when interrupted during writing (#870).


2.1.2 (2020-01-28)
------------------

### Core
- `__init__`: Resolve absolute path for `STATE_FILE_PATH` variable (resolves `..`).
- `intelmq.lib.utils`:
  - log: Do not raise an exception if logging to neither file nor syslog is requested.
  - logging StreamHandler: Colorize all warning and error messages red.
  - logging FileHandler: Strip all shell colorizations from the messages (#1436).
- `intelmq.lib.message`:
  - `Message.to_json`: Set `sort_keys=True` to get reproducible results.
  - `drop_privileges`: Handle situations where the user or group `intelmq` does not exist.
- `intelmq.lib.pipeline`:
  - `Amqp._send` and `Amqp._acknowledge`: Log traceback in debug mode in case of errors and necessary re-connections.
  - `Amqp._acknowledge`: Reset delivery tag if acknowledge was successful.

### Bots
#### Collectors
- `intelmq.bots.collectors.misp.collector`:
  - Add compatibility with current pymisp versions and versions released after January 2020 (PR #1468).

#### Parsers
- `intelmq.bots.parsers.shadowserver.config`: Add some missing fields for the feed `accessible-rdp` (#1463).
- `intelmq.bots.parsers.shadowserver.parser`:
  - Feed-detection based on file names: The prefixed date is optional now.
  - Feed-detection based on file names: Re-detect feed for every report received (#1493).

#### Experts
- `intelmq.bots.experts.national_cert_contact_certat`: Handle empty responses by server (#1467).
- `intelmq.bots.experts.maxmind_geoip`: The script `update-geoip-data` now requires a license key as second parameter because of upstream changes (#1484)).

#### Outputs
- `intelmq.bots.outputs.restapi.output`: Fix logging of response body if response status code was not ok.

### Documentation
- Remove some hardcoded `/opt/intelmq/` paths from code comments and program outputs.

### Packaging
- debian/rules: Only replace `/opt/intelmq/` with LSB-paths in some certain files, not the whole tree, avoiding wrong replacements.
- debian/rules and debian/intelmq.install: Do install the examples configuration directly instead of working around the abandoned examples directory.

### Tests
- `lib/test_utils`: Skip some tests on Python 3.4 because `contextlib.redirect_stdout` and `contextlib.redirect_sterr` are not supported on this version.
- Travis: Stop running tests with all optional dependencies on Python 3.4, as more and more libraries are dropping support for it. Tests on the core and code without non-optional requirements are not affected.
- `tests.bots.parsers.html_table`: Make tests independent of current year.

### Tools
- `intelmqctl upgrade-config`: Fix missing substitution in error message "State file %r is not writable.".

### Known issues
- bots trapped in endless loop if decoding of raw message fails (#1494)
- intelmqctl status of processes: need to check bot id too (#1492)
- MongoDB authentication: compatibility on different MongoDB and pymongo versions (#1439)
- ctl: shell colorizations are logged (#1436)
- http stream collector: retry on regular connection problems? (#1435)
- tests: capture logging with context manager (#1342)
- Bots started with IntelMQ-Manager stop when the webserver is restarted. (#952)
- n6 parser: mapping is modified within each run (#905)
- reverse DNS: Only first record is used (#877)
- Corrupt dump files when interrupted during writing (#870)


2.1.1 (2019-11-11)
------------------

### Configuration
- Default configuration:
  - Remove discontinued feed "Feodo Tracker Domains" from default configuration.
  - Add "Feodo Tracker Browse" feed to default configuration.

### Core
- `intelmq.lib.pipeline`: AMQP: using port 15672 as default (like RabbitMQ's defaults) for the monitoring interface for getting statistical data (`intelmqctl_rabbitmq_monitoring_url`).
- `intelmq.lib.upgrades`: Added a generic upgrade function for harmonization, checking of all message types, it's fields and their types.
- `intelmq.lib.utils`:
  - `TimeoutHTTPAdapter`: A subclass of `requests.adapters.HTTPAdapter` with the possibility to set the timeout per adapter.
  - `create_request_session_from_bot`: Use the `TimeoutHTTPAdapter` with the user-defined timeout. Previously the timeout was not functional.

### Bots
#### Parsers
- `intelmq.bots.parsers.shadowserver.parser`: Fix logging message if the parameter `feedname` is not present.
- `intelmq.bots.parsers.shodan.parser`: Also add field `classification.identifier` (`'network-scan'`) in minimal mode.
- `intelmq.bots.parsers.spamhaus.parser_cert`: Add support for category `'misc'`.
- `intelmq.bots.parsers.cymru.parser_cap_program`:
  - Add support for phishing events without URL.
  - Add support for protocols >= 143 (unassigned, experiments, testing, reserved), saving the number to extra, as the data would be bogus.
- `intelmq.bots.parsers.microsoft.parser_bingmurls`:
  - Save the `Tags` data as `source.geolocation.cc`.

#### Experts
- `intelmq.bots.experts.modify.expert`: Fix bug with setting non-string values (#1460).

#### Outputs
- `intelmq.bots.outputs.smtp`:
  - Allow non-existent field in text formatting by using a default value `None` instead of throwing errors.
  - Fix Authentication (#1464).
  - Fix sending to multiple recipients (#1464).

### Documentation
- Feeds:
  - Fix configuration of `Feodo Tracker Browse` feed.
- Bots:
  - Sieve expert: Document behavior of `!=` with lists.

### Tests
- Adaption and extension of the test cases to the changes.

### Tools
- `intelmq.bin.intelmqctl`:
  - check: Check if running the upgrade function for harmonization is necessary.
  - upgrade-config: Run the upgrade function for harmonization.
  - `intelmqctl restart` did throw an error as the message for restarting was not defined (#1465).

### Known issues
- MongoDB authentication: compatibility on different MongoDB and pymongo versions (#1439)
- ctl: shell colorizations are logged (#1436)
- http stream collector: retry on regular connection problems? (#1435)
- tests: capture logging with context manager (#1342)
- Bots started with IntelMQ-Manager stop when the webserver is restarted. (#952)
- n6 parser: mapping is modified within each run (#905)
- reverse DNS: Only first record is used (#877)
- Corrupt dump files when interrupted during writing (#870)


2.1.0 (2019-10-15)
-----------------

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
  - Add `reject_message` method to the Pipeline class for explicit re-queue of messages.
  - AMQP:
    - Make exchange configurable.
    - If exchange is set, the queues are not declared, the queue name is for routing used by exchanges.
- `intelmq.lib.bot`:
  - Log message after successful bot initialization, no log message anymore for ready pipeline.
  - Use existing current message if receive is called and the current message still exists.
  - Fix handling of received messaged after a SIGHUP that happened during a blocking receiving connection using explicit rejection (#1438).
  - New method `_parse_common_parameters` called before `init` to parse commonly used argument. Currently supported: `extract_files`.
- `intelmq.lib.test`:
  - Fix the tests broker by providing the testing pipeline.
- `intelmq.lib.utils`:
  - `unzip`:
    - new parameter `return_names` to optionally return the file names.
    - support for zip
    - new parameters `try_zip`, `try_gzip` and `try_tar` to control which compressions are tried.
    - rewritten to an iterative approach
  - add `file_name_from_response` to extract a file name from a Response object for downloaded files.
- `intelmq.lib.upgrades`: Added `v210_deprecations` for deprecated parameters.

### Harmonization
- Add extra to reports.

### Bots
#### Collectors
- `intelmq.bots.collectors.http.collector_http`:
  - More extensive usage of `intelmq.lib.utils.unzip`.
  - Save the file names in the report if files have been extracted form an archive.
- `intelmq.bots.collectors.rt.collector_rt`:
  - Save ticket information/metadata in the extra fields of the report.
  - Support for RT 3.8 and RT 4.4.
  - New parameters `extract_attachment` and `extract_download` for generic archive extraction and consistency. The parameter `unzip_attachment` is deprecated.
- `intelmq.bots.collectors.mail.*`: Save email information/metadata in the extra fields of the report. See the bots documentation for a complete list of provided data.
  - `intelmq.bots.collectors.mail.collector_mail_attach`: Check for existence/validity of the `attach_regex` parameter.
  - Use the lib's `unzip` function for uncompressing attachments and use the .
  - `intelmq.bots.collectors.mail.collector_mail_url`: Save the file name of the downloaded file as `extra.file_name`.
- `intelmq.bots.collectors.amqp.collector_amqp`: New collector to collect data from (remote) AMQP servers, for bot IntelMQ as well as external data.
  - use default SSL context for client purposes, fixes compatibility with python `<` 3.6 if TLS is used.

#### Parsers
- `intelmq.bot.parsers.html_table.parser`:
  * New parameter "html_parser".
  * Use time conversion functions directly from `intelmq.lib.harmonization.DateTime.convert`.
  - Limit lxml dependency on 3.4 to `<` 4.4.0 (incompatibility).
- `intelmq.bots.parsers.netlab_360.parser`: Add support for hajime scanners.
- `intelmq.bots.parsers.hibp.parser_callback`: A new parser to parse data retrieved from a HIBP Enterprise Subscription.
- `intelmq.bots.parsers.shadowserver.parser`:
  - Ability to detect the feed base on the reports's field `extra.file_name`, so the parameter `feedname` is no longer required and one configured parser can parse any feed (#1442).

#### Experts
- Add geohash expert.
- `intelmq.bot.experts.generic_db_lookup.expert`
  - new optional parameter `engine` with `postgresql` (default) and `sqlite` (new) as possible values.

#### Outputs
- Add `intelmq.bots.outputs.touch.output`.
- `intelmq.bot.outputs.postgresql.output`:
  - deprecated in favor of `intelmq.bot.outputs.sql.output`
  - Compatibility shim will be available in the 2.x series.
- `intelmq.bot.outputs.sql.output` added generic SQL output bot. Comparted to
  - new optional parameter `engine` with `postgresql` (default) and `sqlite` (new) as possible values.
- `intelmq.bots.outputs.stomp.output`: New parameters `message_hierarchical`, `message_jsondict_as_string`, `message_with_type`, `single_key`.

### Documentation
- Feeds:
  - Add ViriBack feed.
  - Add Have I Been Pwned Enterprise Callback.
- `intelmq.tests.bots.outputs.amqptopic.test_output`: Added.
- Move the documentation of most bots from separate README files to the central Bots.md and feeds.yaml files.

### Tests
- Travis:
  - Use UTC timezone.
- Tests for `utils.unzip`.
- Add a new asset: Zip archive with two files, same as with `.tar.gz` archive.
- Added tests for the Mail Attachment & Mail URL collectors.
- Ignore logging-tests on Python 3.7 temporarily (#1342).

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
- MongoDB authentication: compatibility on different MongoDB and pymongo versions (#1439)
- ctl: shell colorizations are logged (#1436)
- http stream collector: retry on regular connection problems? (#1435)
- tests: capture logging with context manager (#1342)
- Bots started with IntelMQ-Manager stop when the webserver is restarted. (#952)
- n6 parser: mapping is modified within each run (#905)
- reverse DNS: Only first record is used (#877)
- Corrupt dump files when interrupted during writing (#870)


2.0.2 (2019-10-14)
-----------------

### Core
- `intelmq.lib.bot.CollectorBot`: Support the deprecated parameter `feed` until version 2.2 as the documentation was not properly updated (#1445).
- `intelmq.lib.bot.Bot`:
  - `_dump_message`: Wait for up to 60 seconds instead of 50 if the dump file is locked (the log message was said 60, but the code was for only 50).
- `intelmq.lib.upgrades.v202_fixes`
  - Migration of deprecated parameter `feed` for Collectors.
  - Ripe expert parameter `query_ripe_stat_ip` was not correctly configured in `v110_deprecations`, now use `query_ripe_stat_asn` as default if it does not exist.
- `intelmq.lib.upgrades.v110_deprecations`: Fix upgrade of ripe expert configuration.
- `intelmq.lib.bot_debugger`:
  - Fix handling of empty messages generated by parser when user wanted to show the result by "--show-sent" flag.
  - Fix handling of sent messages for bots using the `path_permissive` parameter (#1453).
- `intelmq.lib.pipeline.Amqp`:
  - use default SSL context for client purposes, fixes compatibility with python `<` 3.6 if TLS is used.
  - Reconnect once on sending messages if disconnect detected.

### Bots
#### Collectors
- `intelmq.bots.collectors.api.collector_api`:
  - Handle non-existing IO loop in shutdown.
  - Close socket on shutdown, fixes reloading.
  - Marked as non-threadable.
- `intelmq.bots.collectors.rt.collector_rt`: Check for matching URLs if no `attachment_regex` is given.
- `intelmq.bots.collectors.stomp.collector_stomp`: Handle disconnects by actively reconnecting.

#### Parsers
- `intelmq.bots.cymru.parser_cap_program`: Fix parsing of the new `$certname_$date.txt` report format (#1443):
  - Support protocol ICMP.
  - Fix error message for unsupported protocols.
  - Support fields `destination_port_numbers`, `port`.
  - Support for all proxy types without ports.
  - Use Country Code of AS as `source.geolocation.cc`.
  - Support for 'scanner' and 'spam' categories.
  - Handle bogus lines with missing separator.
  - Fix bug preventing use of old format after using the new format.
  - Handle postfix ` (total_count:..)` for destination port numbers.

#### Experts
- `intelmq.bots.experts.cymru_whois.expert`: Add optional parameter `overwrite`, current behavior was `True`, default if not given is `True` now, will change to `False` in 3.0.0 (#1452, #1455).
- `intelmq.bots.experts.modify.expert`: Add optional parameter `overwrite`, current behavior was `True`, default if not given is `True` now, will change to `False` in 3.0.0 (#1452, #1455).
- `intelmq.bots.experts.reverse_dns.expert`: Add optional parameter `overwrite`, current behavior was `True`, default if not given is `True` now, will change to `False` in 3.0.0 (#1452, #1455).

#### Outputs
- `intelmq.bots.outputs.amqptopic.output`: use default SSL context for client purposes, fixes compatibility with python `<` 3.6 if TLS is used.

### Packaging
- Rules:
  - Exclude intelmqsetup tool in packages
  - Include update-rfiprisk-data in packages

### Tests
- Tests for `intelmq.lib.upgrades.v202_fixes`.
- Tests for `intelmq.lib.upgrades.v110_deprecations`.
- Extended tests for `intelmq.bots.parser.cymru.parser_cap_program`.

### Tools
- intelmqctl:
  - More and more precise logging messages for botnet starting and restarting, enable and disable.
  - No error message for disabled bots on botnet reload.
  - Fix `upgrade-conf` is state file is empty or not existing.
  - Use arpgarse's `store_true` action for flags instead of `store_const`.
  - If the loading of the defaults configuration failed, a variable definition was missing and causing an exception (#1456).

### Contrib
- Check MK Statistics Cronjob:
  - Use `statistics_*` parameters.
  - Make file executable
  - Handle None values in `*.temporary.*` keys and treat them as 0.
- systemd:
  - Add `PIDFile` parameter to service file.

### Known issues
- MongoDB authentication: compatibility on different MongoDB and pymongo versions (#1439)
- ctl: shell colorizations are logged (#1436)
- http stream collector: retry on regular connection problems? (#1435)
- tests: capture logging with context manager (#1342)
- Bots started with IntelMQ-Manager stop when the webserver is restarted. (#952)
- n6 parser: mapping is modified within each run (#905)
- reverse DNS: Only first record is used (#877)
- Corrupt dump files when interrupted during writing (#870)


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
- Do not execute the tcp collector tests during Debian and Ubuntu builds as they fail there.

### Tests
- `intelmq.lib.test`: Disable statistics for test runs of bots.
- `contrib.malware_name_mapping`: Added tests.
- Travis: Also run tests of contrib.

### Tools
- `intelmqsetup`: Only change directory ownerships if necessary.
- `intelmqctl`:/**---
  - Provide new command `upgrade-conf` to upgrade configuration to a newer version.
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
- Use the new RSIT types in several bots, see above

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
  - Dump messages locks the dump file using Unix file locks (#574).
  - Print idle/rate limit time also in human readable format (#1332).
  - `set_request_parameters`: Use `{}` as default proxy value instead of `None`. Allows updating of existing proxy dictionaries.
  - Bots drop privileges if they run as root.
  - Save statistics on successfully and failed processed messages in the redis database 3.
- `lib/utils`
  - Function `unzip` to extract files from gz-zipped and/or tar-archives.
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
  - Add support for uncompressing of gz-zipped-files (#1270).
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
- `intelmqctl run`: The message that a running bot has been stopped, is not longer a warning, but an informational message. No need to inform sysadmins about this intended behavior.
- `intelmqdump`: Inspecting dumps locks the dump file using unix file locks (#574).
- `intelmqctl`:
  - After the check if the program runs as root, it tries to drop privileges. Only if this does not work, a warning is shown.
- `intelmqsetup`: New tool for initializing an IntelMQ environment.

### Contrib
- `malware_name_mapping`:
  - Added the script `apply_mapping_eventdb.py` to apply the mapping to an EventDB.
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
  - Use logging level from defaults configuration if possible, otherwise intelmq's internal default. Previously, DEBUG was used unconditionally.

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
- `intelmq_gen_feeds_docs` added to bin directory, allows generating the Feeds.md documentation file from feeds.yaml
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
- `intelmqctl list queues`: don't display named paths among standard queues.
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
- Replaced various occurrences of `self.logger.error()` + `self.stop()` with `raise ValueError`.

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
- Requests is no longer listed as dependency of the core. For depending bots the requirement is noted in their `REQUIREMENTS.txt` file.

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
  - `intelmqctl run [bot-id] message send` can now send report messages (#1077).
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
  - warnings of bots are caught by the logger (#1074, #1113).
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
- Fixes a thrown `FileNotFound` exception when stopping bots started with `intelmqctl run ...`

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
- HTTP collectors: If `http_username` and `http_password` are both given and empty or null, 'None:None' has been used to authenticate. It is now checked that the username evaluates to non-false/null before adding the authentication. (fixes #1017)
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
   This setting is honored by `bots.collectors.http.*` and `bots.collectors.mail.collector_mail_url`, `bots.collectors.rt` (only `http_timeout_sec`), `bots.outputs.restapi.output` and `bots.experts.ripencc_abuse_contact`.

### Documentation
- Minor fixes
- Dropped install scripts, see INSTALL.md for more detailed instructions and explanations
- Better structure of INSTALL.md
- Better documentation of packages

### Tools
- added a bot debugger (#975)
- missing bot executable is detected and handled by intelmqctl (#979)

### Core
- fix bug which prevented dumps to be written if the file did not exist (#986)
- Fix reload of bots regarding logging
- type annotations for all core libraries

### Bots
- added `bots.experts.idea`, bots.outputs.files
- possibility to split large csv Reports into Chunks, currently possible for mail url and file collector
- elasticsearch output supports HTTP Basic Auth
- `bots.collectors.mail.collector_mail_url` and bots collectors.file.collector can split large reports (#680)
- `bots.parsers.shadowserver` support the VNC feed
- handling of HTTP timeouts, see above #859
- `bots.parsers.bambenek` saves the malware name
- `bots.parsers.fraunhofer.parser_dga` saves the malware name
- `bots.parsers.shadowserver` handles NULL bytes
- `bots.parsers.abusech.parser_ransomware` handles the IP 0.0.0.0 specially

### Harmonization
- New field named `output` to support export to foreign formats

v1.0.0.dev7 Beta release (2017-05-09)
-------------------------------------

### Documentation
- more verbose installation and upgrade instructions

### Bots
#### Collectors
- `bots.collectors.alienvault_otx`: OTX library has been removed, install it as package instead

#### Parsers
- API keys will be removed from feed.url if possible
- `intelmq.bots.parsers.shadowserver.config`:
  - Added support for Compromised-Website, Open-Netis, NTP-Version, Sandbox-URL, Spam-URL, Vulnerable-ISAKMP, Botnet-CCIP, Accessible-RDP, Open-LDAP, Blacklisted-IP, Accessible-Telnet, Accessible-CWMP (#748).

#### Experts
- added `bots.experts.field_reducer`, `bots.outputs.smtp`.
- `bots.experts.deduplicator`: `ignore_keys` has been renamed to `filter_keys` and `filter_type` has been removed.
- `bots.experts.modify`: The configuration is now list-based for a consistent ordering.
- `bots.experts.tor_node` as an optional parameter `overwrite`.

### Harmonization
- New parameter and field named feed.documentation to link to documentation of the feed
- `classification.taxonomy` is lower case only

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
- DEV: `intelmq_gen_harm_docs`: added to generate Harmonization documentation
- `intelmq_psql_initdb`: creates a table for a postgresql database using the harmonization fields
- intelmqctl: reworked argument parsing, many bugfixes
- intelmqdump: added to inspect dumped messages and reinsert them into the queues
- DEV: `rewrite_config_files`: added to rewrite configuration files with consistent style


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
- renamed `intelmq.bots.parsers.spamhaus.parser` to `intelmq.bots.parsers.spamhaus.parser_drop`.
  renamed `intelmq.bots.parsers.malwarepatrol.parser-dansguardian to `intelmq.bots.parsers.malwarepatrol.parser_dansguardian`
- renamed `intelmq.bots.parsers.taichungcitynetflow.parser to `intelmq.bots.parsers.taichung.parser`
- major rework of shadowserver parsers
- enhanced all parsers

#### Experts
- Added experts: asnlookup, cert.at contact lookup, filter, generic db lookup, gethostbyname, modify, reverse dns, rfc1918, tor_nodes, url2fqdn
- removed experts: contactdb, countrycodefilter (obsolete), sanitizer (obsolete)
- renamed `intelmq.bots.experts.abusix.abusix` to `intelmq.bots.experts.abusix.expert`
  `intelmq.bots.experts.asnlookup.asnlookup` to `intelmq.bots.experts.asn_lookup.expert`
  `intelmq.bots.experts.cymru.expert` to `intelmq.bots.experts.cymru_whois.expert`
  `intelmq.bots.experts.deduplicator.deduplicator` to `intelmq.bots.experts.deduplicator.expert`
  `intelmq.bots.experts.geoip.geopip` to `intelmq.bots.experts.maxmind_geoip.expert`
  `intelmq.bots.experts.ripencc.ripencc` to `intelmq.bots.experts.ripencc_abuse_contact.expert`
  `intelmq.bots.experts.taxonomy.taxonomy` to `intelmq.bots.experts.taxonomy.expert`
- enhanced all experts
- changed configuration syntax for `intelmq.bots.experts.modify` to a more simple variant

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
