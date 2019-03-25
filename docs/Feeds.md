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
- [Bitcash](#bitcash)
- [Blocklist.de](#blocklistde)
- [Blueliv](#blueliv)
- [CERT.PL](#certpl)
- [CINSscore](#cinsscore)
- [Calidog](#calidog)
- [CleanMX](#cleanmx)
- [DShield](#dshield)
- [Danger Rulez](#danger-rulez)
- [Dataplane](#dataplane)
- [DynDNS](#dyndns)
- [Fraunhofer](#fraunhofer)
- [HPHosts](#hphosts)
- [Malc0de](#malc0de)
- [Malware Domain List](#malware-domain-list)
- [Malware Domains](#malware-domains)
- [MalwarePatrol](#malwarepatrol)
- [MalwareURL](#malwareurl)
- [Microsoft](#microsoft)
- [Netlab 360](#netlab-360)
- [Nothink](#nothink)
- [OpenPhish](#openphish)
- [OpenPhish Commercial](#openphish-commercial)
- [PhishTank](#phishtank)
- [ShadowServer](#shadowserver)
- [Spamhaus](#spamhaus)
- [Sucuri](#sucuri)
- [Taichung](#taichung)
- [Team Cymru](#team-cymru)
- [Threatminer](#threatminer)
- [Turris](#turris)
- [URLVir](#urlvir)
- [University of Toulouse](#university-of-toulouse)
- [VXVault](#vxvault)
- [WebInspektor](#webinspektor)
- [ZoneH](#zoneh)


<!-- /TOC -->


# Abuse.ch

## Feodo Tracker IPs

* **Status:** on
* **Revision:** 25-03-2019
* **Description:** List of botnet Command&Control servers (C&Cs) tracked by Feodo Tracker, associated with Dridex and Emotet (aka Heodo).
* **Additional Information:** https://feodotracker.abuse.ch/

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://feodotracker.abuse.ch/downloads/ipblocklist.csv`
*  * `name`: `Feodo Tracker IPs`
*  * `provider`: `Abuse.ch`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.abusech.parser_ip
* **Configuration Parameters:**


## Ransomware Tracker

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Ransomware Tracker feed includes FQDN's, URL's, and known IP addresses that were used for said FQDN's and URL's for various ransomware families.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://ransomwaretracker.abuse.ch/feeds/csv/`
*  * `name`: `Ransomware Tracker`
*  * `provider`: `Abuse.ch`
*  * `rate_limit`: `129600`

### Parser

* **Module:** intelmq.bots.parsers.abusech.parser_ransomware
* **Configuration Parameters:**


## Zeus Tracker Domains

* **Status:** off
* **Revision:** 20-01-2018
* **Description:** The ZeuS domain blocklist (BadDomains) is the recommended blocklist if you want to block only ZeuS domain names. It has domain names that ZeuS Tracker believes to be hijacked (level 2). Hence the false positive rate should be much lower compared to the standard ZeuS domain blocklist.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://zeustracker.abuse.ch/blocklist.php?download=baddomains`
*  * `name`: `Zeus Tracker Domains`
*  * `provider`: `Abuse.ch`
*  * `rate_limit`: `129600`

### Parser

* **Module:** intelmq.bots.parsers.abusech.parser_domain
* **Configuration Parameters:**


## Zeus Tracker IPs

* **Status:** off
* **Revision:** 20-01-2018
* **Description:** This list only includes IPv4 addresses that are used by the ZeuS Trojan. It is the recommended list if you want to block only ZeuS IPs. It excludes IP addresses that ZeuS Tracker believes to be hijacked (level 2) or belong to a free web hosting provider (level 3). Hence the false positive rate should be much lower compared to the standard ZeuS IP blocklist.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://zeustracker.abuse.ch/blocklist.php?download=badips`
*  * `name`: `Zeus Tracker IPs`
*  * `provider`: `Abuse.ch`
*  * `rate_limit`: `129600`

### Parser

* **Module:** intelmq.bots.parsers.abusech.parser_ip
* **Configuration Parameters:**


# AlienVault

## OTX

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** AlienVault OTX Collector is the bot responsible to get the report through the API. Report could vary according to subscriptions.

### Collector

* **Module:** intelmq.bots.collectors.alienvault_otx.collector
* **Configuration Parameters:**
*  * `api_key`: `{{ your API key }}`
*  * `name`: `OTX`
*  * `provider`: `AlienVault`

### Parser

* **Module:** intelmq.bots.parsers.alienvault.parser_otx
* **Configuration Parameters:**


## Reputation List

* **Status:** off
* **Revision:** 20-01-2018
* **Description:** List of malicious IPs.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://reputation.alienvault.com/reputation.data`
*  * `name`: `Reputation List`
*  * `provider`: `AlienVault`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.alienvault.parser
* **Configuration Parameters:**


# AnubisNetworks

## Cyberfeed Stream

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** AnubisNetworks Collector is the bot responsible to get AnubisNetworks Cyberfeed Stream.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http_stream
* **Configuration Parameters:**
*  * `http_url`: `https://prod.cyberfeed.net/stream?key={{ your API key }}`
*  * `name`: `Cyberfeed Stream`
*  * `provider`: `AnubisNetworks`
*  * `strip_lines`: `true`

### Parser

* **Module:** intelmq.bots.parsers.anubisnetworks.parser
* **Configuration Parameters:**


# Autoshun

## Shunlist

* **Status:** off
* **Revision:** 20-01-2018
* **Description:** You need to register in order to use the list.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.autoshun.org/download/?api_key=__APIKEY__&format=html`
*  * `name`: `Shunlist`
*  * `provider`: `Autoshun`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.autoshun.parser
* **Configuration Parameters:**


# Bambenek

## C2 Domains

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Master Feed of known, active and non-sinkholed C&Cs domain names. License: https://osint.bambenekconsulting.com/license.txt

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt`
*  * `name`: `C2 Domains`
*  * `provider`: `Bambenek`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.bambenek.parser
* **Configuration Parameters:**


## C2 IPs

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Master Feed of known, active and non-sinkholed C&Cs IP addresses License: https://osint.bambenekconsulting.com/license.txt

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt`
*  * `name`: `C2 IPs`
*  * `provider`: `Bambenek`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.bambenek.parser
* **Configuration Parameters:**


## DGA Domains

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Domain feed of known DGA domains from -2 to +3 days License: https://osint.bambenekconsulting.com/license.txt

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://osint.bambenekconsulting.com/feeds/dga-feed.txt`
*  * `name`: `DGA Domains`
*  * `provider`: `Bambenek`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.bambenek.parser
* **Configuration Parameters:**


# Bitcash

## Banned IPs

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** IPs banned for serious abusing of our services (scanning, sniffing, harvesting, dos attacks).

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://bitcash.cz/misc/log/blacklist`
*  * `name`: `Banned IPs`
*  * `provider`: `Bitcash`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.bitcash.parser
* **Configuration Parameters:**


# Blocklist.de

## Apache

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Blocklist.DE Apache Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service Apache, Apache-DDOS, RFI-Attacks.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/apache.txt`
*  * `name`: `Apache`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.blocklistde.parser
* **Configuration Parameters:**


## Bots

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Blocklist.DE Bots Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks attacks on the RFI-Attacks, REG-Bots, IRC-Bots or BadBots (BadBots = he has posted a Spam-Comment on a open Forum or Wiki).

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/bots.txt`
*  * `name`: `Bots`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.blocklistde.parser
* **Configuration Parameters:**


## Brute-force Logins

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Blocklist.DE Brute-force Login Collector is the bot responsible to get the report from source of information. All IPs which attacks Joomlas, Wordpress and other Web-Logins with Brute-Force Logins.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/bruteforcelogin.txt`
*  * `name`: `Brute-force Logins`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.blocklistde.parser
* **Configuration Parameters:**


## FTP

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Blocklist.DE FTP Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours for attacks on the Service FTP.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/ftp.txt`
*  * `name`: `FTP`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.blocklistde.parser
* **Configuration Parameters:**


## IMAP

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Blocklist.DE IMAP Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours for attacks on the service like IMAP, SASL, POP3, etc.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/imap.txt`
*  * `name`: `IMAP`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.blocklistde.parser
* **Configuration Parameters:**


## IRC Bots

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** No description provided by feed provider.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/ircbot.txt`
*  * `name`: `IRC Bots`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.blocklistde.parser
* **Configuration Parameters:**


## Mail

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Blocklist.DE Mail Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service Mail, Postfix.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/mail.txt`
*  * `name`: `Mail`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.blocklistde.parser
* **Configuration Parameters:**


## SIP

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Blocklist.DE SIP Collector is the bot responsible to get the report from source of information. All IP addresses that tried to login in a SIP-, VOIP- or Asterisk-Server and are included in the IPs-List from http://www.infiltrated.net/ (Twitter).

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/sip.txt`
*  * `name`: `SIP`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.blocklistde.parser
* **Configuration Parameters:**


## SSH

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Blocklist.DE SSH Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service SSH.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/ssh.txt`
*  * `name`: `SSH`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.blocklistde.parser
* **Configuration Parameters:**


## Strong IPs

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Blocklist.DE Strong IPs Collector is the bot responsible to get the report from source of information. All IPs which are older then 2 month and have more then 5.000 attacks.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://lists.blocklist.de/lists/strongips.txt`
*  * `name`: `Strong IPs`
*  * `provider`: `Blocklist.de`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.blocklistde.parser
* **Configuration Parameters:**


# Blueliv

## CrimeServer

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Blueliv Crimeserver Collector is the bot responsible to get the report through the API.

### Collector

* **Module:** intelmq.bots.collectors.blueliv.collector_crimeserver
* **Configuration Parameters:**
*  * `api_key`: `__APIKEY__`
*  * `name`: `CrimeServer`
*  * `provider`: `Blueliv`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.blueliv.parser_crimeserver
* **Configuration Parameters:**


# CERT.PL

## N6 Stomp Stream

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** N6 Collector - CERT.pl's N6 Collector - N6 feed via STOMP interface. Note that rate_limit does not apply for this bot as it is waiting for messages on a stream.

### Collector

* **Module:** intelmq.bots.collectors.stomp.collector
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

* **Module:** intelmq.bots.parsers.n6.parser_n6stomp
* **Configuration Parameters:**


# CINSscore

## Army List

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** The CINS Army list is a subset of the CINS Active Threat Intelligence ruleset, and consists of IP addresses that meet one of two basic criteria: 1) The IP's recent Rogue Packet score factor is very poor, or 2) The IP has tripped a designated number of 'trusted' alerts across a given number of our Sentinels deployed around the world.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://cinsscore.com/list/ci-badguys.txt`
*  * `name`: `Army List`
*  * `provider`: `CINSscore`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.ci_army.parser
* **Configuration Parameters:**


# Calidog

## CertStream

* **Status:** on
* **Revision:** 15-06-2018
* **Description:** HTTP Websocket Stream from certstream.calidog.io providing data from Certificate Transparency Logs.

### Collector

* **Module:** intelmq.bots.collectors.certstream.collector_certstream
* **Configuration Parameters:**
*  * `name`: `CertStream`
*  * `provider`: `Calidog`

### Parser

* **Module:** intelmq.bots.parses.certstream.parser_certstream
* **Configuration Parameters:**


# CleanMX

## Phishing

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** In order to download the CleanMX feed you need to use a custom user agent and register that user agent.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_timeout_sec`: `120`
*  * `http_url`: `http://support.clean-mx.de/clean-mx/xmlphishing?response=alive&domain=`
*  * `http_user_agent`: `{{ your user agent }}`
*  * `name`: `Phishing`
*  * `provider`: `CleanMX`
*  * `rate_limit`: `129600`

### Parser

* **Module:** intelmq.bots.parsers.cleanmx.parser
* **Configuration Parameters:**


## Virus

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** In order to download the CleanMX feed you need to use a custom user agent and register that user agent.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_timeout_sec`: `120`
*  * `http_url`: `http://support.clean-mx.de/clean-mx/xmlviruses?response=alive&domain=`
*  * `http_user_agent`: `{{ your user agent }}`
*  * `name`: `Virus`
*  * `provider`: `CleanMX`
*  * `rate_limit`: `129600`

### Parser

* **Module:** intelmq.bots.parsers.cleanmx.parser
* **Configuration Parameters:**


# DShield

## AS Details

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** No description provided by feed provider.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://dshield.org/asdetailsascii.html?as={{ AS Number }}`
*  * `name`: `AS Details`
*  * `provider`: `DShield`
*  * `rate_limit`: `129600`

### Parser

* **Module:** intelmq.bots.parsers.dshield.parser_asn
* **Configuration Parameters:**


## Block

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** This list summarizes the top 20 attacking class C (/24) subnets over the last three days. The number of 'attacks' indicates the number of targets reporting scans from this subnet.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.dshield.org/block.txt`
*  * `name`: `Block`
*  * `provider`: `DShield`
*  * `rate_limit`: `129600`

### Parser

* **Module:** intelmq.bots.parsers.dshield.parser_block
* **Configuration Parameters:**


## Suspicious Domains

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** There are many suspicious domains on the internet. In an effort to identify them, as well as false positives, we have assembled weighted lists based on tracking and malware lists from different sources. ISC is collecting and categorizing various lists associated with a certain level of sensitivity.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.dshield.org/feeds/suspiciousdomains_High.txt`
*  * `name`: `Suspicious Domains`
*  * `provider`: `DShield`
*  * `rate_limit`: `129600`

### Parser

* **Module:** intelmq.bots.parsers.dshield.parser_domain
* **Configuration Parameters:**


# Danger Rulez

## Bruteforce Blocker

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Its main purpose is to block SSH bruteforce attacks via firewall.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://danger.rulez.sk/projects/bruteforceblocker/blist.php`
*  * `name`: `Bruteforce Blocker`
*  * `provider`: `Danger Rulez`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.danger_rulez.parser
* **Configuration Parameters:**


## SIP Invitation

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP INVITE operation to a remote host. The report lists hosts that are suspicious of more than just port scanning. These hosts may be SIP client cataloging or conducting various forms of telephony abuse. Report is updated hourly.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://dataplane.org/sipinvitation.txt`
*  * `name`: `SIP Invitation`
*  * `provider`: `Danger Rulez`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.dataplane.parser
* **Configuration Parameters:**


# Dataplane

## SIP Query

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP OPTIONS query to a remote host. This report lists hosts that are suspicious of more than just port scanning. The hosts may be SIP server cataloging or conducting various forms of telephony abuse. Report is updated hourly.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://dataplane.org/sipquery.txt`
*  * `name`: `SIP Query`
*  * `provider`: `Dataplane`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.dataplane.parser
* **Configuration Parameters:**


## SIP Registration

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP REGISTER operation to a remote host. This report lists hosts that are suspicious of more than just port scanning. The hosts may be SIP client cataloging or conducting various forms of telephony abuse. Report is updated hourly.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://dataplane.org/sipregistration.txt`
*  * `name`: `SIP Registration`
*  * `provider`: `Dataplane`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.dataplane.parser
* **Configuration Parameters:**


## SSH Client Connection

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Entries below consist of fields with identifying characteristics of a source IP address that has been seen initiating an SSH connection to a remote host. This report lists hosts that are suspicious of more than just port scanning. The hosts may be SSH server cataloging or conducting authentication attack attempts. Report is updated hourly.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://dataplane.org/sshclient.txt`
*  * `name`: `SSH Client Connection`
*  * `provider`: `Dataplane`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.dataplane.parser
* **Configuration Parameters:**


## SSH Password Authentication

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Entries below consist of fields with identifying characteristics of a source IP address that has been seen attempting to remotely login to a host using SSH password authentication. The report lists hosts that are highly suspicious and are likely conducting malicious SSH password authentication attacks. Report is updated hourly.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://dataplane.org/sshpwauth.txt`
*  * `name`: `SSH Password Authentication`
*  * `provider`: `Dataplane`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.dataplane.parser
* **Configuration Parameters:**


# DynDNS

## Infected Domains

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** DynDNS ponmocup. List of ponmocup malware redirection domains and infected web-servers. See also http://security-research.dyndns.org/pub/botnet-links.html

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://security-research.dyndns.org/pub/malware-feeds/ponmocup-infected-domains-CIF-latest.txt`
*  * `name`: `Infected Domains`
*  * `provider`: `DynDNS`
*  * `rate_limit`: `10800`

### Parser

* **Module:** intelmq.bots.parsers.dyn.parser
* **Configuration Parameters:**


# Fraunhofer

## DGA Archive

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Fraunhofer DGA collector fetches data from Fraunhofer's domain generation archive.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_password`: `{{ your password}}`
*  * `http_url`: `https://dgarchive.caad.fkie.fraunhofer.de/today`
*  * `http_username`: `{{ your username}}`
*  * `name`: `DGA Archive`
*  * `provider`: `Fraunhofer`
*  * `rate_limit`: `10800`

### Parser

* **Module:** intelmq.bots.parsers.fraunhofer.parser_dga
* **Configuration Parameters:**


# HPHosts

## Hosts

* **Status:** off
* **Revision:** 20-01-2018
* **Description:** hpHosts is a community managed and maintained hosts file that allows an additional layer of protection against access to ad, tracking and malicious websites.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://hosts-file.net/download/hosts.txt`
*  * `name`: `Hosts`
*  * `provider`: `HPHosts`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.hphosts.parser
* **Configuration Parameters:**
*  * `error_log_message`: `false`


# Malc0de

## Bind Format

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** This feed includes FQDN's of malicious hosts, the file format is in Bind file format.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://malc0de.com/bl/ZONES`
*  * `name`: `Bind Format`
*  * `provider`: `Malc0de`
*  * `rate_limit`: `10800`

### Parser

* **Module:** intelmq.bots.parsers.malc0de.parser
* **Configuration Parameters:**


## IP Blacklist

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** This feed includes IP Addresses of malicious hosts.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://malc0de.com/bl/IP_Blacklist.txt`
*  * `name`: `IP Blacklist`
*  * `provider`: `Malc0de`
*  * `rate_limit`: `10800`

### Parser

* **Module:** intelmq.bots.parsers.malc0de.parser
* **Configuration Parameters:**


## Windows Format

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** This feed includes FQDN's of malicious hosts, the file format is in Windows Hosts file format.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://malc0de.com/bl/BOOT`
*  * `name`: `Windows Format`
*  * `provider`: `Malc0de`
*  * `rate_limit`: `10800`

### Parser

* **Module:** intelmq.bots.parsers.malc0de.parser
* **Configuration Parameters:**


# Malware Domain List

## Blacklist

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** No description provided by feed provider.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://www.malwaredomainlist.com/updatescsv.php`
*  * `name`: `Blacklist`
*  * `provider`: `Malware Domain List`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.malwaredomainlist.parser
* **Configuration Parameters:**


# Malware Domains

## Malicious

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Malware Prevention through Domain Blocking (Black Hole DNS Sinkhole)

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://mirror1.malwaredomains.com/files/domains.txt`
*  * `name`: `Malicious`
*  * `provider`: `Malware Domains`
*  * `rate_limit`: `172800`

### Parser

* **Module:** intelmq.bots.parsers.malwaredomains.parser
* **Configuration Parameters:**


# MalwarePatrol

## DansGuardian

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Malware block list with URLs

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://lists.malwarepatrol.net/cgi/getfile?receipt={{ your API key }}&product=8&list=dansguardian`
*  * `name`: `DansGuardian`
*  * `provider`: `MalwarePatrol`
*  * `rate_limit`: `180000`

### Parser

* **Module:** intelmq.bots.parsers.malwarepatrol.parser_dansguardian
* **Configuration Parameters:**


# MalwareURL

## Latest malicious activity

* **Status:** on
* **Revision:** 05-02-2018
* **Description:** Latest malicious domains/IPs.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.malwareurl.com/`
*  * `name`: `Latest malicious activity`
*  * `provider`: `MalwareURL`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.malwareurl.parser
* **Configuration Parameters:**


# Microsoft

## BingMURLs

* **Status:** on
* **Revision:** 29-05-2018
* **Description:** Collects Malicious URLs detected by Bing from the Interflow API.
* **Additional Information:** Depending on the file sizes you may need to increase the parameter 'http_timeout_sec' of the collector.

### Collector

* **Module:** intelmq.bots.collectors.microsoft.collector_interflow
* **Configuration Parameters:**
*  * `api_key`: `{{your API key}}`
*  * `file_match`: `^bingmurls_`
*  * `http_timeout_sec`: `300`
*  * `name`: `BingMURLs`
*  * `not_older_than`: `2 days`
*  * `provider`: `Microsoft`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.microsoft.parser_bingmurls
* **Configuration Parameters:**


## CTIP

* **Status:** on
* **Revision:** 06-03-2018
* **Description:** Collects CTIP files from the Interflow API.
* **Additional Information:** Depending on the file sizes you may need to increase the parameter 'http_timeout_sec' of the collector. As many IPs occur very often in the data, you may want to use a deduplicator specifically for the feed.

### Collector

* **Module:** intelmq.bots.collectors.microsoft.collector_interflow
* **Configuration Parameters:**
*  * `api_key`: `{{your API key}}`
*  * `file_match`: `^ctip_`
*  * `http_timeout_sec`: `300`
*  * `name`: `CTIP`
*  * `not_older_than`: `2 days`
*  * `provider`: `Microsoft`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.microsoft.parser_ctip
* **Configuration Parameters:**


# Netlab 360

## DGA

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** This feed lists DGA family, Domain, Start and end of valid time(UTC) of a number of DGA families. reference: http://data.netlab.360.com/dga

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://data.netlab.360.com/feeds/dga/dga.txt`
*  * `name`: `DGA`
*  * `provider`: `Netlab 360`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.netlab_360.parser
* **Configuration Parameters:**


## Magnitude EK

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** This feed lists FQDN and possibly the URL used by Magnitude Exploit Kit. Information also includes the IP address used for the domain and last time seen. reference: http://data.netlab.360.com/ek

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://data.netlab.360.com/feeds/ek/magnitude.txt`
*  * `name`: `Magnitude EK`
*  * `provider`: `Netlab 360`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.netlab_360.parser
* **Configuration Parameters:**


## Mirai Scanner

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** This feed provides IP addresses which actively scan for vulnerable IoT devices and install Mirai Botnet. reference: http://data.netlab.360.com/mirai-scanner/

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://data.netlab.360.com/feeds/mirai-scanner/scanner.list`
*  * `name`: `Mirai Scanner`
*  * `provider`: `Netlab 360`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.netlab_360.parser
* **Configuration Parameters:**


# Nothink

## DNS Attack

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** This feed provides attack information for attack information against DNS honeypots. reference: http://www.nothink.org/honeypot_dns.php .

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://www.nothink.org/honeypot_dns_attacks.txt`
*  * `name`: `DNS Attack`
*  * `provider`: `Nothink`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.nothink.parser
* **Configuration Parameters:**


## SNMP

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** There are a number of feeds you can use to depend on how far back you would like to go. The time.source will still be the date and time the feed was generated at nothink. This feed provides IP addresses of systems that have connected to a honeypot via SNMP in the last 24 hours. reference: http://www.nothink.org/honeypot_snmp.php

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://www.nothink.org/blacklist/blacklist_snmp_day.txt`
*  * `name`: `SNMP`
*  * `provider`: `Nothink`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.nothink.parser
* **Configuration Parameters:**


## SSH

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** There are a number of feeds you can use to depend on how far back you would like to go. The time.source will still be the date and time the feed was generated at nothink. This feed provides IP addresses of systems that have connected to a honeypot via SSH in the last 24 hours. Reference: http://www.nothink.org/honeypots.php

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://www.nothink.org/blacklist/blacklist_ssh_day.txt`
*  * `name`: `SSH`
*  * `provider`: `Nothink`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.nothink.parser
* **Configuration Parameters:**


## Telnet

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** There are a number of feeds you can use to depend on how far back you would like to go. The time.source will still be the date and time the feed was generated at nothink. This feed provides IP addresses of systems that have connected to a honeypot via Telnet in the last 24 hours. reference: http://www.nothink.org/honeypots.php

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://www.nothink.org/blacklist/blacklist_telnet_day.txt`
*  * `name`: `Telnet`
*  * `provider`: `Nothink`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.nothink.parser
* **Configuration Parameters:**


# OpenPhish

## Phishing

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** OpenPhish is a fully automated self-contained platform for phishing intelligence. It identifies phishing sites and performs intelligence analysis in real time without human intervention and without using any external resources, such as blacklists.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.openphish.com/feed.txt`
*  * `name`: `Phishing`
*  * `provider`: `OpenPhish`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.openphish.parser
* **Configuration Parameters:**


# OpenPhish Commercial

## Phishing

* **Status:** on
* **Revision:** 06-02-2018
* **Description:** OpenPhish is a fully automated self-contained platform for phishing intelligence. It identifies phishing sites and performs intelligence analysis in real time without human intervention and without using any external resources, such as blacklists.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_password`: `{{ your password}}`
*  * `http_url`: `https://openphish.com/prvt-intell/`
*  * `http_username`: `{{ your username}}`
*  * `name`: `Phishing`
*  * `provider`: `OpenPhish Commercial`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.openphish.parser_commercial
* **Configuration Parameters:**


# PhishTank

## Online

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** PhishTank is a collaborative clearing house for data and information about phishing on the Internet.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://data.phishtank.com/data/{{ your API key }}/online-valid.csv`
*  * `name`: `Online`
*  * `provider`: `PhishTank`
*  * `rate_limit`: `28800`

### Parser

* **Module:** intelmq.bots.parsers.phishtank.parser
* **Configuration Parameters:**


# ShadowServer

## Custom

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Shadowserver sends out a variety of reports (see https://www.shadowserver.org/wiki/pmwiki.php/Services/Reports). The reports can be retrieved from the URL in the mail or from the attachment.

### Collector

* **Module:** intelmq.bots.collectors.mail.collector_mail_attach
* **Configuration Parameters:**
*  * `attach_regex`: `csv.zip`
*  * `attach_unzip`: `True`
*  * `folder`: `INBOX`
*  * `mail_host`: `__HOST__`
*  * `mail_password`: `__PASSWORD__`
*  * `mail_ssl`: `True`
*  * `mail_user`: `__USERNAME__`
*  * `name`: `Custom`
*  * `provider`: `ShadowServer`
*  * `rate_limit`: `86400`
*  * `subject_regex`: `__REGEX__`

### Parser

* **Module:** intelmq.bots.parsers.shadowserver.parser
* **Configuration Parameters:**


# Spamhaus

## ASN Drop

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** ASN-DROP contains a list of Autonomous System Numbers controlled by spammers or cyber criminals, as well as "hijacked" ASNs. ASN-DROP can be used to filter BGP routes which are being used for malicious purposes.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.spamhaus.org/drop/asndrop.txt`
*  * `name`: `ASN Drop`
*  * `provider`: `Spamhaus`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.spamhaus.parser_drop
* **Configuration Parameters:**


## CERT

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Spamhaus CERT Insight Portal. Access limited to CERTs and CSIRTs with national or regional responsibility. https://www.spamhaus.org/news/article/705/spamhaus-launches-cert-insight-portal .

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `{{ your CERT portal URL }}`
*  * `name`: `CERT`
*  * `provider`: `Spamhaus`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.spamhaus.parser_cert
* **Configuration Parameters:**


## Drop

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** The DROP list will not include any IP address space under the control of any legitimate network - even if being used by "the spammers from hell". DROP will only include netblocks allocated directly by an established Regional Internet Registry (RIR) or National Internet Registry (NIR) such as ARIN, RIPE, AFRINIC, APNIC, LACNIC or KRNIC or direct RIR allocations.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.spamhaus.org/drop/drop.txt`
*  * `name`: `Drop`
*  * `provider`: `Spamhaus`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.spamhaus.parser_drop
* **Configuration Parameters:**


## Dropv6

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** The DROPv6 list includes IPv6 ranges allocated to spammers or cyber criminals. DROPv6 will only include IPv6 netblocks allocated directly by an established Regional Internet Registry (RIR) or National Internet Registry (NIR) such as ARIN, RIPE, AFRINIC, APNIC, LACNIC or KRNIC or direct RIR allocations.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.spamhaus.org/drop/dropv6.txt`
*  * `name`: `Dropv6`
*  * `provider`: `Spamhaus`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.spamhaus.parser_drop
* **Configuration Parameters:**


## EDrop

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** EDROP is an extension of the DROP list that includes sub-allocated netblocks controlled by spammers or cyber criminals. EDROP is meant to be used in addition to the direct allocations on the DROP list.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.spamhaus.org/drop/edrop.txt`
*  * `name`: `EDrop`
*  * `provider`: `Spamhaus`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.spamhaus.parser_drop
* **Configuration Parameters:**


# Sucuri

## Hidden IFrames

* **Status:** on
* **Revision:** 28-01-2018
* **Description:** Latest hidden iframes identified on compromised web sites.
* **Additional Information:** Please note that the parser only extracts the hidden iframes  and the conditional redirects, not the encoded javascript.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://labs.sucuri.net/?malware`
*  * `name`: `Hidden IFrames`
*  * `provider`: `Sucuri`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.sucuri.parser
* **Configuration Parameters:**


# Taichung

## Netflow

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Abnormal flows detected.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.tc.edu.tw/net/netflow/lkout/recent/30`
*  * `name`: `Netflow`
*  * `provider`: `Taichung`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.taichung.parser
* **Configuration Parameters:**
*  * `error_log_message`: `false`


# Team Cymru

## CAP

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Team Cymru provides daily lists of compromised or abused devices for the ASNs and/or netblocks with a CSIRT's jurisdiction. This includes such information as bot infected hosts, command and control systems, open resolvers, malware urls, phishing urls, and brute force attacks

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_password`: `{{your password}}`
*  * `http_url`: `https://www.cymru.com/{{your organization name}}/infected_{time[%Y%m%d]}.txt`
*  * `http_url_formatting`: `True`
*  * `http_username`: `{{your login}}`
*  * `name`: `CAP`
*  * `provider`: `Team Cymru`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.cymru.parser_cap_program
* **Configuration Parameters:**


## Full Bogons

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** Fullbogons are a larger set which also includes IP space that has been allocated to an RIR, but not assigned by that RIR to an actual ISP or other end-user. IANA maintains a convenient IPv4 summary page listing allocated and reserved netblocks, and each RIR maintains a list of all prefixes that they have assigned to end-users. Our bogon reference pages include additional links and resources to assist those who wish to properly filter bogon prefixes within their networks.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt`
*  * `name`: `Full Bogons`
*  * `provider`: `Team Cymru`
*  * `rate_limit`: `129600`

### Parser

* **Module:** intelmq.bots.parsers.cymru.parser_full_bogons
* **Configuration Parameters:**


# Threatminer

## Recent domains

* **Status:** on
* **Revision:** 06-02-2018
* **Documentation:** https://www.threatminer.org/
* **Description:** Latest malicious domains.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.threatminer.org/`
*  * `name`: `Recent domains`
*  * `provider`: `Threatminer`
*  * `rate_limit`: `86400`

### Parser

* **Module:** intelmq.bots.parsers.threatminer.parser
* **Configuration Parameters:**


# Turris

## Greylist

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** The data are processed and clasified every week and behaviour of IP addresses that accessed a larger number of Turris routers is evaluated. The result is a list of addresses that have tried to obtain information about services on the router or tried to gain access to them. We publish this so called "greylist" that also contains a list of tags for each address which indicate what behaviour of the address was observed.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://www.turris.cz/greylist-data/greylist-latest.csv`
*  * `name`: `Greylist`
*  * `provider`: `Turris`
*  * `rate_limit`: `43200`

### Parser

* **Module:** intelmq.bots.parsers.turris.parser
* **Configuration Parameters:**


# URLVir

## Hosts

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** This feed provides FQDN's or IP addresses for Active Malicious Hosts.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://www.urlvir.com/export-hosts/`
*  * `name`: `Hosts`
*  * `provider`: `URLVir`
*  * `rate_limit`: `129600`

### Parser

* **Module:** intelmq.bots.parsers.urlvir.parser
* **Configuration Parameters:**


## IPs

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** This feed provides IP addresses hosting Malware.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://www.urlvir.com/export-ip-addresses/`
*  * `name`: `IPs`
*  * `provider`: `URLVir`
*  * `rate_limit`: `129600`

### Parser

* **Module:** intelmq.bots.parsers.urlvir.parser
* **Configuration Parameters:**


# University of Toulouse

## Blacklist

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** The collections and feed description can be found on: https://dsi.ut-capitole.fr/blacklists/.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `extract_files`: `true`
*  * `http_url`: `https://dsi.ut-capitole.fr/blacklists/download/{collection name}.tar.gz`
*  * `name`: `Blacklist`
*  * `provider`: `University of Toulouse`
*  * `rate_limit`: `43200`

### Parser

* **Module:** intelmq.bots.parsers.generic.parser_csv
* **Configuration Parameters:**
*  * `columns`: `{depends on a collection}`
*  * `delimiter`: `false`
*  * `type`: `{depends on a collection}`


# VXVault

## IPs

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** This feed provides IP addresses hosting Malware.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `http://vxvault.net/URL_List.php`
*  * `name`: `IPs`
*  * `provider`: `VXVault`
*  * `rate_limit`: `3600`

### Parser

* **Module:** intelmq.bots.parsers.vxvault.parser
* **Configuration Parameters:**


# WebInspektor

## Unsafe sites

* **Status:** on
* **Revision:** 09-03-2018
* **Description:** Latest detected unsafe sites.

### Collector

* **Module:** intelmq.bots.collectors.http.collector_http
* **Configuration Parameters:**
*  * `http_url`: `https://app.webinspector.com/public/recent_detections/`
*  * `name`: `Unsafe sites`
*  * `provider`: `WebInspektor`
*  * `rate_limit`: `60`

### Parser

* **Module:** intelmq.bots.parsers.webinspektor.parser
* **Configuration Parameters:**


# ZoneH

## Defacements

* **Status:** on
* **Revision:** 20-01-2018
* **Description:** all the information contained in Zone-H's cybercrime archive were either collected online from public sources or directly notified anonymously to us.

### Collector

* **Module:** intelmq.bots.collectors.mail.collector_mail_attach
* **Configuration Parameters:**
*  * `attach_regex`: `csv`
*  * `attach_unzip`: `False`
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

* **Module:** intelmq.bots.parsers.zoneh.parser
* **Configuration Parameters:**


