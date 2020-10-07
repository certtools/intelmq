# Available Feeds

The available feeds are grouped by the provider of the feeds.
For each feed the collector and parser that can be used is documented as well as any feed-specific parameters.
To add feeds to this file add them to `intelmq/etc/feeds.yaml` and then run
`intelmq/bin/intelmq_gen_feeds_docs.py` to generate the new content of this file.

<!-- TOC depthFrom:2 depthTo:2 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Abuse.ch](#abusech)
- [AlienVault](#alienvault)
- [AnubisNetworks](#anubisnetworks)
- [Autoshun](#autoshun)
- [Bambenek](#bambenek)
- [Blocklist.de](#blocklistde)
- [Blueliv](#blueliv)
- [CERT.PL](#certpl)
- [CINSscore](#cinsscore)
- [CZ.NIC](#cznic)
- [Calidog](#calidog)
- [CleanMX](#cleanmx)
- [CyberCrime Tracker](#cybercrime-tracker)
- [DShield](#dshield)
- [Danger Rulez](#danger-rulez)
- [Dataplane](#dataplane)
- [DynDNS](#dyndns)
- [ESET](#eset)
- [Fraunhofer](#fraunhofer)
- [Have I Been Pwned](#have-i-been-pwned)
- [Malc0de](#malc0de)
- [Malware Domain List](#malware-domain-list)
- [Malware Domains](#malware-domains)
- [MalwarePatrol](#malwarepatrol)
- [MalwareURL](#malwareurl)
- [McAfee Advanced Threat Defense](#mcafee-advanced-threat-defense)
- [Microsoft](#microsoft)
- [Netlab 360](#netlab-360)
- [OpenPhish](#openphish)
- [PhishTank](#phishtank)
- [PrecisionSec](#precisionsec)
- [ShadowServer](#shadowserver)
- [Spamhaus](#spamhaus)
- [Strangereal Intel](#strangereal-intel)
- [Sucuri](#sucuri)
- [Surbl](#surbl)
- [Taichung](#taichung)
- [Team Cymru](#team-cymru)
- [Threatminer](#threatminer)
- [Turris](#turris)
- [University of Toulouse](#university-of-toulouse)
- [VXVault](#vxvault)
- [ViriBack](#viriback)
- [WebInspektor](#webinspektor)
- [ZoneH](#zoneh)


<!-- /TOC -->


# Abuse.ch

## Feodo Tracker Browse

* **Public:** yes
* **Revision:** 2019-03-19
* **Documentation:** https://feodotracker.abuse.ch/browse
* **Description:**

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://feodotracker.abuse.ch/browse`
*  * `name`: `Feodo Tracker Browse`
*  * `provider`: `Abuse.ch`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** HTML Table (Module `intelmq.bots.parsers.html_table.parser`)
* **Configuration Parameters:**
*  * `columns`: `time.source,source.ip,malware.name,status,extra.SBL,source.as_name,source.geolocation.cc`
*  * `ignore_values`: `,,,,Not listed,,`
*  * `skip_table_head`: `True`
*  * `type`: `c2server`


## Feodo Tracker IPs

* **Public:** yes
* **Revision:** 2019-03-25
* **Documentation:** https://feodotracker.abuse.ch/
* **Description:** List of botnet Command&Control servers (C&Cs) tracked by Feodo Tracker, associated with Dridex and Emotet (aka Heodo).
* **Additional Information:** https://feodotracker.abuse.ch/ The data in the column Last Online is used for `time.source` if available, with 00:00 as time. Otherwise first seen is used as `time.source`.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://feodotracker.abuse.ch/downloads/ipblocklist.csv`
*  * `name`: `Feodo Tracker IPs`
*  * `provider`: `Abuse.ch`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Abuse.ch IP (Module `intelmq.bots.parsers.abusech.parser_ip`)
* **Configuration Parameters:**


## URLhaus

* **Public:** yes
* **Revision:** 2020-07-07
* **Documentation:** https://urlhaus.abuse.ch/feeds/
* **Description:** URLhaus is a project from abuse.ch with the goal of sharing malicious URLs that are being used for malware distribution. URLhaus offers a country, ASN (AS number) and Top Level Domain (TLD) feed for network operators / Internet Service Providers (ISPs), Computer Emergency Response Teams (CERTs) and domain registries.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://urlhaus.abuse.ch/feeds/tld/<TLD>/, https://urlhaus.abuse.ch/feeds/country/<CC>/, or https://urlhaus.abuse.ch/feeds/asn/<ASN>/`
*  * `name`: `URLhaus`
*  * `provider`: `Abuse.ch`
*  * `rate_limit`: `129600`

### Parser

* **Bot:** Generic CSV (Module `intelmq.bots.parsers.generic.parser_csv`)
* **Configuration Parameters:**
*  * `columns`: `["time.source", "source.url", "status", "classification.type|__IGNORE__", "source.fqdn|__IGNORE__", "source.ip", "source.asn", "source.geolocation.cc"]`
*  * `default_url_protocol`: `http://`
*  * `delimeter`: `,`
*  * `skip_header`: `False`
*  * `type_translation`: `{"malware_download": "malware-distribution"}`


# AlienVault

## OTX

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://otx.alienvault.com/
* **Description:** AlienVault OTX Collector is the bot responsible to get the report through the API. Report could vary according to subscriptions.

### Collector

* **Bot:** AlienVault OTX (Module `intelmq.bots.collectors.alienvault_otx.collector`)
* **Configuration Parameters:**
*  * `api_key`: `{{ your API key }}`
*  * `name`: `OTX`
*  * `provider`: `AlienVault`

### Parser

* **Bot:** AlienVault OTX (Module `intelmq.bots.parsers.alienvault.parser_otx`)
* **Configuration Parameters:**


## Reputation List

* **Public:** yes
* **Revision:** 2018-01-20
* **Description:** List of malicious IPs.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://reputation.alienvault.com/reputation.data`
*  * `name`: `Reputation List`
*  * `provider`: `AlienVault`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** AlienVault (Module `intelmq.bots.parsers.alienvault.parser`)
* **Configuration Parameters:**


# AnubisNetworks

## Cyberfeed Stream

* **Public:** unknown
* **Revision:** 2020-06-15
* **Documentation:** https://www.anubisnetworks.com/ https://www.bitsight.com/
* **Description:** Fetches and parsers the Cyberfeed data stream.

### Collector

* **Bot:** URL Stream Fetcher (Module `intelmq.bots.collectors.http.collector_http_stream`)
* **Configuration Parameters:**
*  * `http_url`: `https://prod.cyberfeed.net/stream?key={{ your API key }}`
*  * `name`: `Cyberfeed Stream`
*  * `provider`: `AnubisNetworks`
*  * `strip_lines`: `true`

### Parser

* **Bot:** AnubisNetworks Cyberfeed Stream (Module `intelmq.bots.parsers.anubisnetworks.parser`)
* **Configuration Parameters:**
*  * `use_malware_familiy_as_classification_identifier`: `True`


# Autoshun

## Shunlist

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://www.autoshun.org/
* **Description:** You need to register in order to use the list.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.autoshun.org/download/?api_key=__APIKEY__&format=html`
*  * `name`: `Shunlist`
*  * `provider`: `Autoshun`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Autoshun (Module `intelmq.bots.parsers.autoshun.parser`)
* **Configuration Parameters:**


# Bambenek

## C2 Domains

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://osint.bambenekconsulting.com/feeds/
* **Description:** Master Feed of known, active and non-sinkholed C&Cs domain names. Requires access credentials.
* **Additional Information:** License: https://osint.bambenekconsulting.com/license.txt

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_password`: `__PASSWORD__`
*  * `http_url`: `https://faf.bambenekconsulting.com/feeds/c2-dommasterlist.txt`
*  * `http_username`: `__USERNAME__`
*  * `name`: `C2 Domains`
*  * `provider`: `Bambenek`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Bambenek (Module `intelmq.bots.parsers.bambenek.parser`)
* **Configuration Parameters:**


## C2 IPs

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://osint.bambenekconsulting.com/feeds/
* **Description:** Master Feed of known, active and non-sinkholed C&Cs IP addresses. Requires access credentials.
* **Additional Information:** License: https://osint.bambenekconsulting.com/license.txt

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_password`: `__PASSWORD__`
*  * `http_url`: `https://faf.bambenekconsulting.com/feeds/c2-ipmasterlist.txt`
*  * `http_username`: `__USERNAME__`
*  * `name`: `C2 IPs`
*  * `provider`: `Bambenek`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Bambenek (Module `intelmq.bots.parsers.bambenek.parser`)
* **Configuration Parameters:**


## DGA Domains

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://osint.bambenekconsulting.com/feeds/
* **Description:** Domain feed of known DGA domains from -2 to +3 days
* **Additional Information:** License: https://osint.bambenekconsulting.com/license.txt

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://faf.bambenekconsulting.com/feeds/dga-feed.txt`
*  * `name`: `DGA Domains`
*  * `provider`: `Bambenek`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Bambenek (Module `intelmq.bots.parsers.bambenek.parser`)
* **Configuration Parameters:**


# Blocklist.de

## Apache

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://www.blocklist.de/en/export.html
* **Description:** Blocklist.DE Apache Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service Apache, Apache-DDOS, RFI-Attacks.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/apache.txt`
*  * `name`: `Apache`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Blocklist.de (Module `intelmq.bots.parsers.blocklistde.parser`)
* **Configuration Parameters:**


## Bots

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://www.blocklist.de/en/export.html
* **Description:** Blocklist.DE Bots Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks attacks on the RFI-Attacks, REG-Bots, IRC-Bots or BadBots (BadBots = he has posted a Spam-Comment on a open Forum or Wiki).

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/bots.txt`
*  * `name`: `Bots`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Blocklist.de (Module `intelmq.bots.parsers.blocklistde.parser`)
* **Configuration Parameters:**


## Brute-force Logins

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://www.blocklist.de/en/export.html
* **Description:** Blocklist.DE Brute-force Login Collector is the bot responsible to get the report from source of information. All IPs which attacks Joomlas, Wordpress and other Web-Logins with Brute-Force Logins.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/bruteforcelogin.txt`
*  * `name`: `Brute-force Logins`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Blocklist.de (Module `intelmq.bots.parsers.blocklistde.parser`)
* **Configuration Parameters:**


## FTP

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://www.blocklist.de/en/export.html
* **Description:** Blocklist.DE FTP Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours for attacks on the Service FTP.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/ftp.txt`
*  * `name`: `FTP`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Blocklist.de (Module `intelmq.bots.parsers.blocklistde.parser`)
* **Configuration Parameters:**


## IMAP

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://www.blocklist.de/en/export.html
* **Description:** Blocklist.DE IMAP Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours for attacks on the service like IMAP, SASL, POP3, etc.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/imap.txt`
*  * `name`: `IMAP`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Blocklist.de (Module `intelmq.bots.parsers.blocklistde.parser`)
* **Configuration Parameters:**


## IRC Bots

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://www.blocklist.de/en/export.html
* **Description:** No description provided by feed provider.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/ircbot.txt`
*  * `name`: `IRC Bots`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Blocklist.de (Module `intelmq.bots.parsers.blocklistde.parser`)
* **Configuration Parameters:**


## Mail

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://www.blocklist.de/en/export.html
* **Description:** Blocklist.DE Mail Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service Mail, Postfix.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/mail.txt`
*  * `name`: `Mail`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Blocklist.de (Module `intelmq.bots.parsers.blocklistde.parser`)
* **Configuration Parameters:**


## SIP

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://www.blocklist.de/en/export.html
* **Description:** Blocklist.DE SIP Collector is the bot responsible to get the report from source of information. All IP addresses that tried to login in a SIP-, VOIP- or Asterisk-Server and are included in the IPs-List from http://www.infiltrated.net/ (Twitter).

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/sip.txt`
*  * `name`: `SIP`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Blocklist.de (Module `intelmq.bots.parsers.blocklistde.parser`)
* **Configuration Parameters:**


## SSH

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://www.blocklist.de/en/export.html
* **Description:** Blocklist.DE SSH Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service SSH.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/ssh.txt`
*  * `name`: `SSH`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Blocklist.de (Module `intelmq.bots.parsers.blocklistde.parser`)
* **Configuration Parameters:**


## Strong IPs

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://www.blocklist.de/en/export.html
* **Description:** Blocklist.DE Strong IPs Collector is the bot responsible to get the report from source of information. All IPs which are older then 2 month and have more then 5.000 attacks.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/strongips.txt`
*  * `name`: `Strong IPs`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Blocklist.de (Module `intelmq.bots.parsers.blocklistde.parser`)
* **Configuration Parameters:**


# Blueliv

## CrimeServer

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://www.blueliv.com/
* **Description:** Blueliv Crimeserver Collector is the bot responsible to get the report through the API.
* **Additional Information:** The service uses a different API for free users and paying subscribers. In 'CrimeServer' feed the difference lies in the data points present in the feed. The non-free API available from Blueliv contains, for this specific feed, following extra fields not present in the free API; "_id" - Internal unique ID "subType" - Subtype of the Crime Server "countryName" - Country name where the Crime Server is located, in English "city" - City where the Crime Server is located "domain" - Domain of the Crime Server "host" - Host of the Crime Server "createdAt" - Date when the Crime Server was added to Blueliv CrimeServer database "asnCidr" - Range of IPs that belong to an ISP (registered via Autonomous System Number (ASN)) "asnId" - Identifier of an ISP registered via ASN "asnDesc" Description of the ISP registered via ASN

### Collector

* **Bot:** Blueliv Crimeserver (Module `intelmq.bots.collectors.blueliv.collector_crimeserver`)
* **Configuration Parameters:**
*  * `api_key`: `__APIKEY__`
*  * `name`: `CrimeServer`
*  * `provider`: `Blueliv`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Blueliv Crimeserver (Module `intelmq.bots.parsers.blueliv.parser_crimeserver`)
* **Configuration Parameters:**


# CERT.PL

## N6 Stomp Stream

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://n6.cert.pl/en/
* **Description:** N6 Collector - CERT.pl's N6 Collector - N6 feed via STOMP interface. Note that rate_limit does not apply for this bot as it is waiting for messages on a stream.
* **Additional Information:** Contact cert.pl to get access to the feed.

### Collector

* **Bot:** STOMP (Module `intelmq.bots.collectors.stomp.collector`)
* **Configuration Parameters:**
*  * `exchange`: `{insert your exchange point as given by CERT.pl}`
*  * `name`: `N6 Stomp Stream`
*  * `port`: `61614`
*  * `provider`: `CERT.PL`
*  * `server`: `n6stream.cert.pl`
*  * `ssl_ca_certificate`: `{insert path to CA file for CERT.pl's n6}`
*  * `ssl_client_certificate`: `{insert path to client cert file for CERTpl's n6}`
*  * `ssl_client_certificate_key`: `{insert path to client cert key file for CERT.pl's n6}`

### Parser

* **Bot:** N6Stomp (Module `intelmq.bots.parsers.n6.parser_n6stomp`)
* **Configuration Parameters:**


# CINSscore

## Army List

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://cinsscore.com/#list
* **Description:** The CINS Army list is a subset of the CINS Active Threat Intelligence ruleset, and consists of IP addresses that meet one of two basic criteria: 1) The IP's recent Rogue Packet score factor is very poor, or 2) The IP has tripped a designated number of 'trusted' alerts across a given number of our Sentinels deployed around the world.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://cinsscore.com/list/ci-badguys.txt`
*  * `name`: `Army List`
*  * `provider`: `CINSscore`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** CI Army (Module `intelmq.bots.parsers.ci_army.parser`)
* **Configuration Parameters:**


# CZ.NIC

## HaaS

* **Public:** yes
* **Revision:** 2020-07-22
* **Documentation:** https://haas.nic.cz/
* **Description:** SSH attackers against HaaS (Honeypot as a Sevice) provided by CZ.NIC, z.s.p.o. The dump is published once a day.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `extract_files`: `True`
*  * `http_url`: `https://haas.nic.cz/stats/export/{time[%Y/%m/%Y-%m-%d]}.json.gz`
*  * `http_url_formatting`: `{'days': -1}`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** CZ.NIC HaaS (Module `intelmq.bots.parsers.cznic.parser_haas`)
* **Configuration Parameters:**


# Calidog

## CertStream

* **Public:** yes
* **Revision:** 2018-06-15
* **Documentation:** https://medium.com/cali-dog-security/introducing-certstream-3fc13bb98067
* **Description:** HTTP Websocket Stream from certstream.calidog.io providing data from Certificate Transparency Logs.
* **Additional Information:** Be aware that this feed provides a lot of data and may overload your system quickly.

### Collector

* **Bot:** Undefined Bot (Module `intelmq.bots.collectors.certstream.collector_certstream`)
* **Configuration Parameters:**
*  * `name`: `CertStream`
*  * `provider`: `Calidog`

### Parser

* **Bot:** Undefined Bot (Module `intelmq.bots.parses.certstream.parser_certstream`)
* **Configuration Parameters:**


# CleanMX

## Phishing

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** http://clean-mx.de/
* **Description:** In order to download the CleanMX feed you need to use a custom user agent and register that user agent.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_timeout_sec`: `120`
*  * `http_url`: `http://support.clean-mx.de/clean-mx/xmlphishing?response=alive&domain=`
*  * `http_user_agent`: `{{ your user agent }}`
*  * `name`: `Phishing`
*  * `provider`: `CleanMX`
*  * `rate_limit`: `129600`

### Parser

* **Bot:** CleanMX (Module `intelmq.bots.parsers.cleanmx.parser`)
* **Configuration Parameters:**


## Virus

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** http://clean-mx.de/
* **Description:** In order to download the CleanMX feed you need to use a custom user agent and register that user agent.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_timeout_sec`: `120`
*  * `http_url`: `http://support.clean-mx.de/clean-mx/xmlviruses?response=alive&domain=`
*  * `http_user_agent`: `{{ your user agent }}`
*  * `name`: `Virus`
*  * `provider`: `CleanMX`
*  * `rate_limit`: `129600`

### Parser

* **Bot:** CleanMX (Module `intelmq.bots.parsers.cleanmx.parser`)
* **Configuration Parameters:**


# CyberCrime Tracker

## Latest

* **Public:** yes
* **Revision:** 2019-03-19
* **Documentation:** https://cybercrime-tracker.net/index.php
* **Description:** C2 servers

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://cybercrime-tracker.net/index.php`
*  * `name`: `Latest`
*  * `provider`: `CyberCrime Tracker`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** HTML Table (Module `intelmq.bots.parsers.html_table.parser`)
* **Configuration Parameters:**
*  * `columns`: `["time.source", "source.url", "source.ip", "malware.name", "__IGNORE__"]`
*  * `default_url_protocol`: `http://`
*  * `skip_table_head`: `True`
*  * `type`: `c2server`


# DShield

## AS Details

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://www.dshield.org/reports.html
* **Description:** No description provided by feed provider.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://dshield.org/asdetailsascii.html?as={{ AS Number }}`
*  * `name`: `AS Details`
*  * `provider`: `DShield`
*  * `rate_limit`: `129600`

### Parser

* **Bot:** DShield AS (Module `intelmq.bots.parsers.dshield.parser_asn`)
* **Configuration Parameters:**


## Block

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://www.dshield.org/reports.html
* **Description:** This list summarizes the top 20 attacking class C (/24) subnets over the last three days. The number of 'attacks' indicates the number of targets reporting scans from this subnet.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.dshield.org/block.txt`
*  * `name`: `Block`
*  * `provider`: `DShield`
*  * `rate_limit`: `129600`

### Parser

* **Bot:** DShield Block (Module `intelmq.bots.parsers.dshield.parser_block`)
* **Configuration Parameters:**


## Suspicious Domains

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://www.dshield.org/reports.html
* **Description:** There are many suspicious domains on the internet. In an effort to identify them, as well as false positives, we have assembled weighted lists based on tracking and malware lists from different sources. ISC is collecting and categorizing various lists associated with a certain level of sensitivity.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.dshield.org/feeds/suspiciousdomains_High.txt`
*  * `name`: `Suspicious Domains`
*  * `provider`: `DShield`
*  * `rate_limit`: `129600`

### Parser

* **Bot:** DShield Suspicious Domains (Module `intelmq.bots.parsers.dshield.parser_domain`)
* **Configuration Parameters:**


# Danger Rulez

## Bruteforce Blocker

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://danger.rulez.sk/index.php/bruteforceblocker/
* **Description:** Its main purpose is to block SSH bruteforce attacks via firewall.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://danger.rulez.sk/projects/bruteforceblocker/blist.php`
*  * `name`: `Bruteforce Blocker`
*  * `provider`: `Danger Rulez`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Danger Rulez (Module `intelmq.bots.parsers.danger_rulez.parser`)
* **Configuration Parameters:**


# Dataplane

## SIP Query

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://dataplane.org/
* **Description:** Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP OPTIONS query to a remote host. This report lists hosts that are suspicious of more than just port scanning. The hosts may be SIP server cataloging or conducting various forms of telephony abuse. Report is updated hourly.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://dataplane.org/sipquery.txt`
*  * `name`: `SIP Query`
*  * `provider`: `Dataplane`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Dataplane (Module `intelmq.bots.parsers.dataplane.parser`)
* **Configuration Parameters:**


## SIP Registration

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://dataplane.org/
* **Description:** Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP REGISTER operation to a remote host. This report lists hosts that are suspicious of more than just port scanning. The hosts may be SIP client cataloging or conducting various forms of telephony abuse. Report is updated hourly.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://dataplane.org/sipregistration.txt`
*  * `name`: `SIP Registration`
*  * `provider`: `Dataplane`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Dataplane (Module `intelmq.bots.parsers.dataplane.parser`)
* **Configuration Parameters:**


## SSH Client Connection

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://dataplane.org/
* **Description:** Entries below consist of fields with identifying characteristics of a source IP address that has been seen initiating an SSH connection to a remote host. This report lists hosts that are suspicious of more than just port scanning. The hosts may be SSH server cataloging or conducting authentication attack attempts. Report is updated hourly.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://dataplane.org/sshclient.txt`
*  * `name`: `SSH Client Connection`
*  * `provider`: `Dataplane`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Dataplane (Module `intelmq.bots.parsers.dataplane.parser`)
* **Configuration Parameters:**


## SSH Password Authentication

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://dataplane.org/
* **Description:** Entries below consist of fields with identifying characteristics of a source IP address that has been seen attempting to remotely login to a host using SSH password authentication. The report lists hosts that are highly suspicious and are likely conducting malicious SSH password authentication attacks. Report is updated hourly.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://dataplane.org/sshpwauth.txt`
*  * `name`: `SSH Password Authentication`
*  * `provider`: `Dataplane`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Dataplane (Module `intelmq.bots.parsers.dataplane.parser`)
* **Configuration Parameters:**


# DynDNS

## Infected Domains

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://security-research.dyndns.org/pub/malware-feeds/
* **Description:** DynDNS ponmocup. List of ponmocup malware redirection domains and infected web-servers. See also http://security-research.dyndns.org/pub/botnet-links.html

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://security-research.dyndns.org/pub/malware-feeds/ponmocup-infected-domains-CIF-latest.txt`
*  * `name`: `Infected Domains`
*  * `provider`: `DynDNS`
*  * `rate_limit`: `10800`

### Parser

* **Bot:** DynDNS ponmocup Domains (Module `intelmq.bots.parsers.dyn.parser`)
* **Configuration Parameters:**


# ESET

## ETI Domains

* **Public:** unknown
* **Revision:** 2020-06-30
* **Documentation:** https://www.eset.com/int/business/services/threat-intelligence/
* **Description:** Domain data from ESET's TAXII API.

### Collector

* **Bot:** ESET ETI TAXII (Module `intelmq.bots.collectors.eset.collector`)
* **Configuration Parameters:**
*  * `collection`: `ei.domains v2 (json)`
*  * `endpoint`: `eti.eset.com`
*  * `password`: `<password>`
*  * `time_delta`: `3600`
*  * `username`: `<username>`

### Parser

* **Bot:** ESET (Module `intelmq.bots.parsers.eset.parser`)
* **Configuration Parameters:**


## ETI URLs

* **Public:** unknown
* **Revision:** 2020-06-30
* **Documentation:** https://www.eset.com/int/business/services/threat-intelligence/
* **Description:** URL data from ESET's TAXII API.

### Collector

* **Bot:** ESET ETI TAXII (Module `intelmq.bots.collectors.eset.collector`)
* **Configuration Parameters:**
*  * `collection`: `ei.urls (json)`
*  * `endpoint`: `eti.eset.com`
*  * `password`: `<password>`
*  * `time_delta`: `3600`
*  * `username`: `<username>`

### Parser

* **Bot:** ESET (Module `intelmq.bots.parsers.eset.parser`)
* **Configuration Parameters:**


# Fraunhofer

## DGA Archive

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://dgarchive.caad.fkie.fraunhofer.de/welcome/
* **Description:** Fraunhofer DGA collector fetches data from Fraunhofer's domain generation archive.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_password`: `{{ your password}}`
*  * `http_url`: `https://dgarchive.caad.fkie.fraunhofer.de/today`
*  * `http_username`: `{{ your username}}`
*  * `name`: `DGA Archive`
*  * `provider`: `Fraunhofer`
*  * `rate_limit`: `10800`

### Parser

* **Bot:** Fraunhofer DGA (Module `intelmq.bots.parsers.fraunhofer.parser_dga`)
* **Configuration Parameters:**


# Have I Been Pwned

## Enterprise Callback

* **Public:** unknown
* **Revision:** 2019-09-11
* **Documentation:** https://haveibeenpwned.com/EnterpriseSubscriber/
* **Description:** With the Enterprise Subscription of 'Have I Been Pwned' you are able to provide a callback URL and any new leak data is submitted to it. It is recommended to put a webserver with Authorization check, TLS etc. in front of the API collector.
* **Additional Information:** "A minimal nginx configuration could look like:
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
"

### Collector

* **Bot:** API (Module `intelmq.bots.collectors.api.collector_api`)
* **Configuration Parameters:**
*  * `name`: `Enterprise Callback`
*  * `port`: `5001`
*  * `provider`: `Have I Been Pwned`

### Parser

* **Bot:** Have I been Pwned Enterprise Callback (Module `intelmq.bots.parsers.hibp.parser_callback`)
* **Configuration Parameters:**


# Malc0de

## Bind Format

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://malc0de.com/dashboard/
* **Description:** This feed includes FQDN's of malicious hosts, the file format is in Bind file format.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://malc0de.com/bl/ZONES`
*  * `name`: `Bind Format`
*  * `provider`: `Malc0de`
*  * `rate_limit`: `10800`

### Parser

* **Bot:** Malc0de (Module `intelmq.bots.parsers.malc0de.parser`)
* **Configuration Parameters:**


## IP Blacklist

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://malc0de.com/dashboard/
* **Description:** This feed includes IP Addresses of malicious hosts.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://malc0de.com/bl/IP_Blacklist.txt`
*  * `name`: `IP Blacklist`
*  * `provider`: `Malc0de`
*  * `rate_limit`: `10800`

### Parser

* **Bot:** Malc0de (Module `intelmq.bots.parsers.malc0de.parser`)
* **Configuration Parameters:**


## Windows Format

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://malc0de.com/dashboard/
* **Description:** This feed includes FQDN's of malicious hosts, the file format is in Windows Hosts file format.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://malc0de.com/bl/BOOT`
*  * `name`: `Windows Format`
*  * `provider`: `Malc0de`
*  * `rate_limit`: `10800`

### Parser

* **Bot:** Malc0de (Module `intelmq.bots.parsers.malc0de.parser`)
* **Configuration Parameters:**


# Malware Domain List

## Blacklist

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://www.malwaredomainlist.com/
* **Description:** No description provided by feed provider.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://www.malwaredomainlist.com/updatescsv.php`
*  * `name`: `Blacklist`
*  * `provider`: `Malware Domain List`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Malware Domain List (Module `intelmq.bots.parsers.malwaredomainlist.parser`)
* **Configuration Parameters:**


# Malware Domains

## Malicious

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://www.malwaredomains.com/
* **Description:** Malware Prevention through Domain Blocking (Black Hole DNS Sinkhole)

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://mirror1.malwaredomains.com/files/domains.txt`
*  * `name`: `Malicious`
*  * `provider`: `Malware Domains`
*  * `rate_limit`: `172800`

### Parser

* **Bot:** Malware Domains (Module `intelmq.bots.parsers.malwaredomains.parser`)
* **Configuration Parameters:**


# MalwarePatrol

## DansGuardian

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://www.malwarepatrol.net/non-commercial/
* **Description:** Malware block list with URLs

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://lists.malwarepatrol.net/cgi/getfile?receipt={{ your API key }}&product=8&list=dansguardian`
*  * `name`: `DansGuardian`
*  * `provider`: `MalwarePatrol`
*  * `rate_limit`: `180000`

### Parser

* **Bot:** MalwarePatrol Dans Guardian (Module `intelmq.bots.parsers.malwarepatrol.parser_dansguardian`)
* **Configuration Parameters:**


# MalwareURL

## Latest malicious activity

* **Public:** yes
* **Revision:** 2018-02-05
* **Documentation:** https://www.malwareurl.com/
* **Description:** Latest malicious domains/IPs.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.malwareurl.com/`
*  * `name`: `Latest malicious activity`
*  * `provider`: `MalwareURL`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Malwareurl (Module `intelmq.bots.parsers.malwareurl.parser`)
* **Configuration Parameters:**


# McAfee Advanced Threat Defense

## Sandbox Reports

* **Public:** unknown
* **Revision:** 2018-07-05
* **Documentation:** https://www.mcafee.com/enterprise/en-us/products/advanced-threat-defense.html
* **Description:** Processes reports from McAfee's sandboxing solution via the openDXL API.

### Collector

* **Bot:** McAfee openDXL (Module `intelmq.bots.collectors.opendxl.collector`)
* **Configuration Parameters:**
*  * `dxl_config_file`: `{{location of dxl configuration file}}`
*  * `dxl_topic`: `/mcafee/event/atd/file/report`

### Parser

* **Bot:** McAfee Advanced Threat Defense (Module `intelmq.bots.parsers.mcafee.parser_atd`)
* **Configuration Parameters:**
*  * `verdict_severity`: `4`


# Microsoft

## BingMURLs via Interflow

* **Public:** unknown
* **Revision:** 2018-05-29
* **Documentation:** https://docs.microsoft.com/en-us/security/gsp/informationsharingandexchange
* **Description:** Collects Malicious URLs detected by Bing from the Interflow API. The feed is available via Microsoft’s Government Security Program (GSP).
* **Additional Information:** Depending on the file sizes you may need to increase the parameter 'http_timeout_sec' of the collector.

### Collector

* **Bot:** Microsoft Interflow (Module `intelmq.bots.collectors.microsoft.collector_interflow`)
* **Configuration Parameters:**
*  * `api_key`: `{{your API key}}`
*  * `file_match`: `^bingmurls_`
*  * `http_timeout_sec`: `300`
*  * `name`: `BingMURLs via Interflow`
*  * `not_older_than`: `2 days`
*  * `provider`: `Microsoft`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Microsoft BingMURLs (Module `intelmq.bots.parsers.microsoft.parser_bingmurls`)
* **Configuration Parameters:**


## CTIP via Azure

* **Public:** unknown
* **Revision:** 2020-05-29
* **Documentation:** https://docs.microsoft.com/en-us/security/gsp/informationsharingandexchange
* **Description:** Collects CTIP (Sinkhole data) files from a shared Azure Storage. The feed is available via Microsoft’s Government Security Program (GSP).
* **Additional Information:** The cache is needed for memorizing which files have already been processed, the TTL should be higher than the oldest file available in the storage (currently the last three days are available). The connection string contains endpoint as well as authentication information.

### Collector

* **Bot:** Microsoft Azure (Module `intelmq.bots.collectors.microsoft.collector_azure`)
* **Configuration Parameters:**
*  * `connection_string`: `{{your connection string}}`
*  * `container_name`: `ctip-infected-summary`
*  * `name`: `CTIP via Azure`
*  * `provider`: `Microsoft`
*  * `rate_limit`: `3600`
*  * `redis_cache_db`: `5`
*  * `redis_cache_host`: `127.0.0.1`
*  * `redis_cache_port`: `6379`
*  * `redis_cache_ttl`: `864000`

### Parser

* **Bot:** Microsoft CTIP (Module `intelmq.bots.parsers.microsoft.parser_ctip`)
* **Configuration Parameters:**


## CTIP via Interflow

* **Public:** unknown
* **Revision:** 2018-03-06
* **Documentation:** https://docs.microsoft.com/en-us/security/gsp/informationsharingandexchange
* **Description:** Collects CTIP (Sinkhole data) files from the Interflow API.The feed is available via Microsoft’s Government Security Program (GSP).
* **Additional Information:** Depending on the file sizes you may need to increase the parameter 'http_timeout_sec' of the collector. As many IPs occur very often in the data, you may want to use a deduplicator specifically for the feed.

### Collector

* **Bot:** Microsoft Interflow (Module `intelmq.bots.collectors.microsoft.collector_interflow`)
* **Configuration Parameters:**
*  * `api_key`: `{{your API key}}`
*  * `file_match`: `^ctip_`
*  * `http_timeout_sec`: `300`
*  * `name`: `CTIP via Interflow`
*  * `not_older_than`: `2 days`
*  * `provider`: `Microsoft`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Microsoft CTIP (Module `intelmq.bots.parsers.microsoft.parser_ctip`)
* **Configuration Parameters:**


# Netlab 360

## DGA

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://data.netlab.360.com/dga
* **Description:** This feed lists DGA family, Domain, Start and end of valid time(UTC) of a number of DGA families.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://data.netlab.360.com/feeds/dga/dga.txt`
*  * `name`: `DGA`
*  * `provider`: `Netlab 360`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Netlab 360 (Module `intelmq.bots.parsers.netlab_360.parser`)
* **Configuration Parameters:**


## Hajime Scanner

* **Public:** yes
* **Revision:** 2019-08-01
* **Documentation:** https://data.netlab.360.com/hajime/
* **Description:** This feed lists IP address for know Hajime bots network. These IPs data are obtained by joining the DHT network and interacting with the Hajime node

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://data.netlab.360.com/feeds/hajime-scanner/bot.list`
*  * `name`: `Hajime Scanner`
*  * `provider`: `Netlab 360`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Netlab 360 (Module `intelmq.bots.parsers.netlab_360.parser`)
* **Configuration Parameters:**


## Magnitude EK

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://data.netlab.360.com/ek
* **Description:** This feed lists FQDN and possibly the URL used by Magnitude Exploit Kit. Information also includes the IP address used for the domain and last time seen.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://data.netlab.360.com/feeds/ek/magnitude.txt`
*  * `name`: `Magnitude EK`
*  * `provider`: `Netlab 360`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Netlab 360 (Module `intelmq.bots.parsers.netlab_360.parser`)
* **Configuration Parameters:**


## Mirai Scanner

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://data.netlab.360.com/mirai-scanner/
* **Description:** This feed provides IP addresses which actively scan for vulnerable IoT devices and install Mirai Botnet.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://data.netlab.360.com/feeds/mirai-scanner/scanner.list`
*  * `name`: `Mirai Scanner`
*  * `provider`: `Netlab 360`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Netlab 360 (Module `intelmq.bots.parsers.netlab_360.parser`)
* **Configuration Parameters:**


# OpenPhish

## Premium Feed

* **Public:** unknown
* **Revision:** 2018-02-06
* **Documentation:** https://www.openphish.com/phishing_feeds.html
* **Description:** OpenPhish is a fully automated self-contained platform for phishing intelligence. It identifies phishing sites and performs intelligence analysis in real time without human intervention and without using any external resources, such as blacklists.
* **Additional Information:** Discounts available for Government and National CERTs a well as for Nonprofit and Not-for-Profit organizations.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_password`: `{{ your password}}`
*  * `http_url`: `https://openphish.com/prvt-intell/`
*  * `http_username`: `{{ your username}}`
*  * `name`: `Premium Feed`
*  * `provider`: `OpenPhish`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** OpenPhish Commercial (Module `intelmq.bots.parsers.openphish.parser_commercial`)
* **Configuration Parameters:**


## Public feed

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://www.openphish.com/
* **Description:** OpenPhish is a fully automated self-contained platform for phishing intelligence. It identifies phishing sites and performs intelligence analysis in real time without human intervention and without using any external resources, such as blacklists.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.openphish.com/feed.txt`
*  * `name`: `Public feed`
*  * `provider`: `OpenPhish`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** OpenPhish (Module `intelmq.bots.parsers.openphish.parser`)
* **Configuration Parameters:**


# PhishTank

## Online

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://www.phishtank.com/developer_info.php
* **Description:** PhishTank is a collaborative clearing house for data and information about phishing on the Internet.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://data.phishtank.com/data/{{ your API key }}/online-valid.csv`
*  * `name`: `Online`
*  * `provider`: `PhishTank`
*  * `rate_limit`: `28800`

### Parser

* **Bot:** PhishTank (Module `intelmq.bots.parsers.phishtank.parser`)
* **Configuration Parameters:**


# PrecisionSec

## Agent Tesla

* **Public:** yes
* **Revision:** 2019-04-02
* **Documentation:** https://precisionsec.com/threat-intelligence-feeds/agent-tesla/
* **Description:** Agent Tesla IoCs, URLs where the malware is hosted.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://precisionsec.com/threat-intelligence-feeds/agent-tesla/`
*  * `name`: `Agent Tesla`
*  * `provider`: `PrecisionSec`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** HTML Table (Module `intelmq.bots.parsers.html_table.parser`)
* **Configuration Parameters:**
*  * `columns`: `["source.ip|source.url", "time.source"]`
*  * `default_url_protocol`: `http://`
*  * `skip_table_head`: `True`
*  * `type`: `malware`


# ShadowServer

## Via IMAP

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://www.shadowserver.org/what-we-do/network-reporting/
* **Description:** Shadowserver sends out a variety of reports (see https://www.shadowserver.org/wiki/pmwiki.php/Services/Reports).
* **Additional Information:** The configuration retrieves the data from a e-mails via IMAP from the attachments.

### Collector

* **Bot:** Mail Attachment Fetcher (Module `intelmq.bots.collectors.mail.collector_mail_attach`)
* **Configuration Parameters:**
*  * `attach_regex`: `csv.zip`
*  * `extract_files`: `True`
*  * `folder`: `INBOX`
*  * `mail_host`: `__HOST__`
*  * `mail_password`: `__PASSWORD__`
*  * `mail_ssl`: `True`
*  * `mail_user`: `__USERNAME__`
*  * `name`: `Via IMAP`
*  * `provider`: `ShadowServer`
*  * `rate_limit`: `86400`
*  * `subject_regex`: `__REGEX__`

### Parser

* **Bot:** ShadowServer (Module `intelmq.bots.parsers.shadowserver.parser`)
* **Configuration Parameters:**


## Via Request Tracker

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://www.shadowserver.org/what-we-do/network-reporting/
* **Description:** Shadowserver sends out a variety of reports (see https://www.shadowserver.org/wiki/pmwiki.php/Services/Reports).
* **Additional Information:** The configuration retrieves the data from a RT/RTIR ticketing instance via the attachment or an download.

### Collector

* **Bot:** Request Tracker (Module `intelmq.bots.collectors.rt.collector_rt`)
* **Configuration Parameters:**
*  * `attachment_regex`: `\\.csv\\.zip$`
*  * `extract_attachment`: `True`
*  * `extract_download`: `False`
*  * `http_password`: `{{ your HTTP Authentication password or null }}`
*  * `http_username`: `{{ your HTTP Authentication username or null }}`
*  * `password`: `__PASSWORD__`
*  * `provider`: `ShadowServer`
*  * `rate_limit`: `3600`
*  * `search_not_older_than`: `{{ relative time or null }}`
*  * `search_owner`: `nobody`
*  * `search_queue`: `Incident Reports`
*  * `search_requestor`: `autoreports@shadowserver.org`
*  * `search_status`: `new`
*  * `search_subject_like`: `\[__COUNTRY__\] Shadowserver __COUNTRY__`
*  * `set_status`: `open`
*  * `take_ticket`: `True`
*  * `uri`: `http://localhost/rt/REST/1.0`
*  * `url_regex`: `https://dl.shadowserver.org/[a-zA-Z0-9?_-]*`
*  * `user`: `__USERNAME__`

### Parser

* **Bot:** ShadowServer (Module `intelmq.bots.parsers.shadowserver.parser`)
* **Configuration Parameters:**


# Spamhaus

## ASN Drop

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://www.spamhaus.org/drop/
* **Description:** ASN-DROP contains a list of Autonomous System Numbers controlled by spammers or cyber criminals, as well as "hijacked" ASNs. ASN-DROP can be used to filter BGP routes which are being used for malicious purposes.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.spamhaus.org/drop/asndrop.txt`
*  * `name`: `ASN Drop`
*  * `provider`: `Spamhaus`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Spamhaus Drop (Module `intelmq.bots.parsers.spamhaus.parser_drop`)
* **Configuration Parameters:**


## CERT

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://www.spamhaus.org/news/article/705/spamhaus-launches-cert-insight-portal
* **Description:** Spamhaus CERT Insight Portal. Access limited to CERTs and CSIRTs with national or regional responsibility. .

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `{{ your CERT portal URL }}`
*  * `name`: `CERT`
*  * `provider`: `Spamhaus`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Spamhaus CERT (Module `intelmq.bots.parsers.spamhaus.parser_cert`)
* **Configuration Parameters:**


## Drop

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://www.spamhaus.org/drop/
* **Description:** The DROP list will not include any IP address space under the control of any legitimate network - even if being used by "the spammers from hell". DROP will only include netblocks allocated directly by an established Regional Internet Registry (RIR) or National Internet Registry (NIR) such as ARIN, RIPE, AFRINIC, APNIC, LACNIC or KRNIC or direct RIR allocations.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.spamhaus.org/drop/drop.txt`
*  * `name`: `Drop`
*  * `provider`: `Spamhaus`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Spamhaus Drop (Module `intelmq.bots.parsers.spamhaus.parser_drop`)
* **Configuration Parameters:**


## Dropv6

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://www.spamhaus.org/drop/
* **Description:** The DROPv6 list includes IPv6 ranges allocated to spammers or cyber criminals. DROPv6 will only include IPv6 netblocks allocated directly by an established Regional Internet Registry (RIR) or National Internet Registry (NIR) such as ARIN, RIPE, AFRINIC, APNIC, LACNIC or KRNIC or direct RIR allocations.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.spamhaus.org/drop/dropv6.txt`
*  * `name`: `Dropv6`
*  * `provider`: `Spamhaus`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Spamhaus Drop (Module `intelmq.bots.parsers.spamhaus.parser_drop`)
* **Configuration Parameters:**


## EDrop

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://www.spamhaus.org/drop/
* **Description:** EDROP is an extension of the DROP list that includes sub-allocated netblocks controlled by spammers or cyber criminals. EDROP is meant to be used in addition to the direct allocations on the DROP list.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.spamhaus.org/drop/edrop.txt`
*  * `name`: `EDrop`
*  * `provider`: `Spamhaus`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Spamhaus Drop (Module `intelmq.bots.parsers.spamhaus.parser_drop`)
* **Configuration Parameters:**


# Strangereal Intel

## DailyIOC

* **Public:** yes
* **Revision:** 2019-12-05
* **Documentation:** https://github.com/StrangerealIntel/DailyIOC
* **Description:** Daily IOC from tweets and articles
* **Additional Information:** collector's `extra_fields` parameter may be any of fields from the github [content API response](https://developer.github.com/v3/repos/contents/)

### Collector

* **Bot:** Github API (Module `intelmq.bots.collectors.github_api.collector_github_contents_api`)
* **Configuration Parameters:**
*  * `basic_auth_password`: `PASSWORD`
*  * `basic_auth_username`: `USERNAME`
*  * `regex`: `.*.json`
*  * `repository`: `StrangerealIntel/DailyIOC`

### Parser

* **Bot:** Undefined Bot (Module `intelmq.bots.parsers.github_feed`)
* **Configuration Parameters:**


# Sucuri

## Hidden IFrames

* **Public:** yes
* **Revision:** 2018-01-28
* **Documentation:** http://labs.sucuri.net/?malware
* **Description:** Latest hidden iframes identified on compromised web sites.
* **Additional Information:** Please note that the parser only extracts the hidden iframes  and the conditional redirects, not the encoded javascript.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://labs.sucuri.net/?malware`
*  * `name`: `Hidden IFrames`
*  * `provider`: `Sucuri`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Sucuri Malware (Module `intelmq.bots.parsers.sucuri.parser`)
* **Configuration Parameters:**


# Surbl

## Malicious Domains

* **Public:** unknown
* **Revision:** 2018-09-04
* **Description:** Detected malicious domains. Note that you have to opened up Sponsored Datafeed Service (SDS) access to the SURBL data via rsync for your IP address.

### Collector

* **Bot:** Rsync (Module `intelmq.bots.collectors.rsync.collector_rsync`)
* **Configuration Parameters:**
*  * `file`: `wild.surbl.org.rbldnsd`
*  * `rsync_path`: `blacksync.prolocation.net::surbl-wild/`

### Parser

* **Bot:** Surbl (Module `intelmq.bots.parsers.surbl.parser`)
* **Configuration Parameters:**


# Taichung

## Netflow Recent

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://www.tc.edu.tw/net/netflow/lkout/recent/
* **Description:** Abnormal flows detected: Attacking (DoS, Brute-Force, Scanners) and malicious hosts (C&C servers, hosting malware)

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.tc.edu.tw/net/netflow/lkout/recent/`
*  * `name`: `Netflow Recent`
*  * `provider`: `Taichung`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** Taichung (Module `intelmq.bots.parsers.taichung.parser`)
* **Configuration Parameters:**


# Team Cymru

## CAP

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://www.team-cymru.com/CSIRT-AP.html https://www.cymru.com/$certname/report_info.txt
* **Description:** Team Cymru provides daily lists of compromised or abused devices for the ASNs and/or netblocks with a CSIRT's jurisdiction. This includes such information as bot infected hosts, command and control systems, open resolvers, malware urls, phishing urls, and brute force attacks
* **Additional Information:** "Two feeds types are offered:
 * The new https://www.cymru.com/$certname/$certname_{time[%Y%m%d]}.txt
 * and the old https://www.cymru.com/$certname/infected_{time[%Y%m%d]}.txt
 Both formats are supported by the parser and the new one is recommended.
 As of 2019-09-12 the old format will be retired soon."

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_password`: `{{your password}}`
*  * `http_url`: `https://www.cymru.com/$certname/$certname_{time[%Y%m%d]}.txt`
*  * `http_url_formatting`: `True`
*  * `http_username`: `{{your login}}`
*  * `name`: `CAP`
*  * `provider`: `Team Cymru`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Cymru CAP Program (Module `intelmq.bots.parsers.cymru.parser_cap_program`)
* **Configuration Parameters:**


## Full Bogons IPv4

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://www.team-cymru.com/bogon-reference-http.html
* **Description:** Fullbogons are a larger set which also includes IP space that has been allocated to an RIR, but not assigned by that RIR to an actual ISP or other end-user. IANA maintains a convenient IPv4 summary page listing allocated and reserved netblocks, and each RIR maintains a list of all prefixes that they have assigned to end-users. Our bogon reference pages include additional links and resources to assist those who wish to properly filter bogon prefixes within their networks.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt`
*  * `name`: `Full Bogons IPv4`
*  * `provider`: `Team Cymru`
*  * `rate_limit`: `129600`

### Parser

* **Bot:** Cymru Full Bogons (Module `intelmq.bots.parsers.cymru.parser_full_bogons`)
* **Configuration Parameters:**


## Full Bogons IPv6

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://www.team-cymru.com/bogon-reference-http.html
* **Description:** Fullbogons are a larger set which also includes IP space that has been allocated to an RIR, but not assigned by that RIR to an actual ISP or other end-user. IANA maintains a convenient IPv4 summary page listing allocated and reserved netblocks, and each RIR maintains a list of all prefixes that they have assigned to end-users. Our bogon reference pages include additional links and resources to assist those who wish to properly filter bogon prefixes within their networks.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.team-cymru.org/Services/Bogons/fullbogons-ipv6.txt`
*  * `name`: `Full Bogons IPv6`
*  * `provider`: `Team Cymru`
*  * `rate_limit`: `129600`

### Parser

* **Bot:** Cymru Full Bogons (Module `intelmq.bots.parsers.cymru.parser_full_bogons`)
* **Configuration Parameters:**


# Threatminer

## Recent domains

* **Public:** yes
* **Revision:** 2018-02-06
* **Documentation:** https://www.threatminer.org/
* **Description:** Latest malicious domains.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.threatminer.org/`
*  * `name`: `Recent domains`
*  * `provider`: `Threatminer`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** Threatminer (Module `intelmq.bots.parsers.threatminer.parser`)
* **Configuration Parameters:**


# Turris

## Greylist

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://project.turris.cz/greylist-data/legend.txt
* **Description:** The data are processed and clasified every week and behaviour of IP addresses that accessed a larger number of Turris routers is evaluated. The result is a list of addresses that have tried to obtain information about services on the router or tried to gain access to them. We publish this so called "greylist" that also contains a list of tags for each address which indicate what behaviour of the address was observed.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://www.turris.cz/greylist-data/greylist-latest.csv`
*  * `name`: `Greylist`
*  * `provider`: `Turris`
*  * `rate_limit`: `43200`

### Parser

* **Bot:** Turris Greylist (Module `intelmq.bots.parsers.turris.parser`)
* **Configuration Parameters:**


# University of Toulouse

## Blacklist

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** https://dsi.ut-capitole.fr/blacklists/
* **Description:** Various blacklist feeds

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `extract_files`: `true`
*  * `http_url`: `https://dsi.ut-capitole.fr/blacklists/download/{collection name}.tar.gz`
*  * `name`: `Blacklist`
*  * `provider`: `University of Toulouse`
*  * `rate_limit`: `43200`

### Parser

* **Bot:** Generic CSV (Module `intelmq.bots.parsers.generic.parser_csv`)
* **Configuration Parameters:**
*  * `columns`: `{depends on a collection}`
*  * `delimiter`: `false`
*  * `type`: `{depends on a collection}`


# VXVault

## URLs

* **Public:** yes
* **Revision:** 2018-01-20
* **Documentation:** http://vxvault.net/ViriList.php
* **Description:** This feed provides IP addresses hosting Malware.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://vxvault.net/URL_List.php`
*  * `name`: `URLs`
*  * `provider`: `VXVault`
*  * `rate_limit`: `3600`

### Parser

* **Bot:** VXVault (Module `intelmq.bots.parsers.vxvault.parser`)
* **Configuration Parameters:**


# ViriBack

## Unsafe sites

* **Public:** yes
* **Revision:** 2018-06-27
* **Documentation:** https://viriback.com/
* **Description:** Latest detected unsafe sites.
* **Additional Information:** You need to install the lxml library in order to parse this feed.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `http://tracker.viriback.com/`
*  * `name`: `Unsafe sites`
*  * `provider`: `ViriBack`
*  * `rate_limit`: `86400`

### Parser

* **Bot:** HTML Table (Module `intelmq.bots.parsers.html_table.parser`)
* **Configuration Parameters:**
*  * `columns`: `["malware.name", "source.url", "source.ip", "time.source"]`
*  * `html_parser`: `lxml`
*  * `time_format`: `from_format_midnight|%d-%m-%Y`
*  * `type`: `malware`


# WebInspektor

## Unsafe sites

* **Public:** yes
* **Revision:** 2018-03-09
* **Description:** Latest detected unsafe sites.

### Collector

* **Bot:** URL Fetcher (Module `intelmq.bots.collectors.http.collector_http`)
* **Configuration Parameters:**
*  * `http_url`: `https://app.webinspector.com/public/recent_detections/`
*  * `name`: `Unsafe sites`
*  * `provider`: `WebInspektor`
*  * `rate_limit`: `60`

### Parser

* **Bot:** Web Inspektor (Module `intelmq.bots.parsers.webinspektor.parser`)
* **Configuration Parameters:**


# ZoneH

## Defacements

* **Public:** unknown
* **Revision:** 2018-01-20
* **Documentation:** https://zone-h.org/
* **Description:** all the information contained in Zone-H's cybercrime archive were either collected online from public sources or directly notified anonymously to us.

### Collector

* **Bot:** Mail Attachment Fetcher (Module `intelmq.bots.collectors.mail.collector_mail_attach`)
* **Configuration Parameters:**
*  * `attach_regex`: `csv`
*  * `extract_files`: `False`
*  * `folder`: `INBOX`
*  * `mail_host`: `__HOST__`
*  * `mail_password`: `__PASSWORD__`
*  * `mail_ssl`: `True`
*  * `mail_user`: `__USERNAME__`
*  * `name`: `Defacements`
*  * `provider`: `ZoneH`
*  * `rate_limit`: `3600`
*  * `sent_from`: `datazh@zone-h.org`
*  * `subject_regex`: `Report`

### Parser

* **Bot:** ZoneH (Module `intelmq.bots.parsers.zoneh.parser`)
* **Configuration Parameters:**


