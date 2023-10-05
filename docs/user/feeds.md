<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
   
   This document is automatically generated. To add feeds here you need to edit `intelmq/etc/feeds.yaml`
   file and rebuild the documentation.
-->

# Feeds

The available feeds are grouped by the provider of the feeds.
For each feed the collector and parser that can be used is documented as well as any feed-specific parameters.
To add feeds to this file add them to `intelmq/etc/feeds.yaml` and then rebuild the documentation.

## Abuse.ch

### Feodo Tracker

List of botnet Command & Control servers (C&Cs) tracked by Feodo Tracker, associated with Dridex and Emotet (aka Heodo).

**Public:** yes

**Revision:** 2022-11-15

**Documentation:** <https://feodotracker.abuse.ch/>

**Additional Information:** The data in the column Last Online is used for `time.source` if available, with 00:00 as time. Otherwise first_seen is used as `time.source`.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://feodotracker.abuse.ch/downloads/ipblocklist.json
  name: Feodo Tracker
  provider: Abuse.ch
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.abusech.parser_feodotracker
```

---


### URLhaus

URLhaus is a project from abuse.ch with the goal of sharing malicious URLs that are being used for malware distribution. URLhaus offers a country, ASN (AS number) and Top Level Domain (TLD) feed for network operators / Internet Service Providers (ISPs), Computer Emergency Response Teams (CERTs) and domain registries.

**Public:** yes

**Revision:** 2020-07-07

**Documentation:** <https://urlhaus.abuse.ch/feeds/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://urlhaus.abuse.ch/feeds/tld/<TLD>/, https://urlhaus.abuse.ch/feeds/country/<CC>/, or https://urlhaus.abuse.ch/feeds/asn/<ASN>/
  name: URLhaus
  provider: Abuse.ch
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.generic.parser_csv
parameters:
  columns: ["time.source", "source.url", "status", "classification.type|__IGNORE__", "source.fqdn|__IGNORE__", "source.ip", "source.asn", "source.geolocation.cc"]
  default_url_protocol: http://
  delimiter: ,
  skip_header: False
  type_translation: [{"malware_download": "malware-distribution"}]
```

---


## AlienVault

### OTX

AlienVault OTX Collector is the bot responsible to get the report through the API. Report could vary according to subscriptions.

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <https://otx.alienvault.com/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.alienvault_otx.collector
parameters:
  api_key: {{ your API key }}
  name: OTX
  provider: AlienVault
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.alienvault.parser_otx
```

---


### Reputation List

List of malicious IPs.

**Public:** yes

**Revision:** 2018-01-20


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://reputation.alienvault.com/reputation.data
  name: Reputation List
  provider: AlienVault
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.alienvault.parser
```

---


## AnubisNetworks

### Cyberfeed Stream

Fetches and parsers the Cyberfeed data stream.

**Public:** no

**Revision:** 2020-06-15

**Documentation:** <https://www.anubisnetworks.com/ https://www.bitsight.com/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http_stream
parameters:
  http_url: https://prod.cyberfeed.net/stream?key={{ your API key }}
  name: Cyberfeed Stream
  provider: AnubisNetworks
  strip_lines: true
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.anubisnetworks.parser
parameters:
  use_malware_familiy_as_classification_identifier: True
```

---


## Bambenek

### C2 Domains

Master Feed of known, active and non-sinkholed C&Cs domain names. Requires access credentials.

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <https://osint.bambenekconsulting.com/feeds/>

**Additional Information:** License: https://osint.bambenekconsulting.com/license.txt


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_password: __PASSWORD__
  http_url: https://faf.bambenekconsulting.com/feeds/c2-dommasterlist.txt
  http_username: __USERNAME__
  name: C2 Domains
  provider: Bambenek
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.bambenek.parser
```

---


### C2 IPs

Master Feed of known, active and non-sinkholed C&Cs IP addresses. Requires access credentials.

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <https://osint.bambenekconsulting.com/feeds/>

**Additional Information:** License: https://osint.bambenekconsulting.com/license.txt


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_password: __PASSWORD__
  http_url: https://faf.bambenekconsulting.com/feeds/c2-ipmasterlist.txt
  http_username: __USERNAME__
  name: C2 IPs
  provider: Bambenek
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.bambenek.parser
```

---


### DGA Domains

Domain feed of known DGA domains from -2 to +3 days

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://osint.bambenekconsulting.com/feeds/>

**Additional Information:** License: https://osint.bambenekconsulting.com/license.txt


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://faf.bambenekconsulting.com/feeds/dga-feed.txt
  name: DGA Domains
  provider: Bambenek
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.bambenek.parser
```

---


## Benkow

### Malware Panels Tracker

Benkow Panels tracker is a list of fresh panel from various malware. The feed is available on the webpage: http://benkow.cc/passwords.php

**Public:** yes

**Revision:** 2022-11-16


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: http://benkow.cc/export.php
  name: Malware Panels Tracker
  provider: Benkow
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.generic.parser_csv
parameters:
  columns: ["__IGNORE__", "malware.name", "source.url", "source.fqdn|source.ip", "time.source"]
  columns_required: [false, true, true, false, true]
  defaults_fields: {'classification.type': 'c2-server'}
  delimiter: ;
  skip_header: True
```

---


## Blocklist.de

### Apache

Blocklist.DE Apache Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service Apache, Apache-DDOS, RFI-Attacks.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://www.blocklist.de/en/export.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://lists.blocklist.de/lists/apache.txt
  name: Apache
  provider: Blocklist.de
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.blocklistde.parser
```

---


### Bots

Blocklist.DE Bots Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks attacks on the RFI-Attacks, REG-Bots, IRC-Bots or BadBots (BadBots = he has posted a Spam-Comment on a open Forum or Wiki).

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://www.blocklist.de/en/export.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://lists.blocklist.de/lists/bots.txt
  name: Bots
  provider: Blocklist.de
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.blocklistde.parser
```

---


### Brute-force Logins

Blocklist.DE Brute-force Login Collector is the bot responsible to get the report from source of information. All IPs which attacks Joomlas, Wordpress and other Web-Logins with Brute-Force Logins.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://www.blocklist.de/en/export.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://lists.blocklist.de/lists/bruteforcelogin.txt
  name: Brute-force Logins
  provider: Blocklist.de
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.blocklistde.parser
```

---


### FTP

Blocklist.DE FTP Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours for attacks on the Service FTP.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://www.blocklist.de/en/export.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://lists.blocklist.de/lists/ftp.txt
  name: FTP
  provider: Blocklist.de
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.blocklistde.parser
```

---


### IMAP

Blocklist.DE IMAP Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours for attacks on the service like IMAP, SASL, POP3, etc.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://www.blocklist.de/en/export.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://lists.blocklist.de/lists/imap.txt
  name: IMAP
  provider: Blocklist.de
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.blocklistde.parser
```

---


### IRC Bots

No description provided by feed provider.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://www.blocklist.de/en/export.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://lists.blocklist.de/lists/ircbot.txt
  name: IRC Bots
  provider: Blocklist.de
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.blocklistde.parser
```

---


### Mail

Blocklist.DE Mail Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service Mail, Postfix.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://www.blocklist.de/en/export.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://lists.blocklist.de/lists/mail.txt
  name: Mail
  provider: Blocklist.de
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.blocklistde.parser
```

---


### SIP

Blocklist.DE SIP Collector is the bot responsible to get the report from source of information. All IP addresses that tried to login in a SIP-, VOIP- or Asterisk-Server and are included in the IPs-List from http://www.infiltrated.net/ (Twitter).

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://www.blocklist.de/en/export.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://lists.blocklist.de/lists/sip.txt
  name: SIP
  provider: Blocklist.de
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.blocklistde.parser
```

---


### SSH

Blocklist.DE SSH Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service SSH.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://www.blocklist.de/en/export.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://lists.blocklist.de/lists/ssh.txt
  name: SSH
  provider: Blocklist.de
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.blocklistde.parser
```

---


### Strong IPs

Blocklist.DE Strong IPs Collector is the bot responsible to get the report from source of information. All IPs which are older then 2 month and have more then 5.000 attacks.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://www.blocklist.de/en/export.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://lists.blocklist.de/lists/strongips.txt
  name: Strong IPs
  provider: Blocklist.de
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.blocklistde.parser
```

---


## Blueliv

### CrimeServer

Blueliv Crimeserver Collector is the bot responsible to get the report through the API.

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <https://www.blueliv.com/>

**Additional Information:** The service uses a different API for free users and paying subscribers. In 'CrimeServer' feed the difference lies in the data points present in the feed. The non-free API available from Blueliv contains, for this specific feed, following extra fields not present in the free API; "_id" - Internal unique ID "subType" - Subtype of the Crime Server "countryName" - Country name where the Crime Server is located, in English "city" - City where the Crime Server is located "domain" - Domain of the Crime Server "host" - Host of the Crime Server "createdAt" - Date when the Crime Server was added to Blueliv CrimeServer database "asnCidr" - Range of IPs that belong to an ISP (registered via Autonomous System Number (ASN)) "asnId" - Identifier of an ISP registered via ASN "asnDesc" Description of the ISP registered via ASN


**Collector configuration**

```yaml
module: intelmq.bots.collectors.blueliv.collector_crimeserver
parameters:
  api_key: __APIKEY__
  name: CrimeServer
  provider: Blueliv
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.blueliv.parser_crimeserver
```

---


## CERT-Bund

### CB-Report Malware infections via IMAP

CERT-Bund sends reports for the malware-infected hosts.

**Public:** no

**Revision:** 2020-08-20

**Additional Information:** Traffic from malware related hosts contacting command-and-control servers is caught and sent to national CERT teams. There are two e-mail feeds with identical CSV structure -- one reports on general malware infections, the other on the Avalanche botnet.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.mail.collector_mail_attach
parameters:
  attach_regex: events.csv
  extract_files: False
  folder: INBOX
  mail_host: __HOST__
  mail_password: __PASSWORD__
  mail_ssl: True
  mail_user: __USERNAME__
  name: CB-Report Malware infections via IMAP
  provider: CERT-Bund
  rate_limit: 86400
  subject_regex: ^\\[CB-Report#.* Malware infections (\\(Avalanche\\) )?in country
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.generic.parser_csv
parameters:
  columns: ["source.asn", "source.ip", "time.source", "classification.type", "malware.name", "source.port", "destination.ip", "destination.port", "destination.fqdn", "protocol.transport"]
  default_url_protocol: http://
  defaults_fields: {'classification.type': 'infected-system'}
  delimiter: ,
  skip_header: True
  time_format: from_format|%Y-%m-%d %H:%M:%S
```

---


## CERT.PL

### N6 Stomp Stream

N6 Collector - CERT.pl's *n6* Stream API feed (via STOMP interface). Note that 'rate_limit' does not apply to this bot, as it is waiting for messages on a stream.

**Public:** no

**Revision:** 2023-10-08

**Documentation:** <https://n6.readthedocs.io/usage/streamapi/>

**Additional Information:** Contact CERT.pl to get access to the feed. Note that the configuration parameter values suggested here are suitable for the new *n6* Stream API variant (with authentication based on 'username' and 'password'); for this variant, typically you can leave the 'ssl_ca_certificate' parameter's value empty - then the system's default CA certificates will be used; however, if that does not work, you need to set 'ssl_ca_certificate' to the path to a file containing CA certificates eligible to verify "*.cert.pl" server certificates (to be found among the publicly available CA certs distributed with modern web browsers/OSes). Also, note that the 'server' parameter's value (for the *new API variant*) suggested here, "n6stream-new.cert.pl", is a temporary domain; ultimately, it will be changed back to "stream.cert.pl". When it comes to the *old API variant* (turned off in November 2023!), you need to have the 'server' parameter set to the name "n6stream.cert.pl", 'auth_by_ssl_client_certificate' set to true, 'ssl_ca_certificate' set to the path to a file containing the *n6*'s legacy self-signed CA certificate (which is stored in file "intelmq/bots/collectors/stomp/ca.pem"), and the parameters 'ssl_client_certificate' and 'ssl_client_certificate_key' set to the paths to your-*n6*-client-specific certificate and key files (note that the 'username' and 'password' parameters are then irrelevant and can be omitted).


**Collector configuration**

```yaml
module: intelmq.bots.collectors.stomp.collector
parameters:
  auth_by_ssl_client_certificate: False
  exchange: {insert your STOMP *destination* to subscribe to, as given by CERT.pl, e.g. /exchange/my.example.org/*.*.*.*}
  name: N6 Stomp Stream
  password: {insert your *n6* API key}
  port: 61614
  provider: CERT.PL
  server: n6stream-new.cert.pl
  ssl_ca_certificate:
  username: {insert your *n6* login, e.g. someuser@my.example.org}
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.n6.parser_n6stomp
```

---


## CINS Army

### CINS Army List

The CINS Army (CIArmy.com) list is a subset of the CINS Active Threat Intelligence ruleset, and consists of IP addresses that meet one of two basic criteria: 1) The IP's recent Rogue Packet score factor is very poor, or 2) The IP has tripped a designated number of 'trusted' alerts across a given number of our Sentinels deployed around the world.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://cinsscore.com/#list>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: http://cinsscore.com/list/ci-badguys.txt
  name: CINS Army List
  provider: CINS Army
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.ci_army.parser
```

---


## CZ.NIC

### HaaS

SSH attackers against HaaS (Honeypot as a Service) provided by CZ.NIC, z.s.p.o. The dump is published once a day.

**Public:** yes

**Revision:** 2020-07-22

**Documentation:** <https://haas.nic.cz/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  extract_files: True
  http_url: https://haas.nic.cz/stats/export/{time[%Y/%m/%Y-%m-%d]}.json.gz
  http_url_formatting: {'days': -1}
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.cznic.parser_haas
```

---


### Proki

Aggregation of various sources on malicious IP addresses (malware spreaders or C&C servers).

**Public:** no

**Revision:** 2020-08-17

**Documentation:** <https://csirt.cz/en/proki/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://proki.csirt.cz/api/1/__APIKEY__/data/day/{time[%Y/%m/%d]}
  http_url_formatting: {'days': -1}
  name: Proki
  provider: CZ.NIC
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.cznic.parser_proki
```

---


## Calidog

### CertStream

HTTP Websocket Stream from certstream.calidog.io providing data from Certificate Transparency Logs.

**Public:** yes

**Revision:** 2018-06-15

**Documentation:** <https://medium.com/cali-dog-security/introducing-certstream-3fc13bb98067>

**Additional Information:** Be aware that this feed provides a lot of data and may overload your system quickly.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.calidog.collector_certstream
parameters:
  name: CertStream
  provider: Calidog
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.calidog.parser_certstream
```

---


## CleanMX

### Phishing

In order to download the CleanMX feed you need to use a custom user agent and register that user agent.

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <http://clean-mx.de/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_timeout_sec: 120
  http_url: http://support.clean-mx.de/clean-mx/xmlphishing?response=alive&domain=
  http_user_agent: {{ your user agent }}
  name: Phishing
  provider: CleanMX
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.cleanmx.parser
```

---


### Virus

In order to download the CleanMX feed you need to use a custom user agent and register that user agent.

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <http://clean-mx.de/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_timeout_sec: 120
  http_url: http://support.clean-mx.de/clean-mx/xmlviruses?response=alive&domain=
  http_user_agent: {{ your user agent }}
  name: Virus
  provider: CleanMX
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.cleanmx.parser
```

---


## CyberCrime Tracker

### Latest

C2 servers

**Public:** yes

**Revision:** 2019-03-19

**Documentation:** <https://cybercrime-tracker.net/index.php>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://cybercrime-tracker.net/index.php
  name: Latest
  provider: CyberCrime Tracker
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.html_table.parser
parameters:
  columns: ["time.source", "source.url", "source.ip", "malware.name", "__IGNORE__"]
  default_url_protocol: http://
  defaults_fields: {'classification.type': 'c2-server'}
  skip_table_head: True
```

---


## DShield

### AS Details

No description provided by feed provider.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://www.dshield.org/reports.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dshield.org/asdetailsascii.html?as={{ AS Number }}
  name: AS Details
  provider: DShield
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dshield.parser_asn
```

---


### Block

This list summarizes the top 20 attacking class C (/24) subnets over the last three days. The number of 'attacks' indicates the number of targets reporting scans from this subnet.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://www.dshield.org/reports.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://www.dshield.org/block.txt
  name: Block
  provider: DShield
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dshield.parser_block
```

---


## Danger Rulez

### Bruteforce Blocker

Its main purpose is to block SSH bruteforce attacks via firewall.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://danger.rulez.sk/index.php/bruteforceblocker/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: http://danger.rulez.sk/projects/bruteforceblocker/blist.php
  name: Bruteforce Blocker
  provider: Danger Rulez
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.danger_rulez.parser
```

---


## Dataplane

### DNS Recursion Desired

Entries consist of fields with identifying characteristics of a source IP address that has been seen performing a DNS recursion desired query to a remote host. This report lists hosts that are suspicious of more than just port scanning. The host may be DNS server cataloging or searching for hosts to use for DNS-based DDoS amplification.

**Public:** yes

**Revision:** 2021-09-09

**Documentation:** <https://dataplane.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dataplane.org/dnsrd.txt
  name: DNS Recursion Desired
  provider: Dataplane
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dataplane.parser
```

---


### DNS Recursion Desired ANY

Entries consist of fields with identifying characteristics of a source IP address that has been seen performing a DNS recursion desired IN ANY query to a remote host. This report lists hosts that are suspicious of more than just port scanning. The host may be DNS server cataloging or searching for hosts to use for DNS-based DDoS amplification.

**Public:** yes

**Revision:** 2021-09-09

**Documentation:** <https://dataplane.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dataplane.org/dnsrdany.txt
  name: DNS Recursion Desired ANY
  provider: Dataplane
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dataplane.parser
```

---


### DNS Version

Entries consist of fields with identifying characteristics of a source IP address that has been seen performing a DNS CH TXT version.bind query to a remote host. This report lists hosts that are suspicious of more than just port scanning. The host may be DNS server cataloging or searching for vulnerable DNS servers.

**Public:** yes

**Revision:** 2021-09-09

**Documentation:** <https://dataplane.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dataplane.org/dnsversion.txt
  name: DNS Version
  provider: Dataplane
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dataplane.parser
```

---


### Protocol 41

Entries consist of fields with identifying characteristics of a host that has been detected to offer open IPv6 over IPv4 tunneling. This could allow for the host to be used a public proxy against IPv6 hosts.

**Public:** yes

**Revision:** 2021-09-09

**Documentation:** <https://dataplane.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dataplane.org/proto41.txt
  name: Protocol 41
  provider: Dataplane
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dataplane.parser
```

---


### SIP Query

Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP OPTIONS query to a remote host. This report lists hosts that are suspicious of more than just port scanning. The hosts may be SIP server cataloging or conducting various forms of telephony abuse. Report is updated hourly.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://dataplane.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dataplane.org/sipquery.txt
  name: SIP Query
  provider: Dataplane
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dataplane.parser
```

---


### SIP Registration

Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP REGISTER operation to a remote host. This report lists hosts that are suspicious of more than just port scanning. The hosts may be SIP client cataloging or conducting various forms of telephony abuse. Report is updated hourly.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://dataplane.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dataplane.org/sipregistration.txt
  name: SIP Registration
  provider: Dataplane
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dataplane.parser
```

---


### SMTP Data

Entries consist of fields with identifying characteristics of a host that has been seen initiating a SMTP DATA operation to a remote host. The source report lists hosts that are suspicious of more than just port scanning. The host may be SMTP server cataloging or conducting various forms of email abuse.

**Public:** yes

**Revision:** 2021-09-09

**Documentation:** <https://dataplane.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dataplane.org/smtpdata.txt
  name: SMTP Data
  provider: Dataplane
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dataplane.parser
```

---


### SMTP Greet

Entries consist of fields with identifying characteristics of a host that has been seen initiating a SMTP HELO/EHLO operation to a remote host. The source report lists hosts that are suspicious of more than just port scanning. The host may be SMTP server cataloging or conducting various forms of email abuse.

**Public:** yes

**Revision:** 2021-09-09

**Documentation:** <https://dataplane.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dataplane.org/smtpgreet.txt
  name: SMTP Greet
  provider: Dataplane
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dataplane.parser
```

---


### SSH Client Connection

Entries below consist of fields with identifying characteristics of a source IP address that has been seen initiating an SSH connection to a remote host. This report lists hosts that are suspicious of more than just port scanning. The hosts may be SSH server cataloging or conducting authentication attack attempts. Report is updated hourly.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://dataplane.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dataplane.org/sshclient.txt
  name: SSH Client Connection
  provider: Dataplane
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dataplane.parser
```

---


### SSH Password Authentication

Entries below consist of fields with identifying characteristics of a source IP address that has been seen attempting to remotely login to a host using SSH password authentication. The report lists hosts that are highly suspicious and are likely conducting malicious SSH password authentication attacks. Report is updated hourly.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://dataplane.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dataplane.org/sshpwauth.txt
  name: SSH Password Authentication
  provider: Dataplane
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dataplane.parser
```

---


### Telnet Login

Entries consist of fields with identifying characteristics of a host that has been seen initiating a telnet connection to a remote host. The source report lists hosts that are suspicious of more than just port scanning. The host may be telnet server cataloging or conducting authentication attack attempts.

**Public:** yes

**Revision:** 2021-09-09

**Documentation:** <https://dataplane.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dataplane.org/telnetlogin.txt
  name: Telnet Login
  provider: Dataplane
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dataplane.parser
```

---


### VNC/RFB Login

Entries consist of fields with identifying characteristics of a host that has been seen initiating a VNC remote buffer session to a remote host. The source report lists hosts that are suspicious of more than just port scanning. The host may be VNC/RFB server cataloging or conducting authentication attack attempts.

**Public:** yes

**Revision:** 2021-09-09

**Documentation:** <https://dataplane.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://dataplane.org/vncrfb.txt
  name: VNC/RFB Login
  provider: Dataplane
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dataplane.parser
```

---


## ESET

### ETI Domains

Domain data from ESET's TAXII API.

**Public:** no

**Revision:** 2020-06-30

**Documentation:** <https://www.eset.com/int/business/services/threat-intelligence/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.eset.collector
parameters:
  collection: ei.domains v2 (json)
  endpoint: eti.eset.com
  password: <password>
  time_delta: 3600
  username: <username>
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.eset.parser
```

---


### ETI URLs

URL data from ESET's TAXII API.

**Public:** no

**Revision:** 2020-06-30

**Documentation:** <https://www.eset.com/int/business/services/threat-intelligence/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.eset.collector
parameters:
  collection: ei.urls (json)
  endpoint: eti.eset.com
  password: <password>
  time_delta: 3600
  username: <username>
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.eset.parser
```

---


## Fireeye

### Malware Analysis System

Process data from Fireeye mail and file analysis appliances. SHA1 and MD5 malware hashes are extracted and if there is network communication, also URLs and domains.

**Public:** no

**Revision:** 2021-05-03

**Documentation:** <https://www.fireeye.com/products/malware-analysis.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.fireeye.collector_mas
parameters:
  host: <hostname of your appliance>
  http_password: <your password>
  http_username: <your username>
  request_duration: <how old date should be fetched eg 24_hours or 48_hours>
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.fireeye.parser
```

---


## Fraunhofer

### DGA Archive

Fraunhofer DGA collector fetches data from Fraunhofer's domain generation archive.

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <https://dgarchive.caad.fkie.fraunhofer.de/welcome/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_password: {{ your password }}
  http_url: https://dgarchive.caad.fkie.fraunhofer.de/today
  http_username: {{ your username }}
  name: DGA Archive
  provider: Fraunhofer
  rate_limit: 10800
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.fraunhofer.parser_dga
```

---


## Have I Been Pwned

### Enterprise Callback

With the Enterprise Subscription of 'Have I Been Pwned' you are able to provide a callback URL and any new leak data is submitted to it. It is recommended to put a webserver with Authorization check, TLS etc. in front of the API collector.

**Public:** no

**Revision:** 2019-09-11

**Documentation:** <https://haveibeenpwned.com/EnterpriseSubscriber/>

**Additional Information:** A minimal nginx configuration could look like:
```
server {
    listen 443 ssl http2;
    server_name [your host name];
    client_max_body_size 50M;

    ssl_certificate [path to your key];
    ssl_certificate_key [path to your certificate];

    location /[your private url] {
         if ($http_authorization != '[your private password]') {
             return 403;
         }
         proxy_pass http://localhost:5001/intelmq/push;
         proxy_read_timeout 30;
         proxy_connect_timeout 30;
     }
}
```


**Collector configuration**

```yaml
module: intelmq.bots.collectors.api.collector_api
parameters:
  name: Enterprise Callback
  port: 5001
  provider: Have I Been Pwned
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.hibp.parser_callback
```

---


## MalwarePatrol

### DansGuardian

Malware block list with URLs

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <https://www.malwarepatrol.net/non-commercial/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://lists.malwarepatrol.net/cgi/getfile?receipt={{ your API key }}&product=8&list=dansguardian
  name: DansGuardian
  provider: MalwarePatrol
  rate_limit: 180000
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.malwarepatrol.parser_dansguardian
```

---


## MalwareURL

### Latest malicious activity

Latest malicious domains/IPs.

**Public:** yes

**Revision:** 2018-02-05

**Documentation:** <https://www.malwareurl.com/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://www.malwareurl.com/
  name: Latest malicious activity
  provider: MalwareURL
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.malwareurl.parser
```

---


## McAfee Advanced Threat Defense

### Sandbox Reports

Processes reports from McAfee's sandboxing solution via the openDXL API.

**Public:** no

**Revision:** 2018-07-05

**Documentation:** <https://www.mcafee.com/enterprise/en-us/products/advanced-threat-defense.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.opendxl.collector
parameters:
  dxl_config_file: {{ location of dxl configuration file }}
  dxl_topic: /mcafee/event/atd/file/report
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.mcafee.parser_atd
parameters:
  verdict_severity: 4
```

---


## Microsoft

### BingMURLs via Interflow

Collects Malicious URLs detected by Bing from the Interflow API. The feed is available via Microsoft’s Government Security Program (GSP).

**Public:** no

**Revision:** 2018-05-29

**Documentation:** <https://docs.microsoft.com/en-us/security/gsp/informationsharingandexchange>

**Additional Information:** Depending on the file sizes you may need to increase the parameter 'http_timeout_sec' of the collector.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.microsoft.collector_interflow
parameters:
  api_key: {{ your API key }}
  file_match: ^bingmurls_
  http_timeout_sec: 300
  name: BingMURLs via Interflow
  not_older_than: 2 days
  provider: Microsoft
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.microsoft.parser_bingmurls
```

---


### CTIP C2 via Azure

Collects the CTIP C2 feed from a shared Azure Storage. The feed is available via Microsoft’s Government Security Program (GSP).

**Public:** no

**Revision:** 2020-05-29

**Documentation:** <https://docs.microsoft.com/en-us/security/gsp/informationsharingandexchange>

**Additional Information:** The cache is needed for memorizing which files have already been processed, the TTL should be higher than the oldest file available in the storage (currently the last three days are available). The connection string contains endpoint as well as authentication information.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.microsoft.collector_azure
parameters:
  connection_string: {{ your connection string }}
  container_name: ctip-c2
  name: CTIP C2 via Azure
  provider: Microsoft
  rate_limit: 3600
  redis_cache_db: 5
  redis_cache_host: 127.0.0.1
  redis_cache_port: 6379
  redis_cache_ttl: 864000
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.microsoft.parser_ctip
```

---


### CTIP Infected via Azure

Collects the CTIP (Sinkhole data) from a shared Azure Storage. The feed is available via Microsoft’s Government Security Program (GSP).

**Public:** no

**Revision:** 2022-06-01

**Documentation:** <https://docs.microsoft.com/en-us/security/gsp/informationsharingandexchange http://www.dcuctip.com/>

**Additional Information:** The cache is needed for memorizing which files have already been processed, the TTL should be higher than the oldest file available in the storage (currently the last three days are available). The connection string contains endpoint as well as authentication information. As many IPs occur very often in the data, you may want to use a deduplicator specifically for the feed. More information about the feed can be found on www.dcuctip.com after login with your GSP account.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.microsoft.collector_azure
parameters:
  connection_string: {{ your connection string }}
  container_name: ctip-infected-summary
  name: CTIP Infected via Azure
  provider: Microsoft
  rate_limit: 3600
  redis_cache_db: 5
  redis_cache_host: 127.0.0.1
  redis_cache_port: 6379
  redis_cache_ttl: 864000
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.microsoft.parser_ctip
```

---


### CTIP Infected via Interflow

Collects the CTIP Infected feed (Sinkhole data for your country) files from the Interflow API.The feed is available via Microsoft’s Government Security Program (GSP).

**Public:** no

**Revision:** 2018-03-06

**Documentation:** <https://docs.microsoft.com/en-us/security/gsp/informationsharingandexchange http://www.dcuctip.com/>

**Additional Information:** Depending on the file sizes you may need to increase the parameter 'http_timeout_sec' of the collector. As many IPs occur very often in the data, you may want to use a deduplicator specifically for the feed. More information about the feed can be found on www.dcuctip.com after login with your GSP account.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.microsoft.collector_interflow
parameters:
  api_key: {{ your API key }}
  file_match: ^ctip_
  http_timeout_sec: 300
  name: CTIP Infected via Interflow
  not_older_than: 2 days
  provider: Microsoft
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.microsoft.parser_ctip
```

---


## Netlab 360

### DGA

This feed lists DGA family, Domain, Start and end of valid time(UTC) of a number of DGA families.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://data.netlab.360.com/dga>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: http://data.netlab.360.com/feeds/dga/dga.txt
  name: DGA
  provider: Netlab 360
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.netlab_360.parser
```

---


### Hajime Scanner

This feed lists IP address for know Hajime bots network. These IPs data are obtained by joining the DHT network and interacting with the Hajime node

**Public:** yes

**Revision:** 2019-08-01

**Documentation:** <https://data.netlab.360.com/hajime/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://data.netlab.360.com/feeds/hajime-scanner/bot.list
  name: Hajime Scanner
  provider: Netlab 360
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.netlab_360.parser
```

---


### Magnitude EK

This feed lists FQDN and possibly the URL used by Magnitude Exploit Kit. Information also includes the IP address used for the domain and last time seen.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://data.netlab.360.com/ek>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: http://data.netlab.360.com/feeds/ek/magnitude.txt
  name: Magnitude EK
  provider: Netlab 360
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.netlab_360.parser
```

---


## OpenPhish

### Premium Feed

OpenPhish is a fully automated self-contained platform for phishing intelligence. It identifies phishing sites and performs intelligence analysis in real time without human intervention and without using any external resources, such as blacklists.

**Public:** no

**Revision:** 2018-02-06

**Documentation:** <https://www.openphish.com/phishing_feeds.html>

**Additional Information:** Discounts available for Government and National CERTs a well as for Nonprofit and Not-for-Profit organizations.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_password: {{ your password }}
  http_url: https://openphish.com/prvt-intell/
  http_username: {{ your username }}
  name: Premium Feed
  provider: OpenPhish
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.openphish.parser_commercial
```

---


### Public feed

OpenPhish is a fully automated self-contained platform for phishing intelligence. It identifies phishing sites and performs intelligence analysis in real time without human intervention and without using any external resources, such as blacklists.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://www.openphish.com/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://www.openphish.com/feed.txt
  name: Public feed
  provider: OpenPhish
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.openphish.parser
```

---


## PhishTank

### Online

PhishTank is a collaborative clearing house for data and information about phishing on the Internet.

**Public:** no

**Revision:** 2022-11-21

**Documentation:** <https://www.phishtank.com/developer_info.php>

**Additional Information:** Updated hourly as per the documentation. Download is possible without API key, but limited to few downloads per day.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  extract_files: True
  http_url: https://data.phishtank.com/data/{{ your API key }}/online-valid.json.gz
  name: Online
  provider: PhishTank
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.phishtank.parser
```

---


## PrecisionSec

### Agent Tesla

Agent Tesla IoCs, URLs where the malware is hosted.

**Public:** yes

**Revision:** 2019-04-02

**Documentation:** <https://precisionsec.com/threat-intelligence-feeds/agent-tesla/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://precisionsec.com/threat-intelligence-feeds/agent-tesla/
  name: Agent Tesla
  provider: PrecisionSec
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.html_table.parser
parameters:
  columns: ["source.ip|source.url", "time.source"]
  default_url_protocol: http://
  defaults_fields: {'classification.type': 'malware-distribution'}
  skip_table_head: True
```

---


## Shadowserver

### Via API

Shadowserver sends out a variety of reports to subscribers, see documentation.

**Public:** no

**Revision:** 2020-01-08

**Documentation:** <https://www.shadowserver.org/what-we-do/network-reporting/api-documentation/>

**Additional Information:** This configuration fetches user-configurable reports from the Shadowserver Reports API. For a list of reports, have a look at the Shadowserver collector and parser documentation.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.shadowserver.collector_reports_api
parameters:
  api_key: <API key>
  country: <CC>
  rate_limit: 86400
  redis_cache_db: 12
  redis_cache_host: 127.0.0.1
  redis_cache_port: 6379
  redis_cache_ttl: 864000
  secret: <API secret>
  types: <single report or list of reports>
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.shadowserver.parser_json
```

---


### Via IMAP

Shadowserver sends out a variety of reports (see https://www.shadowserver.org/wiki/pmwiki.php/Services/Reports).

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <https://www.shadowserver.org/what-we-do/network-reporting/>

**Additional Information:** The configuration retrieves the data from a e-mails via IMAP from the attachments.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.mail.collector_mail_attach
parameters:
  attach_regex: csv.zip
  extract_files: True
  folder: INBOX
  mail_host: __HOST__
  mail_password: __PASSWORD__
  mail_ssl: True
  mail_user: __USERNAME__
  name: Via IMAP
  provider: Shadowserver
  rate_limit: 86400
  subject_regex: __REGEX__
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.shadowserver.parser
```

---


### Via Request Tracker

Shadowserver sends out a variety of reports (see https://www.shadowserver.org/wiki/pmwiki.php/Services/Reports).

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <https://www.shadowserver.org/what-we-do/network-reporting/>

**Additional Information:** The configuration retrieves the data from a RT/RTIR ticketing instance via the attachment or an download.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.rt.collector_rt
parameters:
  attachment_regex: \\.csv\\.zip$
  extract_attachment: True
  extract_download: False
  http_password: {{ your HTTP Authentication password or null }}
  http_username: {{ your HTTP Authentication username or null }}
  password: __PASSWORD__
  provider: Shadowserver
  rate_limit: 3600
  search_not_older_than: {{ relative time or null }}
  search_owner: nobody
  search_queue: Incident Reports
  search_requestor: autoreports@shadowserver.org
  search_status: new
  search_subject_like: \[__COUNTRY__\] Shadowserver __COUNTRY__
  set_status: open
  take_ticket: True
  uri: http://localhost/rt/REST/1.0
  url_regex: https://dl.shadowserver.org/[a-zA-Z0-9?_-]*
  user: __USERNAME__
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.shadowserver.parser
```

---


## Shodan

### Country Stream

Collects the Shodan stream for one or multiple countries from the Shodan API.

**Public:** no

**Revision:** 2021-03-22

**Documentation:** <https://developer.shodan.io/api/stream>

**Additional Information:** A Shodan account with streaming permissions is needed.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.shodan.collector_stream
parameters:
  api_key: <API key>
  countries: <comma-separated list of country codes>
  error_retry_delay: 0
  name: Country Stream
  provider: Shodan
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.shodan.parser
parameters:
  error_retry_delay: 0
  ignore_errors: False
  minimal_mode: False
```

---


## Spamhaus

### ASN Drop

ASN-DROP contains a list of Autonomous System Numbers controlled by spammers or cyber criminals, as well as "hijacked" ASNs. ASN-DROP can be used to filter BGP routes which are being used for malicious purposes.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://www.spamhaus.org/drop/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://www.spamhaus.org/drop/asndrop.txt
  name: ASN Drop
  provider: Spamhaus
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.spamhaus.parser_drop
```

---


### CERT

Spamhaus CERT Insight Portal. Access limited to CERTs and CSIRTs with national or regional responsibility. .

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <https://www.spamhaus.org/news/article/705/spamhaus-launches-cert-insight-portal>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: {{ your CERT portal URL }}
  name: CERT
  provider: Spamhaus
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.spamhaus.parser_cert
```

---


### Drop

The DROP list will not include any IP address space under the control of any legitimate network - even if being used by "the spammers from hell". DROP will only include netblocks allocated directly by an established Regional Internet Registry (RIR) or National Internet Registry (NIR) such as ARIN, RIPE, AFRINIC, APNIC, LACNIC or KRNIC or direct RIR allocations.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://www.spamhaus.org/drop/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://www.spamhaus.org/drop/drop.txt
  name: Drop
  provider: Spamhaus
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.spamhaus.parser_drop
```

---


### Dropv6

The DROPv6 list includes IPv6 ranges allocated to spammers or cyber criminals. DROPv6 will only include IPv6 netblocks allocated directly by an established Regional Internet Registry (RIR) or National Internet Registry (NIR) such as ARIN, RIPE, AFRINIC, APNIC, LACNIC or KRNIC or direct RIR allocations.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://www.spamhaus.org/drop/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://www.spamhaus.org/drop/dropv6.txt
  name: Dropv6
  provider: Spamhaus
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.spamhaus.parser_drop
```

---


### EDrop

EDROP is an extension of the DROP list that includes sub-allocated netblocks controlled by spammers or cyber criminals. EDROP is meant to be used in addition to the direct allocations on the DROP list.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://www.spamhaus.org/drop/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://www.spamhaus.org/drop/edrop.txt
  name: EDrop
  provider: Spamhaus
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.spamhaus.parser_drop
```

---


## Strangereal Intel

### DailyIOC

Daily IOC from tweets and articles

**Public:** yes

**Revision:** 2019-12-05

**Documentation:** <https://github.com/StrangerealIntel/DailyIOC>

**Additional Information:** collector's `extra_fields` parameter may be any of fields from the github `content API response <https://developer.github.com/v3/repos/contents/>`_


**Collector configuration**

```yaml
module: intelmq.bots.collectors.github_api.collector_github_contents_api
parameters:
  personal_access_token: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
  regex: .*.json
  repository: StrangerealIntel/DailyIOC
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.github_feed
```

---


## Sucuri

### Hidden IFrames

Latest hidden iframes identified on compromised web sites.

**Public:** yes

**Revision:** 2018-01-28

**Documentation:** <http://labs.sucuri.net/?malware>

**Additional Information:** Please note that the parser only extracts the hidden iframes  and the conditional redirects, not the encoded javascript.


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: http://labs.sucuri.net/?malware
  name: Hidden IFrames
  provider: Sucuri
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.sucuri.parser
```

---


## Surbl

### Malicious Domains

Detected malicious domains. Note that you have to opened up Sponsored Datafeed Service (SDS) access to the SURBL data via rsync for your IP address.

**Public:** no

**Revision:** 2018-09-04


**Collector configuration**

```yaml
module: intelmq.bots.collectors.rsync.collector_rsync
parameters:
  file: wild.surbl.org.rbldnsd
  rsync_path: blacksync.prolocation.net::surbl-wild/
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.surbl.parser
```

---


## Team Cymru

### CAP

Team Cymru provides daily lists of compromised or abused devices for the ASNs and/or netblocks with a CSIRT's jurisdiction. This includes such information as bot infected hosts, command and control systems, open resolvers, malware urls, phishing urls, and brute force attacks

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <https://www.team-cymru.com/CSIRT-AP.html https://www.cymru.com/$certname/report_info.txt>

**Additional Information:** "Two feeds types are offered:
 * The new https://www.cymru.com/$certname/$certname_{time[%Y%m%d]}.txt
 * and the old https://www.cymru.com/$certname/infected_{time[%Y%m%d]}.txt
 Both formats are supported by the parser and the new one is recommended.
 As of 2019-09-12 the old format will be retired soon."


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_password: {{ your password }}
  http_url: https://www.cymru.com/$certname/$certname_{time[%Y%m%d]}.txt
  http_url_formatting: True
  http_username: {{ your username }}
  name: CAP
  provider: Team Cymru
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.cymru.parser_cap_program
```

---


### Full Bogons IPv4

Fullbogons are a larger set which also includes IP space that has been allocated to an RIR, but not assigned by that RIR to an actual ISP or other end-user. IANA maintains a convenient IPv4 summary page listing allocated and reserved netblocks, and each RIR maintains a list of all prefixes that they have assigned to end-users. Our bogon reference pages include additional links and resources to assist those who wish to properly filter bogon prefixes within their networks.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://www.team-cymru.com/bogon-reference-http.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt
  name: Full Bogons IPv4
  provider: Team Cymru
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.cymru.parser_full_bogons
```

---


### Full Bogons IPv6

Fullbogons are a larger set which also includes IP space that has been allocated to an RIR, but not assigned by that RIR to an actual ISP or other end-user. IANA maintains a convenient IPv4 summary page listing allocated and reserved netblocks, and each RIR maintains a list of all prefixes that they have assigned to end-users. Our bogon reference pages include additional links and resources to assist those who wish to properly filter bogon prefixes within their networks.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://www.team-cymru.com/bogon-reference-http.html>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://www.team-cymru.org/Services/Bogons/fullbogons-ipv6.txt
  name: Full Bogons IPv6
  provider: Team Cymru
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.cymru.parser_full_bogons
```

---


## Threatminer

### Recent domains

Latest malicious domains.

**Public:** yes

**Revision:** 2018-02-06

**Documentation:** <https://www.threatminer.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://www.threatminer.org/
  name: Recent domains
  provider: Threatminer
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.threatminer.parser
```

---


## Turris

### Greylist

The data are processed and classified every week and behaviour of IP addresses that accessed a larger number of Turris routers is evaluated. The result is a list of addresses that have tried to obtain information about services on the router or tried to gain access to them. The list also contains a list of tags for each address which indicate what behaviour of the address was observed.

**Public:** yes

**Revision:** 2023-06-13

**Documentation:** <https://project.turris.cz/en/greylist>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://view.sentinel.turris.cz/greylist-data/greylist-latest.csv
  name: Greylist
  provider: Turris
  rate_limit: 43200
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.turris.parser
```

---


### Greylist with PGP signature verification

The data are processed and classified every week and behaviour of
IP addresses that accessed a larger number of Turris routers is evaluated.
The result is a list of addresses that have tried to obtain information about
services on the router or tried to gain access to them. The list also
contains a list of tags for each address which
indicate what behaviour of the address was observed.

The Turris Greylist feed provides PGP signatures for the provided files.
You will need to import the public PGP key from the linked documentation
page, currently available at
https://pgp.mit.edu/pks/lookup?op=vindex&search=0x10876666
or from below.
See the URL Fetcher Collector documentation for more information on
PGP signature verification.

PGP Public key:

```
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: SKS 1.1.6
Comment: Hostname: pgp.mit.edu

mQINBFRl7D8BEADaRFoDa/+r27Gtqrdn8sZL4aSYTU4Q3gDr3TfigK8H26Un/Y79a/DUL1o0
o8SRae3uwVcjJDHZ6KDnxThbqF7URfpuCcCYxOs8p/eu3dSueqEGTODHWF4ChIh2japJDc4t
3FQHbIh2e3GHotVqJGhvxMmWqBFoZ/mlWvhjs99FFBZ87qbUNk7l1UAGEXeWeECgz9nGox40
3YpCgEsnJJsKC53y5LD/wBf4z+z0GsLg2GMRejmPRgrkSE/d9VjF/+niifAj2ZVFoINSVjjI
8wQFc8qLiExdzwLdgc+ggdzk5scY3ugI5IBt1zflxMIOG4BxKj/5IWsnhKMG2NLVGUYOODoG
pKhcY0gCHypw1bmkp2m+BDVyg4KM2fFPgQ554DAX3xdukMCzzZyBxR3UdT4dN7xRVhpph3Y2
Amh1E/dpde9uwKFk1oRHkRZ3UT1XtpbXtFNY0wCiGXPt6KznJAJcomYFkeLHjJo3nMK0hISV
GSNetVLfNWlTkeo93E1innbSaDEN70H4jPivjdVjSrLtIGfr2IudUJI84dGmvMxssWuM2qdg
FSzoTHw9UE9KT3SltKPS+F7u9x3h1J492YaVDncATRjPZUBDhbvo6Pcezhup7XTnI3gbRQc2
oEUDb933nwuobHm3VsUcf9686v6j8TYehsbjk+zdA4BoS/IdCwARAQABtC5UdXJyaXMgR3Jl
eWxpc3QgR2VuZXJhdG9yIDxncmV5bGlzdEB0dXJyaXMuY3o+iQI4BBMBAgAiBQJUZew/AhsD
BgsJCAcDAgYVCAIJCgsEFgIDAQIeAQIXgAAKCRDAQrU3EIdmZoH4D/9Jo6j9RZxCAPTaQ9WZ
WOdb1Eqd/206bObEX+xJAago+8vuy+waatHYBM9/+yxh0SIg2g5whd6J7A++7ePpt5XzX6hq
bzdG8qGtsCRu+CpDJ40UwHep79Ck6O/A9KbZcZW1z/DhbYT3z/ZVWALy4RtgmyC67Vr+j/C7
KNQ529bs3kP9AzvEIeBC4wdKl8dUSuZIPFbgf565zRNKLtHVgVhiuDPcxKmBEl4/PLYF30a9
5Tgp8/PNa2qp1DV/EZjcsxvSRIZB3InGBvdKdSzvs4N/wLnKWedj1GGm7tJhSkJa4MLBSOIx
yamhTS/3A5Cd1qoDhLkp7DGVXSdgEtpoZDC0jR7nTS6pXojcgQaF7SfJ3cjZaLI5rjsx0YLk
G4PzonQKCAAQG1G9haCDniD8NrrkZ3eFiafoKEECRFETIG0BJHjPdSWcK9jtNCupBYb7JCiz
Q0hwLh2wrw/wCutQezD8XfsBFFIQC18TsJAVgdHLZnGYkd5dIbV/1scOcm52w6EGIeMBBYlB
J2+JNukH5sJDA6zAXNl2I1H1eZsP4+FSNIfB6LdovHVPAjn7qXCw3+IonnQK8+g8YJkbbhKJ
sPejfg+ndpe5u0zX+GvQCFBFu03muANA0Y/OOeGIQwU93d/akN0P1SRfq+bDXnkRIJQOD6XV
0ZPKVXlNOjy/z2iN2A==
=wjkM
-----END PGP PUBLIC KEY BLOCK-----
```


**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://project.turris.cz/en/greylist>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://www.turris.cz/greylist-data/greylist-latest.csv
  name: Greylist
  provider: Turris
  rate_limit: 43200
  signature_url: https://www.turris.cz/greylist-data/greylist-latest.csv.asc
  verify_pgp_signatures: True
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.turris.parser
```

---


## University of Toulouse

### Blacklist

Various blacklist feeds

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <https://dsi.ut-capitole.fr/blacklists/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  extract_files: true
  http_url: https://dsi.ut-capitole.fr/blacklists/download/{collection name}.tar.gz
  name: Blacklist
  provider: University of Toulouse
  rate_limit: 43200
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.generic.parser_csv
parameters:
  columns: {depends on a collection}
  defaults_fields: {'classification.type': '{depends on a collection}'}
  delimiter: false
```

---


## VXVault

### URLs

This feed provides IP addresses hosting Malware.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://vxvault.net/ViriList.php>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: http://vxvault.net/URL_List.php
  name: URLs
  provider: VXVault
  rate_limit: 3600
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.vxvault.parser
```

---


## ViriBack

### C2 Tracker

Latest detected C2 servers.

**Public:** yes

**Revision:** 2022-11-15

**Documentation:** <https://viriback.com/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://tracker.viriback.com/dump.php
  name: C2 Tracker
  provider: ViriBack
  rate_limit: 86400
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.generic.csv_parser
parameters:
  columns: ["malware.name", "source.url", "source.ip", "time.source"]
  defaults_fields: {'classification.type': 'malware-distribution'}
  skip_header: True
```

---


## WebInspektor

### Unsafe sites

Latest detected unsafe sites.

**Public:** yes

**Revision:** 2018-03-09


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: https://app.webinspector.com/public/recent_detections/
  name: Unsafe sites
  provider: WebInspektor
  rate_limit: 60
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.webinspektor.parser
```

---


## ZoneH

### Defacements

all the information contained in Zone-H's cybercrime archive were either collected online from public sources or directly notified anonymously to us.

**Public:** no

**Revision:** 2018-01-20

**Documentation:** <https://zone-h.org/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.mail.collector_mail_attach
parameters:
  attach_regex: csv
  extract_files: False
  folder: INBOX
  mail_host: __HOST__
  mail_password: __PASSWORD__
  mail_ssl: True
  mail_user: __USERNAME__
  name: Defacements
  provider: ZoneH
  rate_limit: 3600
  sent_from: datazh@zone-h.org
  subject_regex: Report
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.zoneh.parser
```

---


## cAPTure

### Ponmocup Domains CIF Format

List of ponmocup malware redirection domains and infected web-servers from cAPTure. See also http://security-research.dyndns.org/pub/botnet-links.htm and http://c-apt-ure.blogspot.com/search/label/ponmocup The data in the CIF format is not equal to the Shadowserver CSV format. Reasons are unknown.

**Public:** yes

**Revision:** 2018-01-20

**Documentation:** <http://security-research.dyndns.org/pub/malware-feeds/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: http://security-research.dyndns.org/pub/malware-feeds/ponmocup-infected-domains-CIF-latest.txt
  name: Infected Domains
  provider: cAPTure
  rate_limit: 10800
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.dyn.parser
```

---


### Ponmocup Domains Shadowserver Format

List of ponmocup malware redirection domains and infected web-servers from cAPTure. See also http://security-research.dyndns.org/pub/botnet-links.htm and http://c-apt-ure.blogspot.com/search/label/ponmocup The data in the Shadowserver CSV is not equal to the CIF format format. Reasons are unknown.

**Public:** yes

**Revision:** 2020-07-08

**Documentation:** <http://security-research.dyndns.org/pub/malware-feeds/>


**Collector configuration**

```yaml
module: intelmq.bots.collectors.http.collector_http
parameters:
  http_url: http://security-research.dyndns.org/pub/malware-feeds/ponmocup-infected-domains-shadowserver.csv
  name: Infected Domains
  provider: cAPTure
  rate_limit: 10800
```

**Parser configuration**

```yaml
module: intelmq.bots.parsers.generic.parser_csv
parameters:
  columns: ["time.source", "source.ip", "source.fqdn", "source.urlpath", "source.port", "protocol.application", "extra.tag", "extra.redirect_target", "extra.category"]
  compose_fields: {'source.url': 'http://{0}{1}'}
  defaults_fields: {'classification.type': 'malware-distribution'}
  delimiter: ,
  skip_header: True
```

---


