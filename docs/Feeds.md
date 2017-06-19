# Available Feeds

The available feeds are grouped by the source of the feeds. For each feed the collector and parser that can be used is documented as well as any feed-specific parameters.

<!-- TOC depthFrom:2 depthTo:2 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Abuse.ch](#abusech)
- [AlienVault](#alienvault)
- [Autoshun](#autoshun)
- [Bambenek](#bambenek)
- [Bitcash](#bitcash)
- [AnubisNetworks Cyberfeed Stream](#anubisnetworks-cyberfeed-stream)
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
- [Proxyspy](#proxyspy)
- [Shadowserver](#shadowserver)
- [Spamhaus](#spamhaus)
- [Taichung](#taichung)
- [Turris Greylist](#turris-greylist)
- [URLVir](#urlvir)
- [VXVault](#vxvault)

<!-- /TOC -->

---

# Abuse.ch

## Feodo Tracker Domains

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: abusech-feodo-domains-collector
provider: Abuse.ch
feed: Abuse.ch Feodo Domains
rate_limit: 129600
http_url: https://feodotracker.abuse.ch/blocklist/?download=domainblocklist
```

### Parser Bot

**Bot Name:** Abuse.ch Domain

**Bot Module:** intelmq.bots.parsers.abusech.parser_domain

**Configuration Parameters:**
```
id: abusech-feodo-domains-parser
```

**Notes:** The Feodo Tracker Feodo Domain Blocklist contains domain names (FQDN) used as C&C communication channel by the Feodo Trojan. These domains names are usually registered and operated by cybercriminals for the exclusive purpose of hosting a Feodo botnet controller. Hence you should expect no legit traffic to those domains. I highly recommend you to block/drop any traffic towards any Feodo C&C domain by using the Feodo Domain Blocklist. Please consider that domain names are usually only used by version B of the Feodo Trojan. C&C communication channels used by version A, version C and version D are not covered by this blocklist.

## Feodo Tracker IPs

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: abusech-feodo-ips-collector
provider: Abuse.ch
feed: Abuse.ch Feodo IPs
rate_limit: 129600
http_url: https://feodotracker.abuse.ch/blocklist/?download=ipblocklist
```

### Parser Bot

**Bot Name:** Abuse.ch IP

**Bot Module:** intelmq.bots.parsers.abusech.parser_ip

**Configuration Parameters:**
```
id: abusech-feodo-ips-parser
```

**Notes:** The Feodo Tracker Feodo IP Blocklist contains IP addresses (IPv4) used as C&C communication channel by the Feodo Trojan. This lists contains two types of IP address: Feodo C&C servers used by version A, version C and version D of the Feodo Trojan (these IP addresses are usually compromised servers running an nginx daemon on port 8080 TCP or 7779 TCP that is acting as proxy, forwarding all traffic to a tier 2 proxy node) and Feodo C&C servers used by version B which are usually used for the exclusive purpose of hosting a Feodo C&C server. Attention: Since Feodo C&C servers associated with version A, version C and version D are usually hosted on compromised servers, its likely that you also block/drop legit traffic e.g. towards websites hosted on a certain IP address acting as Feodo C&C for version A, version C and version D. If you only want to block/drop traffic to Feodo C&C servers hosted on bad IPs (version B), please use the blocklist BadIPs documented below.


## Ransomware Tracker

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```====
id: abusech-ransomware-collector
provider: Abuse.ch
feed: Abuse.ch Ransomware
rate_limit: 129600
http_url: https://ransomwaretracker.abuse.ch/feeds/csv/
```

### Parser Bot

**Bot Name:** Abuse.ch Ransomware

**Bot Module:** intelmq.bots.parsers.abusech.parser_ransomware

**Configuration Parameters:**
```
id: abusech-ransomware-parser
```

**Notes:** Ransomware Tracker feed includes FQDN's, URL's, and known IP addresses that were used for said FQDN's and URL's for various ransomware families.


## ZeuS Tracker Domains

**Status:** Unknown (no dates given)

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: abusech-zeus-domains-collector
provider: Abuse.ch
feed: Abuse.ch Zeus Domains
rate_limit: 129600
http_url: https://zeustracker.abuse.ch/blocklist.php?download=baddomains
```

### Parser Bot

**Bot Name:** Abuse.ch Domain

**Bot Module:** intelmq.bots.parsers.abusech.parser_domain

**Configuration Parameters:**
```
id: abusech-zeus-domains-parser
```

**Notes:** The ZeuS domain blocklist (BadDomains) is the recommended blocklist if you want to block only ZeuS domain names. It has domain names that ZeuS Tracker believes to be hijacked (level 2). Hence the false positive rate should be much lower compared to the standard ZeuS domain blocklist.

## ZeuS Tracker IPs

**Status:** Unknown (no dates given)

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: abusech-zeus-ips-collector
provider: Abuse.ch
feed: Abuse.ch Zeus IPs
rate_limit: 129600
http_url: https://zeustracker.abuse.ch/blocklist.php?download=badips
```

### Parser Bot

**Bot Name:** Abuse.ch IP

**Bot Module:** intelmq.bots.parsers.abusech.parser_ip

**Configuration Parameters:**
```
id: abusech-zeus-ips-parser
```

**Notes:** This list only includes IPv4 addresses that are used by the ZeuS Trojan. It is the recommended list if you want to block only ZeuS IPs. It excludes IP addresses that ZeuS Tracker believes to be hijacked (level 2) or belong to a free web hosting provider (level 3). Hence the false positive rate should be much lower compared to the standard ZeuS IP blocklist.


# AlienVault

## URL

**Status:** Unknown

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: alienvault-url-collector
provider: AlienVault
feed: AlienVault Reputation List
rate_limit: 3600
http_url: https://reputation.alienvault.com/reputation.data
```

### Parser Bot

**Bot Name:** AlienVault

**Bot Module:** intelmq.bots.parsers.alienvault.parser

**Configuration Parameters:**
```
id: alienvault-url-parser
```


## OTX

**Status:** Active

### Collector Bot

**Bot Name:** AlienVault OTX

**Bot Module:** intelmq.bots.collectors.alienvault_otx.collector

**Configuration Parameters:**
```
id: alienvault-otx-collector
provider: AlienVault
feed: AlienVault OTX
api_key: {{ your API key }}
```

### Parser Bot

**Bot Name:** AlienVault OTX

**Bot Module:** intelmq.bots.parsers.alienvault.parser_otx

**Configuration Parameters:**
```
id: alienvault-otx-parser
```

**Notes:** AlienVault OTX Collector is the bot responsible to get the report through the API. Report could vary according to subscriptions.


# AnubisNetworks Cyberfeed Stream

**Status:** Active

## Collector Bot

**Bot Name:** AnubisNetworks Cyberfeed Stream

**Bot Module:** intelmq.bots.collectors.http.collector_http_stream

**Configuration Parameters:**
```
id: anubisnetworks-collector
provider: AnubisNetworks
feed: AnubisNetworks Cyberfeed
http_url: https://prod.cyberfeed.net/stream?key={{ your api key }}
strip_lines: true
```

## Parser Bot

**Bot Name:** AnubisNetworks Cyberfeed Stream

**Bot Module:** intelmq.bots.parsers.anubisnetworks.parser

**Configuration Parameters:**
```
id: anubisnetworks-parser
```

**Notes:** AnubisNetworks Collector is the bot responsible to get AnubisNetworks Cyberfeed Stream.


# Autoshun

**Status:** Unknown

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: autoshun-collector
provider: Autoshun
feed: Autoshun List
rate_limit: 3600
http_url: https://www.autoshun.org/files/shunlist.html
```

## Parser Bot

**Bot Name:** Autoshun

**Bot Module:** intelmq.bots.parsers.autoshun.parser

**Configuration Parameters:**
```
id: autoshun-parser
```

**Notes:** You need to register in order to use the list.


# Bambenek

## C2 Domains

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: bambenek-c2-domains-collector
provider: Bambenek
feed: Bambenek C2 Domains
rate_limit: FIXME
http_url: http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt
```

### Parser Bot

**Bot Name:** Bambenek C2 Domain Feed

**Bot Module:** intelmq.bots.parsers.bambenek.parser

**Configuration Parameters:**
```
id: bambenek-c2-domains-parser
```

**Notes:** Master Feed of known, active and non-sinkholed C&Cs domain names.
License: http://osint.bambenekconsulting.com/license.txt

## C2 IPs

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: bambenek-c2-ips-collector
provider: Bambenek
feed: Bambenek C2 IPs
rate_limit: FIXME
http_url: http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt
```

### Parser Bot

**Bot Name:** Bambenek C2 IP Feed

**Bot Module:** intelmq.bots.parsers.bambenek.parser

**Configuration Parameters:**
```
id: bambenek-c2-ips-parser
```

**Notes:** Master Feed of known, active and non-sinkholed C&Cs IP addresses
License: http://osint.bambenekconsulting.com/license.txt

## DGA Domains

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: bambenek-dga-domains-collector
provider: Bambenek
feed: Bambenek DGA Domains
rate_limit: FIXME
http_url: http://osint.bambenekconsulting.com/feeds/dga-feed.txt
```

### Parser Bot

**Bot Name:** Bambenek DGA Domain Feed

**Bot Module:** intelmq.bots.parsers.bambenek.parser

**Configuration Parameters:**
```
id: bambenek-dga-domains-parser
```

**Notes:** Domain feed of known DGA domains from -2 to +3 days
License: http://osint.bambenekconsulting.com/license.txt


# Bitcash

**Status:** Unknown (newest data 2016-11-15)

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: bitcash-collector
provider: BitCash
feed: BitCash
rate_limit: FIXME
http_url: http://bitcash.cz/misc/log/blacklist
```

## Parser Bot

**Bot Name:** Bitcash Blocklist Feed

**Bot Module:** intelmq.bots.parsers.bitcash.parser

**Configuration Parameters:**
```
id: bitcash-parser
```

**Notes:** Blocklist provided by bitcash.cz of banned IPs for service abuse, this includes scanning, sniffing, harvesting, and dos attacks.

# Blocklist.de

## Apache

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: blocklistde-apache-collector
provider: Blocklist.de
feed: Blocklist.de Apache
rate_limit: 86400
http_url: https://lists.blocklist.de/lists/apache.txt
```

### Parser Bot

**Bot Name:** Blocklist.de

**Bot Module:** intelmq.bots.parsers.blocklistde.parser

**Configuration Parameters:**
```
id: blocklistde-apache-parser
```

**Notes:** Blocklist.DE Apache Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service Apache, Apache-DDOS, RFI-Attacks.

## Bots

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: blocklistde-bots-collector
provider: Blocklist.de
feed: Blocklist.de Bots
rate_limit: 86400
http_url: https://lists.blocklist.de/lists/bots.txt
```

### Parser Bot

**Bot Name:** Blocklist.de

**Bot Module:** intelmq.bots.parsers.blocklistde.parser

**Configuration Parameters:**
```
id: blocklistde-bots-parser
```

**Notes:** Blocklist.DE Bots Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks attacks on the RFI-Attacks, REG-Bots, IRC-Bots or BadBots (BadBots = he has posted a Spam-Comment on a open Forum or Wiki).

## Brute-force Logins

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: blocklistde-bruteforce-collector
provider: Blocklist.de
feed: Blocklist.de Brute-force Logins
rate_limit: 86400
http_url: https://lists.blocklist.de/lists/bruteforcelogin.txt
```

### Parser Bot

**Bot Name:** Blocklist.de

**Bot Module:** intelmq.bots.parsers.blocklistde.parser

**Configuration Parameters:**
```
id: blocklistde-bruteforce-parser
```

**Notes:** Blocklist.DE Brute-force Login Collector is the bot responsible to get the report from source of information. All IPs which attacks Joomlas, Wordpress and other Web-Logins with Brute-Force Logins.

## FTP

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: blocklistde-ftp-collector
provider: Blocklist.de
feed: Blocklist.de FTP
rate_limit: 86400
http_url: https://lists.blocklist.de/lists/ftp.txt
```

### Parser Bot

**Bot Name:** Blocklist.de

**Bot Module:** intelmq.bots.parsers.blocklistde.parser

**Configuration Parameters:**
```
id: blocklistde-ftp-parser
```

**Notes:** Blocklist.DE FTP Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours for attacks on the Service FTP.

## IMAP

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: blocklistde-imap-collector
provider: Blocklist.de
feed: Blocklist.de IMAP
rate_limit: 86400
http_url: https://lists.blocklist.de/lists/imap.txt
```

### Parser Bot

**Bot Name:** Blocklist.de

**Bot Module:** intelmq.bots.parsers.blocklistde.parser

**Configuration Parameters:**
```
id: blocklistde-imap-parser
```

**Notes:** Blocklist.DE IMAP Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours for attacks on the Service IMAP, SASL, POP3.....

## IRC Bots

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: blocklistde-irc-bots-collector
provider: Blocklist.de
feed: Blocklist.de IRC Bots
rate_limit: 86400
http_url: https://lists.blocklist.de/lists/ircbot.txt
```

### Parser Bot

**Bot Name:** Blocklist.de

**Bot Module:** intelmq.bots.parsers.blocklistde.parser

**Configuration Parameters:**
```
id: blocklistde-mail-parser
```

## Mail

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: blocklistde-mail-collector
provider: Blocklist.de
feed: Blocklist.de Mail
rate_limit: 86400
http_url: https://lists.blocklist.de/lists/mail.txt
```

### Parser Bot

**Bot Name:** Blocklist.de

**Bot Module:** intelmq.bots.parsers.blocklistde.parser

**Configuration Parameters:**
```
id: blocklistde-mail-parser
```

**Notes:** Blocklist.DE Mail Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service Mail, Postfix.

## SIP

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: blocklistde-sip-collector
provider: Blocklist.de
feed: Blocklist.de SIP
rate_limit: 86400
http_url: https://lists.blocklist.de/lists/sip.txt
```

### Parser Bot

**Bot Name:** Blocklist.de

**Bot Module:** intelmq.bots.parsers.blocklistde.parser

**Configuration Parameters:**
```
id: blocklistde-sip-parser
```

**Notes:** Blocklist.DE SIP Collector is the bot responsible to get the report from source of information. All IP addresses that tried to login in a SIP-, VOIP- or Asterisk-Server and are included in the IPs-List from http://www.infiltrated.net/ (Twitter).

## SSH

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: blocklistde-ssh-collector
provider: Blocklist.de
feed: Blocklist.de SSH
rate_limit: 86400
http_url: https://lists.blocklist.de/lists/ssh.txt
```

### Parser Bot

**Bot Name:** Blocklist.de

**Bot Module:** intelmq.bots.parsers.blocklistde.parser

**Configuration Parameters:**
```
id: blocklistde-ssh-parser
```

**Notes:** Blocklist.DE SSH Collector is the bot responsible to get the report from source of information. All IP addresses which have been reported within the last 48 hours as having run attacks on the service SSH.

## Strong IPs

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: blocklistde-strong-ips-collector
provider: Blocklist.de
feed: Blocklist.de Strong IPs
rate_limit: 86400
http_url: https://lists.blocklist.de/lists/strongips.txt
```

### Parser Bot

**Bot Name:** Blocklist.de

**Bot Module:** intelmq.bots.parsers.blocklistde.parser

**Configuration Parameters:**
```
id: blocklistde-strong-ips-parser
```

**Notes:** Blocklist.DE Strong IPs Collector is the bot responsible to get the report from source of information. All IPs which are older then 2 month and have more then 5.000 attacks.


# Blueliv Crimeserver

**Status:** Unknown

## Collector Bot

**Bot Name:** Blueliv Crimeserver

**Bot Module:** intelmq.bots.collectors.blueliv.collector_crimeserver

**Configuration Parameters:**
```
id: blueliv-crimeserver-collector
provider: Blueliv Crimeserver
feed: Blueliv Crimeserver
rate_limit: 3600
```

## Parser Bot

**Bot Name:** Blueliv Crimeserver

**Bot Module:** intelmq.bots.parsers.blueliv.parser_crimeserver

**Configuration Parameters:**
```
 id: blueliv-crimeserver-parser
```

**Notes:** Blueliv Crimeserver Collector is the bot responsible to get the report through the API.

# CI Army

**Status:** Active

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: ci-army-collector
provider: CINS Score
feed: CI Army
rate_limit: 3600
http_url: http://cinsscore.com/list/ci-badguys.txt
```

## Parser Bot

**Bot Name:** CI Army

**Bot Module:** intelmq.bots.parsers.ci_army.parser

**Configuration Parameters:**
```
id: ci-army-parser
```

# CleanMX

**Notes:** In order to download the CleanMX feed you need to use a custom user agent and
register that user agent.

## Phishing

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: cleanmx-phishing-collector
provider: CleanMX
feed: CleanMX Phishing
rate_limit: 129600
http_url: http://support.clean-mx.de/clean-mx/xmlphishing?response=alive&format=csv&domain=
http_user_agent: {{ your user agent }}
```

### Parser Bot

**Bot Name:** CleanMX Phishing

**Bot Module:** intelmq.bots.parsers.cleanmx.parser

**Configuration Parameters:**
```
 id: cleanmx-phishing-parser
```

## Virus

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: cleanmx-virus-collector
provider: CleanMX
feed: CleanMX Virus
rate_limit: 129600
http_url: http://support.clean-mx.de/clean-mx/xmlviruses?response=alive&format=csv&domain=
http_user_agent: {{ your user agent }}
```

### Parser Bot

**Bot Name:** CleanMX Virus

**Bot Module:** intelmq.bots.parsers.cleanmx.parser

**Configuration Parameters:**
```
id: cleanmx-virus-parser
```

# Cymru Full Bogons

**Status:** Active

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: cymru-full-bogons-collector
provider: Cymru
feed: Cymru Full Bogons
rate_limit: 129600
http_url: https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt
```

## Parser Bot

**Bot Name:** Cymru Full Bogons

**Bot Module:** intelmq.bots.parsers.cymru_full_bogons.parser

**Configuration Parameters:**
```
id: cymru-full-bogons-parser
```

# DShield

## AS

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: dshield-as-collector
provider: DShield
feed: DShield AS
rate_limit: 129600
http_url: https://dshield.org/asdetailsascii.html?as={{ AS Number }}
```

### Parser Bot

**Bot Name:** DShield AS

**Bot Module:** intelmq.bots.parsers.dshield.parser_asn

**Configuration Parameters:**
```
id: dshield-as-parser
```

## Block

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: dshield-block-collector
provider: DShield
feed: DShield Block
rate_limit: 129600
http_url: https://www.dshield.org/block.txt
```

### Parser Bot

**Bot Name:** DShield Block

**Bot Module:** intelmq.bots.parsers.dshield.parser_block

**Configuration Parameters:**
```
id: dshield-block-parser
```

## Suspicious Domains

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: dshield-suspicious-domains-collector
provider: DShield
feed: DShield Suspicious Domains
rate_limit: 129600
http_url: https://www.dshield.org/feeds/suspiciousdomains_High.txt
```

### Parser Bot

**Bot Name:** DShield Suspicious Domain

**Bot Module:** intelmq.bots.parsers.dshield.parser_domain

**Configuration Parameters:**
```
id: dshield-suspicious-domains-parser
```

# Danger Rulez

**Status:** Active

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: danger-rulez-collector
provider: Danger Rulez
feed: Danger Rulez Bruteforce Blocker
rate_limit: 3600
http_url: http://danger.rulez.sk/projects/bruteforceblocker/blist.php
```

## Parser Bot

**Bot Name:** Danger Rulez

**Bot Module:** intelmq.bots.parsers.danger_rulez.parser

**Configuration Parameters:**
```
id: danger-rulez-parser
```

# Dataplane

## SIP Invitation

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: dataplane-sip-invitation-collector
provider: Dataplane
feed: Dataplane SIP Invitation
rate_limit: 3600
http_url: http://dataplane.org/sipinvitation.txt
```

### Parser Bot

**Bot Name:** Dataplane Feeds

**Bot Module:** intelmq.bots.parsers.dataplane.parser

**Configuration Parameters:**
```
id: dataplane-sip-invitation-parser
```

**Notes:** Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP INVITE operation to a remote host.  The report lists hosts that are suspicious of more than just port scanning.  These hosts may be SIP client cataloging or conducting various forms of telephony abuse.  
Report is updated hourly.

## SIP Query

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: dataplane-sip-query-collector
provider: Dataplane
feed: Dataplane SIP Query
rate_limit: 3600
http_url: http://dataplane.org/sipquery.txt
```

### Parser Bot

**Bot Name:** Dataplane Feeds

**Bot Module:** intelmq.bots.parsers.dataplane.parser

**Configuration Parameters:**
```
 id: dataplane-sip-query-parser
```

**Notes:** Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP OPTIONS query to a remote host.  This report lists hosts that are suspicious of more than just port scanning.  The hosts may be SIP server cataloging or conducting various forms of telephony abuse.  
Report is updated hourly.

## SIP Registration

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: dataplane-sip-registration-collector
provider: Dataplane
feed: Dataplane SIP Registration
rate_limit: 3600
http_url: http://dataplane.org/sipregistration.txt
```

### Parser Bot

**Bot Name:** Dataplane Feeds

**Bot Module:** intelmq.bots.parsers.dataplane.parser

**Configuration Parameters:**
```
id: dataplane-sip-registration-parser
```

**Notes:** Entries consist of fields with identifying characteristics of a source IP address that has been seen initiating a SIP REGISTER operation to a remote host.  This report lists hosts that are suspicious of more than just port scanning.  The hosts may be SIP client cataloging or conducting various forms of telephony abuse.  
Report is updated hourly.

## SSH Client Connection

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: dataplane-ssh-client-collector
provider: Dataplane
feed: Dataplane SSH Client Connection
rate_limit: 3600
http_url: http://dataplane.org/sshclient.txt
```

### Parser Bot

**Bot Name:** Dataplane Feeds

**Bot Module:** intelmq.bots.parsers.dataplane.parser

**Configuration Parameters:**
```
id: dataplane-ssh-client-parser
```

**Notes:** Entries below consist of fields with identifying characteristics of a source IP address that has been seen initiating an SSH connection to a remote host.  This report lists hosts that are suspicious of more than just port scanning.  The hosts may be SSH server cataloging or conducting authentication attack attempts.  
Report is updated hourly.

## SSH Password Authentication

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: dataplane-ssh-password-collector
provider: Dataplane
feed: Dataplane SSH Password Authentication
rate_limit: 3600
http_url: http://dataplane.org/sshpwauth.txt
```

### Parser Bot

**Bot Name:** Dataplane Feeds

**Bot Module:** intelmq.bots.parsers.dataplane.parser

**Configuration Parameters:**
```
id: dataplane-ssh-password-parser
```

**Notes:** Entries below consist of fields with identifying characteristics of a source IP address that has been seen attempting to remotely login to a host using SSH password authentication.  The report lists hosts that are highly suspicious and are likely conducting malicious SSH password authentication attacks.
Report is updated hourly.


# DynDNS

**Status:** Active

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: dyndns-collector
provider: DynDNS
feed: DynDNS Infected Domains
rate_limit: 10800
http_url: http://security-research.dyndns.org/pub/malware-feeds/ponmocup-infected-domains-CIF-latest.txt
```

## Parser Bot

**Bot Name:** DynDNS ponmocup Domains

**Bot Module:** intelmq.bots.parsers.dyn.parser

**Configuration Parameters:**
```
id: dyndns-parser
```

**Notes:** DynDNS ponmocup. List of ponmocup malware redirection domains and infected web-servers. See also http://security-research.dyndns.org/pub/botnet-links.html

# Fraunhofer DGA

**Status:** Active

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: fraunhofer-dga-collector
provider: Fraunhofer
feed: Fraunhofer DGA
rate_limit: 10800
http_url: https://dgarchive.caad.fkie.fraunhofer.de/today
http_username: {{ your username}}
http_password: {{ your password }}
```

## Parser Bot

**Bot Name:** Fraunhofer DGA

**Bot Module:** intelmq.bots.parsers.fraunhofer.parser_dga

**Configuration Parameters:**
```
id: fraunhofer-dga-parser
```

**Notes:** Fraunhofer DGA collector fetches data from Fraunhofer's domain generation archive.

# HPHosts

**Status:** Unknown (last update 2016-12-21)

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: hphosts-collector
provider: HPHosts
feed: HPHosts
rate_limit: 3600
http_url: http://hosts-file.net/download/hosts.txt
```

## Parser Bot

**Bot Name:** HPHosts

**Bot Module:** intelmq.bots.parsers.hphosts.parser

**Configuration Parameters:**
```
id: hphosts-parser
```
error_log_message: false

# Malc0de

## Windows Format

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: malc0de-windows-format-collector
provider: Malc0de
feed: Malc0de Windows Format
rate_limit: 10800
http_url: https://malc0de.com/bl/BOOT
```

### Parser Bot

**Bot Name:** Malc0de

**Bot Module:** intelmq.bots.parsers.malc0de.parser

**Configuration Parameters:**
```
id: malc0de-windows-format-parser
```

**Notes:** This feed includes FQDN's of malicious hosts, the file format is in Windows Hosts file format.

## Bind Format

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: malc0de-bind-format-collector
provider: Malc0de
feed: Malc0de Bind Format
rate_limit: 10800
http_url: https://malc0de.com/bl/BOOT
```

### Parser Bot

**Bot Name:** Malc0de

**Bot Module:** intelmq.bots.parsers.malc0de.parser

**Configuration Parameters:**
```
id: malc0de-ip-blacklist-parser
```

**Notes:** This feed includes FQDN's of malicious hosts, the file format is in Bind format.

## IP Blacklist

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: malc0de-ip-blacklist-collector
provider: Malc0de
feed: Malc0de IP Blacklist
rate_limit: 10800
http_url: https://malc0de.com/bl/IP_Blacklist.txt
```

### Parser Bot

**Bot Name:** Malc0de IP Blacklist

**Bot Module:** intelmq.bots.parsers.malc0de.parser_ip_blacklist

**Configuration Parameters:**
```
id: malc0de-ip-blacklist-parser
```

**Notes:** This feed includes IP Addresses of malicious hosts.

# Malware Domain List

**Status:** Active

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: malware-domain-list-collector
provider: Malware Domain List
feed: Malware Domain List
rate_limit: 3600
http_url: http://www.malwaredomainlist.com/updatescsv.php
```

## Parser Bot

**Bot Name:** Malware Domain List

**Bot Module:** intelmq.bots.parsers.malwaredomainlist.parser

**Configuration Parameters:**
```
id: malware-domain-list-parser
```

# Malware Domains

**Status:** Active

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: malware-domains-collector
provider: Malware Domains
feed: Malware Domains
rate_limit: 172800
http_url: http://mirror2.malwaredomains.com/files/domains.txt
```

## Parser Bot

**Bot Name:** Malware Domains

**Bot Module:** intelmq.bots.parsers.malwaredomains.parser

**Configuration Parameters:**
```
id: malware-domains-parser
```

# MalwarePatrol Dans Guardian

**Status:** Unknown

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: malwarepatrol-dans-guardian-collector
provider: MalwarePatrol
feed: MalwarePatrol Dans Guardian
rate_limit: 180000
http_url: https://lists.malwarepatrol.net/cgi/getfile?receipt={{ API KEY }}&product=8&list=dansguardian
```

## Parser Bot

**Bot Name:** MalwarePatrol Dans Guardian

**Bot Module:** intelmq.bots.parsers.malwarepatrol.parser_dansguardian

**Configuration Parameters:**
```
 id: malwarepatrol-dans-guardian-parser
```

# N6

## Stomp

**Status:** Active

## Collector Bot

**Bot Name:** N6stomp

**Bot Module:** intelmq.bots.collectors.n6.collector_stomp

**Configuration Parameters:**
```
id: n6-collector
provider: CERT.pl
feed: CERT.pl N6 Stream
server: n6stream.cert.pl
port: 61614
exchange: {{ insert your exchange point as given by CERT.pl }}
ssl_ca_certificate: {{ insert path to CA file for CERT.pl's n6 }}
ssl_client_certificate: {{ insert path to client cert file for CERTpl's n6 }}
ssl_client_certificate_key: {{ insert path to client cert key file for CERT.pl's n6 }}
```

## Parser Bot

**Bot Name:** N6Stomp

**Bot Module:** intelmq.bots.parsers.n6.parser_n6stomp

**Configuration Parameters:**
```
id: n6-parser
```

**Notes:** N6 Collector - CERT.pl's N6 Collector - N6 feed via STOMP interface. Note that rate_limit does not apply for this bot as it is waiting for messages on a stream.

# Netlab 360

## DGA Feed

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: netlab360-dga-collector
provider: Netlab 360
feed: Netlab 360 DGA
rate_limit: FIXME
http_url: http://data.netlab.360.com/feeds/dga/dga.txt
```

### Parser Bot

**Bot Name:** Netlab 360 DGA

**Bot Module:** intelmq.bots.parsers.netlab_360.parser

**Configuration Parameters:**
```
id: netlab360-dga-parser
```

**Notes:** This feed lists DGA family, Domain, Start and end of valid time(UTC) of a number of DGA families.
reference: http://data.netlab.360.com/dga

## Magnitude EK Feed

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: netlab360-magnitude-ek-collector
provider: Netlab 360
feed: Netlab 360 Magnitude EK
rate_limit: FIXME
http_url: http://data.netlab.360.com/feeds/ek/magnitude.txt
```

### Parser Bot

**Bot Name:** Netlab 360 Magnitude

**Bot Module:** intelmq.bots.parsers.netlab_360.parser

**Configuration Parameters:**
```
id: netlab360-magnitude-ek-parser
```

**Notes:** This feed lists FQDN and possibly the URL used by Magnitude Exploit Kit.  Information also includes the IP address used for the domain and last time seen.
reference: http://data.netlab.360.com/ek


## Mirai Scanner Feed

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: netlab360-mirai-scanner-collector
provider: Netlab 360
feed: Netlab 360 Mirai Scanner List
rate_limit: 86400
http_url: http://data.netlab.360.com/feeds/mirai-scanner/scanner.list
```

### Parser Bot

**Bot Name:** Netlab 360 Mirai Scanner

**Bot Module:** intelmq.bots.parsers.netlab_360.parser

**Configuration Parameters:**
```
id: netlab360-mirai-scanner-parser
```

**Notes:** This feed provides IP addresses which actively scan for vulnerable IoT devices and install Mirai Botnet.
reference: http://data.netlab.360.com/mirai-scanner/


# Nothink

## DNS Attack Feed

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: nothink-dns-attack-collector
provider: Nothink
feed: Nothink DNS Attack
rate_limit: FIXME
http_url: http://www.nothink.org/honeypot_dns_attacks.txt
```

### Parser Bot

**Bot Name:** Nothink

**Bot Module:** intelmq.bots.parsers.nothink.parser

**Configuration Parameters:**
```
id: nothink-dns-attack-parser
```

**Notes:** This feed provides attack information for attack information against DNS honeypots.
reference: http://www.nothink.org/honeypot_dns.php

## SNMP Feed

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: nothink-snmp-collector
provider: Nothink
feed: Nothink SNMP
rate_limit: FIXME
http_url: http://www.nothink.org/blacklist/blacklist_snmp_day.txt
http_url: http://www.nothink.org/blacklist/blacklist_snmp_week.txt
http_url: http://www.nothink.org/blacklist/blacklist_snmp_year.txt
```

**Notes:** There are a number of feeds you can use to depend on how far back you would like to go.  The time.source will still be the date and time the feed was generated at nothink.


### Parser Bot

**Bot Name:** Nothink

**Bot Module:** intelmq.bots.parsers.nothink.parser

**Configuration Parameters:**
```
id: nothink-snmp-parser
```

**Notes:** This feed provides IP addresses of systems that have connected to a honeypot via SNMP in the last 24 hours.
reference: http://www.nothink.org/honeypot_snmp.php

## SSH Feed

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: nothink-ssh-collector
provider: Nothink
feed: Nothink DNS Attack
rate_limit: FIXME
http_url: http://www.nothink.org/blacklist/blacklist_ssh_day.txt
http_url: http://www.nothink.org/blacklist/blacklist_ssh_week.txt
http_url: http://www.nothink.org/blacklist/blacklist_ssh_year.txt
```

**Notes:** There are a number of feeds you can use to depend on how far back you would like to go.  The time.source will still be the date and time the feed was generated at nothink.


### Parser Bot

**Bot Name:** Nothink

**Bot Module:** intelmq.bots.parsers.nothink.parser

**Configuration Parameters:**
```
id: nothink-ssh-parser
```

**Notes:** This feed provides IP addresses of systems that have connected to a honeypot via SSH in the last 24 hours.
Reference: http://www.nothink.org/honeypots.php

## Telnet Feed

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: nothink-telnet-collector
provider: Nothink
feed: Nothink DNS Attack
rate_limit: FIXME
http_url: http://www.nothink.org/blacklist/blacklist_telnet_day.txt
http_url: http://www.nothink.org/blacklist/blacklist_telnet_week.txt
http_url: http://www.nothink.org/blacklist/blacklist_telnet_year.txt
```

**Notes:** There are a number of feeds you can use to depend on how far back you would like to go.  The time.source will still be the date and time the feed was generated at nothink.


### Parser Bot

**Bot Name:** Nothink

**Bot Module:** intelmq.bots.parsers.nothink.parser

**Configuration Parameters:**
```
id: nothink-telnet-parser
```

**Notes:** This feed provides IP addresses of systems that have connected to a honeypot via Telnet in the last 24 hours.
reference: http://www.nothink.org/honeypots.php


# OpenBL

**Status:** Active

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: openbl-collector
provider: OpenBL
feed: OpenBL
rate_limit: 43200
http_url: https://www.openbl.org/lists/date_all.txt
```

**Notes:** there is a list available [here](https://www.openbl.org/lists.html) with all blacklists available by the source which can be handled with the exact same bot, only `http_url` value needs to be specified.


## Parser Bot

**Bot Name:** OpenBL

**Bot Module:** intelmq.bots.parsers.openbl.parser

**Configuration Parameters:**
```
id: openbl-parser
```

# OpenPhish

**Status:** Unknown

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: openpish-collector
provider: OpenPhish
feed: OpenPhish
rate_limit: 86400
http_url: https://www.openphish.com/feed.txt
```

## Parser Bot

**Bot Name:** OpenPhish

**Bot Module:** intelmq.bots.parsers.openphish.parser

**Configuration Parameters:**
```
id: openpish-parser
```

# PhishTank

**Status:** Unknown

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: phishtank-collector
provider: PhishTank
feed: PhishTank
rate_limit: 28800
http_url: https://data.phishtank.com/data/{{ your API key }}/online-valid.csv
```

## Parser Bot

**Bot Name:** PhishTank

**Bot Module:** intelmq.bots.parsers.phishtank.parser

**Configuration Parameters:**
```
id: phishtank-parser
```

# Proxyspy

**Status:** Active

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: proxyspy-collector
provider: ProxySpy
feed: ProxySpy
rate_limit: FIXME
http_url: http://txt.proxyspy.net/proxy.txt
```

## Parser Bot

**Bot Name:** Proxyspy

**Bot Module:** intelmq.bots.parsers.proxyspy.parser

**Configuration Parameters:**
```
id: proxyspy-parser
```

**Notes:** This feed provides IP addresses, ports and country codes for available proxies.  Feed is updated hourly.


# Shadowserver

**Status:** Active

## Collector Bot

**Bot Name:** Generic Mail URL Fetcher

**Bot Module:** intelmq.bots.collectors.mail.collector_mail_url

**Configuration Parameters:**
```
id: shadowserver-<report_type>-collector
provider: ShadowServer
feed: ShadowServer <report_type>
rate_limit: FIXME
subject_regex: (see individual reports below)
url_regex: https://dl.shadowserver.org/[^ ]+
```

## Collector Bot

**Bot Name:** Generic Mail Attachment Fetcher

**Bot Module:** intelmq.bots.collectors.mail.collector_mail_attach

**Configuration Parameters:**
```
id: shadowserver-<report_type>-collector
provider: ShadowServer
feed: ShadowServer <report_type>
rate_limit: FIXME
subject_regex: (see individual reports below)
attach_regex: csv.zip
attach_unzip: true
```

## Parser Bot

**Bot Name:** Shadowserver

**Bot Module:** intelmq.bots.parsers.shadowserver.parser

**Configuration Parameters:**
```
id: shadowserver-<report_type>-parser
```

**Notes:** Shadowserver sends out a variety of reports (see https://www.shadowserver.org/wiki/pmwiki.php/Services/Reports). The reports can be retrieved from the URL in the mail or from the attachment. These are some examples of the subjects of the mails:

 - Shadowserver [^ ]+ Chargen Report
 - Shadowserver [^ ]+ Drone Report
 - Shadowserver [^ ]+ Microsoft Sinkhole Report
 - Shadowserver [^ ]+ QOTD Report
 - Shadowserver [^ ]+ SNMP Report


# Spamhaus

## CERT

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: spamhaus-cert-collector
provider: Spamhaus
feed: Spamhaus CERT
rate_limit: 3600
http_url: {{ your CERT portal URL }}
```

### Parser Bot

**Bot Name:** Spamhaus CERT

**Bot Module:** intelmq.bots.parsers.spamhaus.parser_cert

**Configuration Parameters:**
```
id: spamhaus-cert-parser
```

**Notes:** Spamhaus CERT Insight Portal. Access limited to CERTs and CSIRTs with national or regional responsibility. https://www.spamhaus.org/news/article/705/spamhaus-launches-cert-insight-portal

## Drop

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: spamhaus-drop-collector
provider: Spamhaus
feed: Spamhaus Drop
rate_limit: 3600
http_url: https://www.spamhaus.org/drop/drop.txt
```

### Parser Bot

**Bot Name:** Spamhaus Drop

**Bot Module:** intelmq.bots.parsers.spamhaus.parser_drop

**Configuration Parameters:**
```
id: spamhaus-drop-parser
```

**Notes:** The DROP list will not include any IP address space under the control of any legitimate network - even if being used by "the spammers from hell". DROP will only include netblocks allocated directly by an established Regional Internet Registry (RIR) or National Internet Registry (NIR) such as ARIN, RIPE, AFRINIC, APNIC, LACNIC or KRNIC or direct RIR allocations.

## EDrop

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: spamhaus-edrop-collector
provider: Spamhaus
feed: Spamhaus EDrop
rate_limit: 3600
http_url: https://www.spamhaus.org/drop/edrop.txt
```

### Parser Bot

**Bot Name:** Spamhaus Drop

**Bot Module:** intelmq.bots.parsers.spamhaus.parser_drop

**Configuration Parameters:**
```
id: spamhaus-edrop-parser
```

**Notes:** EDROP is an extension of the DROP list that includes sub-allocated netblocks controlled by spammers or cyber criminals. EDROP is meant to be used in addition to the direct allocations on the DROP list.

## Dropv6

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: spamhaus-dropv6-collector
provider: Spamhaus
feed: Spamhaus Drop v6
rate_limit: 3600
http_url: https://www.spamhaus.org/drop/dropv6.txt
```

### Parser Bot

**Bot Name:** Spamhaus Drop

**Bot Module:** intelmq.bots.parsers.spamhaus.parser_drop

**Configuration Parameters:**
```
id: spamhaus-dropv6-parser
```

**Notes:** The DROPv6 list includes IPv6 ranges allocated to spammers or cyber criminals. DROPv6 will only include IPv6 netblocks allocated directly by an established Regional Internet Registry (RIR) or National Internet Registry (NIR) such as ARIN, RIPE, AFRINIC, APNIC, LACNIC or KRNIC or direct RIR allocations.

## ASN-Drop

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: spamhaus-asn-drop-collector
provider: Spamhaus
feed: Spamhaus ASN Drop
rate_limit: 3600
http_url: https://www.spamhaus.org/drop/asndrop.txt
```

### Parser Bot

**Bot Name:** Spamhaus Drop

**Bot Module:** intelmq.bots.parsers.spamhaus.parser_drop

**Configuration Parameters:**
```
id: spamhaus-asn-drop-parser
```

**Notes:** ASN-DROP contains a list of Autonomous System Numbers controlled by spammers or cyber criminals, as well as "hijacked" ASNs. ASN-DROP can be used to filter BGP routes which are being used for malicious purposes.


# Taichung

**Status:** Active

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: taichung-collector
provider: Taichung
feed: Taichung
rate_limit: 3600
http_url: https://www.tc.edu.tw/net/netflow/lkout/recent/30
```

## Parser Bot

**Bot Name:** Taichung

**Bot Module:** intelmq.bots.parsers.taichung.parser

**Configuration Parameters:**
```
id: taichung-parser
```
error_log_message: false

# Turris Greylist

**Status:** Active

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: turris-greylist-collector
provider: Turris
feed: Turris Greylist
rate_limit: 43200
http_url: https://www.turris.cz/greylist-data/greylist-latest.csv
```

## Parser Bot

**Bot Name:** Turris Greylist

**Bot Module:** intelmq.bots.parsers.turris.parser

**Configuration Parameters:**
```
id: turris-greylist-parser
```

# URLVir

## Hosts

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: urlvir-hosts-collector
provider: URLVir
feed: URLVir Hosts
rate_limit: 129600
http_url: http://www.urlvir.com/export-hosts/
```

### Parser Bot

**Bot Name:** URLVir Hosts

**Bot Module:** intelmq.bots.parsers.urlvir.parser

**Configuration Parameters:**
```
id: urlvir-hosts-parser
```

**Notes:** This feed provides FQDN's or IP addresses for Active Malicious Hosts.

## IPs

**Status:** Active

### Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: urlvir-ips-collector
provider: URLVir
feed: URLVir IPs
rate_limit: 129600
http_url: http://www.urlvir.com/export-ip-addresses/
```

### Parser Bot

**Bot Name:** URLVir IPs

**Bot Module:** intelmq.bots.parsers.urlvir.parser

**Configuration Parameters:**
```
id: urlvir-ips-parser
```

**Notes:** This feed provides IP addresses hosting Malware.


# VXVault

**Status:** Active

## Collector Bot

**Bot Name:** Generic URL Fetcher

**Bot Module:** intelmq.bots.collectors.http.collector_http

**Configuration Parameters:**
```
id: vxvault-collector
provider: VXVault
feed: VXVault
rate_limit: 3600
http_url: http://vxvault.net/URL_List.php
```

## Parser Bot

**Bot Name:** VXVault

**Bot Module:** intelmq.bots.parsers.vxvault.parser

**Configuration Parameters:**
```
id: vxvault-parser
```

