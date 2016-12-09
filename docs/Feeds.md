# Available Feeds

The available feeds are grouped by the source of the feeds. For each feed the collector and parser that can be used is documented as well as any feed-specific parameters.

<!-- TOC depthFrom:2 depthTo:2 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Abuse.ch](#abusech)
- [AlienVault](#alienvault)
- [Autoshun](#autoshun)
- [Bambenek](#bambenek)
- [Bitcash](#bitcash)
- [BitSight Ciberfeed Stream](#bitsight-ciberfeed-stream)
- [Blocklist.de](#blocklistde)
- [Blueliv Crimeserver](#blueliv-crimeserver)
- [CI Army](#ci-army)
- [CleanMX](#cleanmx)
- [Cymru](#cymru)
- [DShield](#dshield)
- [Danger Rulez](#danger-rulez)
- [Dataplane](#dataplane)
- [DynDNS](#dyndns)
- [Fraunhofer DGA](#fraunhofer-dga)
- [HPHosts](#hphosts)
- [Malc0de](#malc0de)
- [Malware Domain List](#malware-domain-list)
- [Malware Domains](#malware-domains)
- [MalwarePatrol Dans Guardian](#malwarepatrol-dans-guardian)
- [N6](#n6)
- [Netlab 360](#netlab-360)
- [Nothink](#nothink)
- [OpenBL](#openbl)
- [OpenPhish](#openphish)
- [PhishTank](#phishtank)
- [Shadowserver](#shadowserver)
- [Spamhaus](#spamhaus)
- [Taichung](#taichung)
- [Turris Greylist](#turris-greylist)
- [URLVir](#urlvir)
- [VXVault](#vxvault)

<!-- /TOC -->

---

## Abuse.ch

### Feodo Tracker Domains

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://feodotracker.abuse.ch/blocklist/?download=domainblocklist

Parser: Abuse.ch Domain (`intelmq.bots.parsers.abusech.parser_domain`)

The Feodo Tracker Feodo Domain Blocklist contains domain names (FQDN) used as C&C communication channel by the Feodo Trojan. These domains names are usually registered and operated by cybercriminals for the exclusive purpose of hosting a Feodo botnet controller. Hence you should expect no legit traffic to those domains. I highly recommend you to block/drop any traffic towards any Feodo C&C domain by using the Feodo Domain Blocklist. Please consider that domain names are usually only used by version B of the Feodo Trojan. C&C communication channels used by version A, version C and version D are not covered by this blocklist.

### Feodo Tracker IPs

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://feodotracker.abuse.ch/blocklist/?download=ipblocklist

Parser: Abuse.ch IP (`intelmq.bots.parsers.abusech.parser_ip`)

The Feodo Tracker Feodo IP Blocklist contains IP addresses (IPv4) used as C&C communication channel by the Feodo Trojan. This lists contains two types of IP address: Feodo C&C servers used by version A, version C and version D of the Feodo Trojan (these IP addresses are usually compromised servers running an nginx daemon on port 8080 TCP or 7779 TCP that is acting as proxy, forwarding all traffic to a tier 2 proxy node) and Feodo C&C servers used by version B which are usually used for the exclusive purpose of hosting a Feodo C&C server. Attention: Since Feodo C&C servers associated with version A, version C and version D are usually hosted on compromised servers, its likely that you also block/drop legit traffic e.g. towards websites hosted on a certain IP address acting as Feodo C&C for version A, version C and version D. If you only want to block/drop traffic to Feodo C&C servers hosted on bad IPs (version B), please use the blocklist BadIPs documented below.


### Ransomware Tracker

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://ransomwaretracker.abuse.ch/feeds/csv/

Parser: Abuse.ch Ranswomware (`intelmq.bots.parsers.abusech.parser_ransomware`)

Ransomware Tracker feed includes FQDN's, URL's, and known IP addresses that were used for said FQDN's and URL's for various ransomware families.


### ZeuS Tracker Domains

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://zeustracker.abuse.ch/blocklist.php?download=baddomains

Parser: Abuse.ch Domain (`intelmq.bots.parsers.abusech.parser_domain`)

The ZeuS domain blocklist (BadDomains) is the recommended blocklist if you want to block only ZeuS domain names. It has domain names that ZeuS Tracker believes to be hijacked (level 2). Hence the false positive rate should be much lower compared to the standard ZeuS domain blocklist.

### ZeuS Tracker IPs

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://zeustracker.abuse.ch/blocklist.php?download=badips

Parser: Abuse.ch IP (`intelmq.bots.parsers.abusech.parser_ip`)

This list only includes IPv4 addresses that are used by the ZeuS Trojan. It is the recommended list if you want to block only ZeuS IPs. It excludes IP addresses that ZeuS Tracker believes to be hijacked (level 2) or belong to a free web hosting provider (level 3). Hence the false positive rate should be much lower compared to the standard ZeuS IP blocklist.


## AlienVault

### URL

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://reputation.alienvault.com/reputation.data

Parser: AlienVault (`intelmq.bots.parsers.alienvault.parser`)


### OTX

Status: Unknown
Collector: AlienVault OTX (`intelmq.bots.collectors.alienvault_otx.collector`)
 * api_key: {{ your API key }}

Parser: AlienVault OTX (`intelmq.bots.parsers.alienvault.parser_otx`)

AlienVault OTX Collector is the bot responsible to get the report through the API. Report could vary according to subscriptions.


## Autoshun

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://www.autoshun.org/files/shunlist.html

Parser: Autoshun (`intelmq.bots.parsers.autoshun.parser`)

You need to register in order to use the list.


## Bambenek

### C2-dommasterlist

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt

Parser: Bambenek C2 Domain Feed (`intelmq.bots.parsers.bambenek.parser`)

Master Feed of known, active and non-sinkholed C&Cs domain names.
 * License: http://osint.bambenekconsulting.com/license.txt

### C2-ipmasterlist

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt

Parser: Bambenek C2 IP Feed (`intelmq.bots.parsers.bambenek.parser`)

Master Feed of known, active and non-sinkholed C&Cs IP addresses
 * License: http://osint.bambenekconsulting.com/license.txt

### DGA Domain Feed

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://osint.bambenekconsulting.com/feeds/dga-feed.txt

Parser: Bambenek DGA Domain Feed (`intelmq.bots.parsers.bambenek.parser`)

Domain feed of known DGA domains from -2 to +3 days
 * License: http://osint.bambenekconsulting.com/license.txt


## Bitcash

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://bitcash.cz/misc/log/blacklist

Parser: Bitcash Blocklist Feed (`intelmq.bots.parsers.bitcash.parser`)

Blocklist provided by bitcash.cz of banned IPs for service abuse, this includes scanning, sniffing, harvesting, and dos attacks.


## BitSight Ciberfeed Stream

Status: Unknown
Collector: BitSight Ciberfeed Stream (`intelmq.bots.collectors.bitsight.collector`)
 * http_url: http://alerts.bitsighttech.com:8080/stream?key={{ your api key }}

Parser: BitSight Ciberfeed Stream (`intelmq.bots.parsers.bitsight.parser`)

Bitsight Collector is the bot responsible to get Bitsight Ciberfeed Alert Stream


## Blocklist.de

### Apache

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://lists.blocklist.de/lists/apache.txt

Parser: Blocklist.de (`intelmq.bots.parsers.blocklistde.parser`)

BlockList.DE Apache Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service Apache, Apache-DDOS, RFI-Attacks.

### Bots

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://lists.blocklist.de/lists/bots.txt

Parser: Blocklist.de (`intelmq.bots.parsers.blocklistde.parser`)

BlockList.DE Bots Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks attacks on the RFI-Attacks, REG-Bots, IRC-Bots or BadBots (BadBots = he has posted a Spam-Comment on a open Forum or Wiki).

### Brute-force Login

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://lists.blocklist.de/lists/bruteforcelogin.txt

Parser: Blocklist.de (`intelmq.bots.parsers.blocklistde.parser`)

BlockList.DE Brute-force Login Collector is the bot responsible to get the report from source of information. All IPs which attacks Joomlas, Wordpress and other Web-Logins with Brute-Force Logins.

### FTP

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://lists.blocklist.de/lists/ftp.txt

Parser: Blocklist.de (`intelmq.bots.parsers.blocklistde.parser`)

BlockList.DE FTP Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours for attacks on the Service FTP.

### IMAP

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://lists.blocklist.de/lists/imap.txt

Parser: Blocklist.de (`intelmq.bots.parsers.blocklistde.parser`)

BlockList.DE IMAP Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours for attacks on the Service IMAP, SASL, POP3.....

### IRC Bot

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://lists.blocklist.de/lists/ircbot.txt

Parser: Blocklist.de (`intelmq.bots.parsers.blocklistde.parser`)

### Mail

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://lists.blocklist.de/lists/mail.txt

Parser: Blocklist.de (`intelmq.bots.parsers.blocklistde.parser`)

BlockList.DE Mail Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service Mail, Postfix.

### SIP

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://lists.blocklist.de/lists/sip.txt

Parser: Blocklist.de (`intelmq.bots.parsers.blocklistde.parser`)

BlockList.DE SIP Collector is the bot responsible to get the report from source of information. All IP addresses that tried to login in a SIP-, VOIP- or Asterisk-Server and are included in the IPs-List from http://www.infiltrated.net/ (Twitter).

### SSH

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://lists.blocklist.de/lists/ssh.txt

Parser: Blocklist.de (`intelmq.bots.parsers.blocklistde.parser`)

BlockList.DE SSH Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service SSH.

### Strong IPs

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://lists.blocklist.de/lists/strongips.txt

Parser: Blocklist.de (`intelmq.bots.parsers.blocklistde.parser`)

BlockList.DE Strong IPs Collector is the bot responsible to get the report from source of information. All IPs which are older then 2 month and have more then 5.000 attacks.


## Blueliv Crimeserver

Status: Unknown
Collector: Blueliv Crimeserver (`intelmq.bots.collectors.blueliv.collector_crimeserver`)

Parser: Blueliv Crimeserver (`intelmq.bots.parsers.blueliv.parser_crimeserver`)

Blueliv Crimeserver Collector is the bot responsible to get the report through the API.

## CI Army

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://cinsscore.com/list/ci-badguys.txt"

Parser: CI Army (`intelmq.bots.parsers.ci_army.parser`)

## CleanMX

In order to download the CleanMX feed you need to use a custom user agent and
register that user agent.

### Phishing

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://support.clean-mx.de/clean-mx/xmlphishing?response=alive&format=csv&domain=
 * http_user_agent: {{ your user agent }}
Parser: CleanMX Phishing (`intelmq.bots.parsers.cleanmx.parser_phishing`)

### Virus

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://support.clean-mx.de/clean-mx/xmlviruses?response=alive&format=csv&domain=
 * http_user_agent: {{ your user agent }}
Parser: CleanMX Virus (`intelmq.bots.parsers.cleanmx.parser_virus`)

## Cymru

### Full Bogons

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt

Parser: Cymru Full Bogons (`intelmq.bots.parsers.cymru_full_bogons.parser`)

## DShield

### AS

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://dshield.org/asdetailsascii.html?as={{ AS Number }}

Parser: DShield AS (`intelmq.bots.parsers.dshield.parser_asn`)

### Block

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://www.dshield.org/block.txt

Parser: DShield Block (`intelmq.bots.parsers.dshield.parser_block`)

### Suspicious Domains

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://www.dshield.org/feeds/suspiciousdomains_High.txt

Parser: DShield Suspicious Domain (`intelmq.bots.parsers.dshield.parser_domain`)


## Danger Rulez

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://danger.rulez.sk/projects/bruteforceblocker/blist.php

Parser: Danger Rulez (`intelmq.bots.parsers.danger_rulez.parser`)


## Dataplane

### SIP Invitation

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://dataplane.org/sipinvitation.txt

Parser: Dataplane Feeds (`intelmq.bots.parsers.dataplane.parser`)

Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP INVITE operation to a remote host.  The report lists hosts that are suspicious of more than just port scanning.  These hosts may be SIP client cataloging or conducting various forms of telephony abuse.  
Report is updated hourly.

### SIP Query

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://dataplane.org/sipquery.txt

Parser: Dataplane Feeds (`intelmq.bots.parsers.dataplane.parser`)

Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP OPTIONS query to a remote host.  This report lists hosts that are suspicious of more than just port scanning.  The hosts may be SIP server cataloging or conducting various forms of telephony abuse.  
Report is updated hourly.

### SIP Registration

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://dataplane.org/sipregistration.txt

Parser: Dataplane Feeds (`intelmq.bots.parsers.dataplane.parser`)

Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP REGISTER operation to a remote host.  This report lists hosts that are suspicious of more than just port scanning.  The hosts may be SIP client cataloging or conducting various forms of telephony abuse.  
Report is updated hourly.

### SSH Client Connection

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://dataplane.org/sshclient.txt

Parser: Dataplane Feeds (`intelmq.bots.parsers.dataplane.parser`)

Entries below consist of fields with identifying characteristics of a source IP address that has been seen initiating an SSH connection to a remote host.  This report lists hosts that are suspicious of more than just port scanning.  The hosts may be SSH server cataloging or conducting authentication attack attempts.  
Report is updated hourly.

### SSH Password Authentication

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://dataplane.org/sshpwauth.txt

Parser: Dataplane Feeds (`intelmq.bots.parsers.dataplane.parser`)

Entries below consist of fields with identifying characteristics of a source IP address that has been seen attempting to remotely login to a host using SSH password authentication.  The report lists hosts that are highly suspicious and are likely conducting malicious SSH password authentication attacks.
Report is updated hourly.


## DynDNS

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://security-research.dyndns.org/pub/malware-feeds/ponmocup-infected-domains-CIF-latest.txt

Parser: DynDNS ponmocup Domains (`intelmq.bots.parsers.dyn.parser`)

DynDNS ponmocup. List of ponmocup malware redirection domains and infected web-servers. See also http://security-research.dyndns.org/pub/botnet-links.html

## Fraunhofer DGA

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://dgarchive.caad.fkie.fraunhofer.de/today
 * http_username: {{ your username}}
 * http_password: {{ your password }}

Parser: Fraunhofer DGA (`intelmq.bots.parsers.fraunhofer.parser_dga`)

Fraunhofer DGA collector fetches data from Fraunhofer's domain generation archive.

## HPHosts

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://hosts-file.net/download/hosts.txt

Parser: HPHosts (`intelmq.bots.parsers.hphosts.parser`)
 * error_log_message: false

## Malc0de

### Windows Format

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://malc0de.com/bl/BOOT

Parser: Malc0de (`intelmq.bots.parsers.malc0de.parser`)

This feed includes FQDN's of malicious hosts, the file format is in Windows Hosts file format.

### Bind Format

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://malc0de.com/bl/BOOT

Parser: Malc0de (`intelmq.bots.parsers.malc0de.parser`)

This feed includes FQDN's of malicious hosts, the file format is in Bind format.

### IP Blacklist

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://malc0de.com/bl/IP_Blacklist.txt

Parser: Malc0de IP Blacklist (`intelmq.bots.parsers.malc0de.parser_ip_blacklist`)

This feed includes IP Addresses of malicious hosts.


## Malware Domain List

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://www.malwaredomainlist.com/updatescsv.php

Parser: Malware Domain List (`intelmq.bots.parsers.malwaredomainlist.parser`)

## Malware Domains

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://mirror2.malwaredomains.com/files/domains.txt

Parser: Malware Domains (`intelmq.bots.parsers.malwaredomains.parser`)

## MalwarePatrol Dans Guardian

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://lists.malwarepatrol.net/cgi/getfile?receipt={{ API KEY }}&product=8&list=dansguardian

Parser: MalwarePatrol Dans Guardian (`intelmq.bots.parsers.malwarepatrol.parser_dansguardian`)

## N6

### Stomp

Status: Unknown
Collector: N6stomp (`intelmq.bots.collectors.n6.collector_stomp`)
 * server: n6stream.cert.pl
 * port: 61614
 * exchange: {{ insert your exchange point as given by CERT.pl }}
 * ssl_ca_certificate: {{ insert path to CA file for CERT.pl's n6 }}
 * ssl_client_certificate: {{ insert path to client cert file for CERTpl's n6 }}
 * ssl_client_certificate_key: {{ insert path to client cert key file for CERT.pl's n6 }}

Parser: N6Stomp (`intelmq.bots.parsers.n6.parser_n6stomp`)

N6 Collector - CERT.pl's N6 Collector - N6 feed via STOMP interface. Note that rate_limit does not apply for this bot as it is waiting for messages on a stream.

### REST API

Status: Unknown FIXME
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
  * http_url: https://n6beta.cert.pl/report/inside.json

Parser: Missing


## Netlab 360

### DGA Feed

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://data.netlab.360.com/feeds/dga/dga.txt

Parser: Netlab 360 DGA (`intelmq.bots.parsers.netlab_360.parser`)

This feed lists DGA family, Domain, Start and end of valid time(UTC) of a number of DGA families.
 * reference: http://data.netlab.360.com/dga

### Magnitude EK Feed

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://data.netlab.360.com/feeds/ek/magnitude.txt

Parser: Netlab 360 Magnitude (`intelmq.bots.parsers.netlab_360.parser`)

This feed lists FQDN and possibly the URL used by Magnitude Exploit Kit.  Information also includes the IP address used for the domain and last time seen.
 * reference: http://data.netlab.360.com/ek

## Nothink

### DNS Attack Feed

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://www.nothink.org/honeypot_dns_attacks.txt

Parser: Nothink (`intelmq.bots.parsers.nothink.parser`)

This feed provides attack information for attack information against DNS honeypots.
 * reference: http://www.nothink.org/honeypot_dns.php

### SNMP Feed

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)

There are a number of feeds you can use to depend on how far back you would like to go.  The time.source will still be the date and time the feed was generated at nothink.
 * http_url: http://www.nothink.org/blacklist/blacklist_snmp_day.txt
 * http_url: http://www.nothink.org/blacklist/blacklist_snmp_week.txt
 * http_url: http://www.nothink.org/blacklist/blacklist_snmp_year.txt

Parser: Nothink (`intelmq.bots.parsers.nothink.parser`)

This feed provides IP addresses of systems that have connected to a honeypot via SNMP in the last 24 hours.
 * reference: http://www.nothink.org/honeypot_snmp.php

### SSH Feed

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)

There are a number of feeds you can use to depend on how far back you would like to go.  The time.source will still be the date and time the feed was generated at nothink.
 * http_url: http://www.nothink.org/blacklist/blacklist_ssh_day.txt
 * http_url: http://www.nothink.org/blacklist/blacklist_ssh_week.txt
 * http_url: http://www.nothink.org/blacklist/blacklist_ssh_year.txt

Parser: Nothink (`intelmq.bots.parsers.nothink.parser`)

This feed provides IP addresses of systems that have connected to a honeypot via SSH in the last 24 hours.
 * reference: http://www.nothink.org/honeypots.php

### Telnet Feed

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)

There are a number of feeds you can use to depend on how far back you would like to go.  The time.source will still be the date and time the feed was generated at nothink.
 * http_url: http://www.nothink.org/blacklist/blacklist_telnet_day.txt
 * http_url: http://www.nothink.org/blacklist/blacklist_telnet_week.txt
 * http_url: http://www.nothink.org/blacklist/blacklist_telnet_year.txt

Parser: Nothink (`intelmq.bots.parsers.nothink.parser`)

This feed provides IP addresses of systems that have connected to a honeypot via Telnet in the last 24 hours.
 * reference: http://www.nothink.org/honeypots.php


## OpenBL

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
  * http_url: https://www.openbl.org/lists/date_all.txt

Parser: OpenBL (`intelmq.bots.parsers.openbl.parser`)

## OpenPhish

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
  * http_url: https://www.openphish.com/feed.txt

Parser: OpenPhish (`intelmq.bots.parsers.openphish.parser`)

## PhishTank

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
  * http_url: https://data.phishtank.com/data/{{ your API key }}/online-valid.csv

Parser: PhishTank (`intelmq.bots.parsers.phishtank.parser`)

## Shadowserver

Status: Unknown

Collector: Generic Mail URL Fetcher (`intelmq.bots.collectors.mail.collector_mail_url`)
 * subject_regex: (see individual reports below)
 * url_regex: https://dl.shadowserver.org/[^ ]+

Collector: Generic Mail Attachment Fetcher (`intelmq.bots.collectors.mail.collector_mail_attach`)
 * subject_regex: (see individual reports below)
 * attach_regex: csv.zip
 * attach_unzip: true

Parser: Shadowserver

Shadowserver sends out a variety of reports (see https://www.shadowserver.org/wiki/pmwiki.php/Services/Reports). The reports can be retrieved from the URL in the mail or from the attachment. These are some of the subjects of the mails:

 - Shadowserver [^ ]+ Chargen Report
 - Shadowserver [^ ]+ Drone Report
 - Shadowserver [^ ]+ Microsoft Sinkhole Report
 - Shadowserver [^ ]+ QOTD Report
 - Shadowserver [^ ]+ SNMP Report


## Spamhaus

### CERT

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
  * http_url: {{ your CERT portal URL }}

Parser: Spamhaus CERT (`intelmq.bots.parsers.spamhaus.parser_cert`)

Spamhaus CERT Insight Portal. Access limited to CERTs and CSIRTs with national or regional responsibility. https://www.spamhaus.org/news/article/705/spamhaus-launches-cert-insight-portal

### Drop

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
  * http_url: https://www.spamhaus.org/drop/drop.txt

Parser: Spamhaus Drop (`intelmq.bots.parsers.spamhaus.parser_drop`)

The DROP list will not include any IP address space under the control of any legitimate network - even if being used by "the spammers from hell". DROP will only include netblocks allocated directly by an established Regional Internet Registry (RIR) or National Internet Registry (NIR) such as ARIN, RIPE, AFRINIC, APNIC, LACNIC or KRNIC or direct RIR allocations.

### EDrop

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
  * http_url: https://www.spamhaus.org/drop/edrop.txt

Parser: Spamhaus Drop (`intelmq.bots.parsers.spamhaus.parser_drop`)

EDROP is an extension of the DROP list that includes suballocated netblocks controlled by spammers or cyber criminals. EDROP is meant to be used in addition to the direct allocations on the DROP list.

### Dropv6

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
  * http_url: https://www.spamhaus.org/drop/dropv6.txt

Parser: Spamhaus Drop (`intelmq.bots.parsers.spamhaus.parser_drop`)

The DROPv6 list includes IPv6 ranges allocated to spammers or cyber criminals. DROPv6 will only include IPv6 netblocks allocated directly by an established Regional Internet Registry (RIR) or National Internet Registry (NIR) such as ARIN, RIPE, AFRINIC, APNIC, LACNIC or KRNIC or direct RIR allocations.

### ASN-Drop

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
  * http_url: https://www.spamhaus.org/drop/asndrop.txt

Parser: Spamhaus Drop (`intelmq.bots.parsers.spamhaus.parser_drop`)
ASN-DROP contains a list of Autonomous System Numbers controlled by spammers or cyber criminals, as well as "hijacked" ASNs. ASN-DROP can be used to filter BGP routes which are being used for malicious purposes.


## Taichung

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://www.tc.edu.tw/net/netflow/lkout/recent/30

Parser: Taichung (`intelmq.bots.parsers.taichung.parser`)
 * error_log_message: false

## Turris Greylist

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: https://www.turris.cz/greylist-data/greylist-latest.csv

Parser: Turris Greylist (`intelmq.bots.parsers.turris.parser`)

## URLVir

### Hosts

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://www.urlvir.com/export-hosts/

Parser: URLVir Hosts (`intelmq.bots.parsers.urlvir.parser`)

This feed provides FQDN's or IP addresses for Active Malicious Hosts.

### IPs

Status: Unknown

Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://www.urlvir.com/export-ip-addresses/

Parser: URLVir IPs (`intelmq.bots.parsers.urlvir.parser`)

This feed provides IP addresses hosting Malware.


## VXVault

Status: Unknown
Collector: Generic URL Fetcher (`intelmq.bots.collectors.http.collector_http`)
 * http_url: http://vxvault.net/URL_List.php

Parser: VXVault (`intelmq.bots.parsers.vxvault.parser`)
