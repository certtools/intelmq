<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Aaron Kaplan, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Data Format

Data passed between bots is called a Message. There are two types of Messages: Report and Event. Report is produced by collector bots and consists of collected raw data (CSV, JSON, HTML, etc) and feed metadata. It is passed to a parser bot which parses Report into a single or multiple Events. Expert bots and output bots handle only Events.

All Messages (Reports and Events) are Python dictionaries (or JSONs). The key names and according types are defined by the IntelMQ Data Format.

The source code for the Data Format can be found in the Python module `intelmq.lib.harmonization` and the configuration is present inside the `harmonization.conf` file. (The term Harmonization is used for historical reasons.)

## Rules for keys

The keys are grouped together in sub-fields, e.g. `source.ip` or `source.geolocation.latitude`.

Only the lower-case alphabet, numbers and the underscore are allowed. Further, the field name must not begin with a
number. Thus, keys must match `^[a-z_][a-z_0-9]+(\.[a-z_0-9]+)*$`. These rules also apply for the otherwise
unregulated `extra.` namespace.

## Data Types

This document describes the IntelMQ data types used for individual events with a description of each allowed field.

### ASN

ASN type. Derived from Integer with forbidden values.

Only valid are: 0 < ASN <= 4294967295

See <https://en.wikipedia.org/wiki/Autonomous_system_(Internet)>

The first and last ASNs of the original 16-bit integers, namely 0 and 65,535, and the last ASN of the 32-bit numbers, namely 4,294,967,295 are reserved and should not be used by operators.


### Accuracy

Accuracy type. A Float between 0 and 100.


### Base64

Base64 type. Always gives unicode strings.

Sanitation encodes to base64 and accepts binary and unicode strings.


### Boolean

Boolean type. Without sanitation only python bool is accepted.

Sanitation accepts string 'true' and 'false' and integers 0 and 1.


### ClassificationTaxonomy

`classification.taxonomy` type.

The mapping follows Reference Security Incident Taxonomy Working Group – RSIT WG:
<https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/>

These old values are automatically mapped to the new ones:

- 'abusive content' -> 'abusive-content'
- 'information gathering' -> 'information-gathering'
- 'intrusion attempts' -> 'intrusion-attempts'
- 'malicious code' -> 'malicious-code'

Allowed values are:

- abusive-content
- availability
- fraud
- information-content-security
- information-gathering
- intrusion-attempts
- intrusions
- malicious-code
- other
- test
- vulnerable

### ClassificationType

`classification.type` type.

The mapping extends Reference Security Incident Taxonomy Working Group – RSIT WG:

<https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/>

These old values are automatically mapped to the new ones:

- 'botnet drone' -> 'infected-system'
- 'ids alert' -> 'ids-alert'
- 'c&c' -> 'c2-server'
- 'c2server' -> 'c2-server'
- 'infected system' -> 'infected-system'
- 'malware configuration' -> 'malware-configuration'
- 'Unauthorised-information-access' -> 'unauthorised-information-access'
- 'leak' -> 'data-leak'
- 'vulnerable client' -> 'vulnerable-system'
- 'vulnerable service' -> 'vulnerable-system'
- 'ransomware' -> 'infected-system'
- 'unknown' -> 'undetermined'

These values changed their taxonomy:
'malware': In terms of the taxonomy 'malicious-code' they can be either 'infected-system' or 'malware-distribution' but in terms of malware actually, it is now taxonomy 'other'

Allowed values are:

- application-compromise
- blacklist
- brute-force
- burglary
- c2-server
- copyright
- data-leak
- data-loss
- ddos
- ddos-amplifier
- dga-domain
- dos
- exploit
- harmful-speech
- ids-alert
- infected-system
- information-disclosure
- malware
- malware-configuration
- malware-distribution
- masquerade
- misconfiguration
- other
- outage
- phishing
- potentially-unwanted-accessible
- privileged-account-compromise
- proxy
- sabotage
- scanner
- sniffing
- social-engineering
- spam
- system-compromise
- test
- tor
- unauthorised-information-access
- unauthorised-information-modification
- unauthorized-use-of-resources
- undetermined
- unprivileged-account-compromise
- violence
- vulnerable-system
- weak-crypto

### DateTime

Date and time type for timestamps.

Valid values are timestamps with time zone and in the format '%Y-%m-%dT%H:%M:%S+00:00'.
Invalid are missing times and missing timezone information (UTC).
Microseconds are also allowed.

Sanitation normalizes the timezone to UTC, which is the only allowed timezone.

The following additional conversions are available with the convert function:

- `timestamp`
- `windows_nt`: From Windows NT / AD / LDAP
- `epoch_millis`: From Milliseconds since Epoch
- `from_format`: From a given format, eg. 'from_format|%H %M %S %m %d %Y %Z'
- `from_format_midnight`: Date from a given format and assume midnight, e.g. 'from_format_midnight|%d-%m-%Y'
- `utc_isoformat`: Parse date generated by datetime.isoformat()
- `fuzzy` (or None): Use dateutils' fuzzy parser, default if no specific parser is given


### FQDN

Fully qualified domain name type.

All valid lowercase domains are accepted, no IP addresses or URLs. Trailing
dot is not allowed.

To prevent values like '10.0.0.1:8080' (#1235), we check for the
non-existence of ':'.


### Float

Float type. Without sanitation only python float/integer/long is
accepted. Boolean is explicitly denied.

Sanitation accepts strings and everything float() accepts.


### IPAddress

Type for IP addresses, all families. Uses the ipaddress module.

Sanitation accepts integers, strings and objects of ipaddress.IPv4Address and ipaddress.IPv6Address.

Valid values are only strings. 0.0.0.0 is explicitly not allowed.


### IPNetwork

Type for IP networks, all families. Uses the ipaddress module.

Sanitation accepts strings and objects of ipaddress.IPv4Network and ipaddress.IPv6Network.
If host bits in strings are set, they will be ignored (e.g 127.0.0.1/32).

Valid values are only strings.


### Integer

Integer type. Without sanitation only python integer/long is accepted.
Bool is explicitly denied.

Sanitation accepts strings and everything int() accepts.


### JSON

JSON type.

Sanitation accepts any valid JSON objects.

Valid values are only unicode strings with JSON objects.


### JSONDict

JSONDict type.

Sanitation accepts pythons dictionaries and JSON strings.

Valid values are only unicode strings with JSON dictionaries.


### LowercaseString

Like string, but only allows lower case characters.

Sanitation lowers all characters.


### Registry

Registry type. Derived from UppercaseString.

Only valid values: AFRINIC, APNIC, ARIN, LACNIC, RIPE.
RIPE-NCC and RIPENCC are normalized to RIPE.


### String

Any non-empty string without leading or trailing whitespace.


### TLP

TLP level type. Derived from UppercaseString.

Only valid values: WHITE, GREEN, AMBER, RED.

Accepted for sanitation are different cases and the prefix 'tlp:'.


### URL

URI type. Local and remote.

Sanitation converts hxxp and hxxps to http and https.
For local URIs (file) a missing host is replaced by localhost.

Valid values must have the host (network location part).


### UppercaseString

Like string, but only allows upper case characters.

Sanitation uppers all characters.
