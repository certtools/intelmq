<!-- comment
   SPDX-FileCopyrightText: 2015-2021 nic.at GmbH, 2023 Filip Pokorný, 2025 Institute for Common Good Technology
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Adding Feeds

Adding a feed doesn't necessarily require any programming experience. There are several collector and parser bots intended for general use. Depending on the data source you are trying to add as a feed, it might be only a matter of creating a working combination of collector bot (such as URL Fetcher) configuration and a parser bot (such as CSV parser) configuration. When you are satisfied with the configurations, add it to the `intelmq/etc/feeds.yaml` file using the following template and open a [pull request](https://github.com/certtools/intelmq/pulls)!

```yaml
<NAME OF THE FEED PROVIDER>:
    <NAME OF THE FEED>:
      description: <DESCRIPTION OF WHAT KIND OF DATA THE FEED PROVIDES>
      additional_information: <ANY ADDITIONAL INFORMATION>
      documentation: <FEED HOMEPAGE/DOCUMENTATION URL>
      revision: <DATE WHEN YOU ADDED THIS FEED>
      public: <TRUE/FALSE IF THE DATA SOURCE IS PUBLICLY AVAILABLE>
      bots:
        collector:
          module: <MODULE USED FOR THE COLLECTOR BOT>
          parameters:
            name: __FEED__ # KEEP AS IT IS
            provider: __PROVIDER__  # KEEP AS IT IS
            <ADDITIONAL COLLECTOR BOT PARAMETERS>
        parser:
          module: <MODULE USED FOR THE PARSER BOT>
          parameters:
            <ADDITIONAL PARSER BOT PARAMETERS>
```

If the data source utilizes some unusual way of distribution or uses a custom format for the data it might be necessary to develop specialized bot(s) for this particular data source. Always try to use existing bots before you start developing your own. Please also consider extending an existing bot if your use-case is close enough to it's features. If you are unsure which way to take, start an [issue](https://github.com/certtools/intelmq/issues) and you will receive guidance.

## Howto

### Choosing the collector

### Choosing the parser

### Classification

### Other static fields

* Feed accuracy
* TLP
* Event Description
	* Target
	* Text
	* URL
* Protocol
	* Application Protocol
	* Transport Protocol

## Example Feeds

### Simple List

As an example, let's add the - very simple - feed *Toxic IP Addresses (CIDR)* by StopForumSpam to the documentation. The data URL is https://www.stopforumspam.com/downloads/toxic_ip_cidr.txt and contains a list of IP Network Ranges in CIDR notation, separated by newlines.

As the resource is available via HTTP, we will use the [HTTP Collector](../user/bots.md#intelmq.bots.collectors.http.collector_http) for the data retrieval and [Generic CSV Parser](../user/bots.md#intelmq.bots.parsers.generic.parser_csv) for parsing.
For the collector, we only specify the module to use (the HTTP collector, as seen on the bots documentation), an estimate on the feed accuracy (as it is a blacklist, not 100%, but still reasonably high), the resource URL to download and the rate limit of 1 hour, as there might be frequent updates.

For the parser we again specify the module name and the required parameter (columns) to map the input data field to the IntelMQ field `source.network`. Further we add some static field values which are equal for all data lines.

```
Stop Forum Spam:
    Toxic IP Addresses:
      description: IP Networks that are believed will only ever be used for abuse
      documentation: https://www.stopforumspam.com/downloads
      revision: 2025-09-21
      public: true
      bots:
        collector:
          module: intelmq.bots.collectors.http.collector_http
          parameters:
            accuracy: 80
            http_url: https://www.stopforumspam.com/downloads/toxic_ip_cidr.txt
            rate_limit: 86400
        parser:
          module: intelmq.bots.parsers.generic.parser_csv
          parameters:
            columns: source.network
            default_fields:
              classification.type: blacklist
              protocol.application: http
              protocol.transport: tcp
              event_description.target: web forums
              event_description.text: web forum spam
              event_description.url: https://www.stopforumspam.com/
              tlp: white
```

### TSV document

As a next example, let's add a feed for https://hole.cert.pl/domains/v2/domains.csv (7 MB).
Contrary to its file name ending, the separator is not a comma, but a tab character.
The file contains four columns:
```
PozycjaRejestru AdresDomeny     DataWpisu       DataWykreslenia
285107  0-1-x.06215785.xyz      2025-04-02T09:02:19+00:00       
332655	d15k2d11r6t6rl.cloudfront.net	2025-06-12T17:06:08+00:00	2025-06-13T13:54:55+00:00
[...]
```

The feeds description is at https://cert.pl/en/warning-list/ and it says the list of blocked domains is updated about every 5 minutes. In IntelMQ we usually don't need such high refresh rates, but setting it to half an hour is reasonable for most use cases.
The list is automatically composed, and the list contains domains for warnings so the accuracy is lower.
As the descriptions says the listed domains are websites, we can again assume the protocol is HTTP/TCP. Although the list is about phishing websites, it's use case is a warning/blacklist and therefore the classification is blacklist. In the event description we explain the kind of blacklist.
The most crucial part is the mapping of da columns to IntelMQ fields. In this case, they are given in Polish.
- `PozycjaRejestru`: Position in the Register. We do not need this in IntelMQ, so we save it as `extra.certpl_register`
- `AdresDomeny`: The domain address, lands in `source.fqdn`. This is the information we case about
- `DataWpisu`: The date of entry, and
- `DataWykreslenia`: The date of deletion
	- This is a tricky situation we as have no clear indication at which time the information is current. Based on the feed description, if the deletion date would is not present, the time of fetching the data (`time.observation`) is closest to the meaning of `time.source`.
	- Therefore, instead of using the Generic CSV Parser, a custom Parser or a downstream expert is required to accomplish this.
	- For simplicity, we map these columns to `extra.first_seen` and `extra.expiration_date`. Both fields are already in use by other bots and feeds.

```yaml
CERT.PL
    Hole Domains v2:
      description: Dangerous websites Warning List
      documentation: https://cert.pl/en/warning-list/
      revision: 2025-09-23
      public: true
      bots:
        collector:
          module: intelmq.bots.collectors.http.collector_http
          parameters:
            accuracy: 50
            rate_limit: 1800
            http_url: https://hole.cert.pl/domains/v2/domains.csv
        parser:
          module: intelmq.bots.parsers.generic.parser_csv
          parameters:
            columns: extra.certpl_register,source.fqdn,extra.first_seen,extra.expiration_date
            default_fields:
              classification.type: blacklist
              protocol.application: http
              protocol.transport: tcp
              event_description.target: users
              event_description.text: phishing
              event_description.url: https://cert.pl/en/warning-list/
              tlp: white
```

## Feeds Wishlist

This is a list with potentially interesting data sources, which are either currently not supported or the usage is not clearly documented in IntelMQ. If you want to **contribute** new feeds to IntelMQ, this is a great place to start!

!!! note
    Some of the following data sources might also serve as an expert bot for enriching processed events.

- Lists of feeds:
    - [threatfeeds.io](https://threatfeeds.io)
    - [TheCyberThreat](http://thecyberthreat.com/cyber-threat-intelligence-feeds/)
    - [sbilly: Awesome Security](https://github.com/sbilly/awesome-security#threat-intelligence)
    - [pannoniait:Backlists](https://doku.pannoniait.at/doku.php?id=know-how:blacklists)
    - [hslatman:awesome-threat-intelligence](https://github.com/hslatman/awesome-threat-intelligence)
    - [Zeek Intelligence Feeds](https://github.com/CriticalPathSecurity/Zeek-Intelligence-Feeds)
    - [imuledx OSING feeds](https://github.com/imuledx/OSINT_sources)
- Some third party intelmq bots: [NRDCS IntelMQ fork](https://github.com/NRDCS/intelmq/tree/certlt/intelmq/bots)
- List of potentially interesting data sources:
    - [Abuse.ch SSL Blacklists](https://sslbl.abuse.ch/blacklist/)
    - [aa419 Fake Banks List](https://db.aa419.org/fakebankslist.php)
    - [AbuseIPDB](https://www.abuseipdb.com/pricing)
    - [Adblock Plus](https://adblockplus.org/en/subscriptions)
    - [apivoid IP Reputation API](https://www.apivoid.com/api/ip-reputation/)
    - [Anomali Limo Free Intel Feed](https://www.anomali.com/resources/limo)
    - [APWG's ecrimex](https://www.ecrimex.net)
    - [Avast Threat Intel IoCs of dark matter repository](https://github.com/avast/ioc)
    - [Berkeley](https://security.berkeley.edu/aggressive_ips/ips)
    - [Binary Defense](https://www.binarydefense.com/)
    - [Bot Invaders Realtime tracker](http://www.marc-blanchard.com/BotInvaders/index.php)
    - [Botherder Targetedthreats](https://github.com/botherder/targetedthreats/)
    - [Botscout Last Caught](http://botscout.com/last_caught_cache.htm)
    - [botvrij](https://www.botvrij.eu/)
    - [Carbon Black Feeds](https://github.com/carbonblack/cbfeeds)
    - [CERT.pl Phishing Warning List](http://hole.cert.pl/domains/)
    - [Chaos Reigns](http://www.chaosreigns.com/spam/)
    - [Critical Stack](https://intel.criticalstack.com)
    - [Cruzit](http://www.cruzit.com/xwbl2txt.php)
    - [Cyber Crime Tracker](http://cybercrime-tracker.net/all.php)
    - [drb-ra C2IntelFeeds](https://github.com/drb-ra/C2IntelFeeds)
    - [DNS DB API](https://api.dnsdb.info)
    - [ESET Malware Indicators of Compromise](https://github.com/eset/malware-ioc)
    - [Facebook Threat Exchange](https://developers.facebook.com/docs/threat-exchange)
    - [FilterLists](https://filterlists.com)
    - [Firehol IPLists](https://iplists.firehol.org/)
    - [Google Webmaster Alerts](https://www.google.com/webmasters/)
    - [GPF Comics DNS Blacklist](https://www.gpf-comics.com/dnsbl/export.php)
    - [Greensnow](https://blocklist.greensnow.co/greensnow.txt)
    - [Greynoise](https://docs.greynoise.io/docs/using-the-greynoise-community-api)
    - [HP Feeds](https://github.com/rep/hpfeeds)
    - [IBM X-Force Exchange](https://exchange.xforce.ibmcloud.com/)
    - [ImproWare AntiSpam](https://antispam.imp.ch/)
    - [ISightPartners](http://www.isightpartners.com/)
    - [James Brine](https://jamesbrine.com.au/)
    - [Joewein](http://www.joewein.net)
    - Maltrail:
        - [Malware](https://github.com/stamparm/maltrail/tree/master/trails/static/malware)
        - [Suspicious](https://github.com/stamparm/maltrail/tree/master/trails/static/suspicious)
        - [Malicious](https://github.com/stamparm/maltrail/tree/master/trails/static/malicious)
        - [Mass Scanners](https://github.com/stamparm/maltrail/blob/master/trails/static/mass_scanner.txt)
          (for whitelisting)
    - [Malshare](https://malshare.com/)
    - [MalSilo Malware URLs](https://malsilo.gitlab.io/feeds/dumps/url_list.txt)
    - [Malware Config](http://malwareconfig.com)
    - [Malware DB (cert.pl)](https://mwdb.cert.pl/)
    - [MalwareInt](http://malwareint.com)
    - [Malware Must Die](https://malwared.malwaremustdie.org/rss.php)
    - [Manity Spam IP addresses](http://www.dnsbl.manitu.net/download/nixspam-ip.dump.gz)
    - [Marc Blanchard DGA Domains](http://www.marc-blanchard.com/BotInvaders/index.php)
    - [MaxMind Proxies](https://www.maxmind.com/en/anonymous_proxies)
    - [mIRC Servers](http://www.mirc.com/servers.ini)
    - [MISP Warning Lists](https://github.com/MISP/misp-warninglists)
    - [Monzymerza](https://github.com/monzymerza/parthenon)
    - [Multiproxy](http://multiproxy.org/txt_all/proxy.txt)
    - [Neo23x0 signature-base](https://github.com/Neo23x0/signature-base/tree/master/iocs)
    - [OpenBugBounty](https://www.openbugbounty.org/)
    - [Phishing Army](https://phishing.army/)
    - [Phishstats](https://phishstats.info/) (offers JSON API and CSV download)
    - [Project Honeypot (#284)](http://www.projecthoneypot.org/list_of_ips.php?rss=1)
    - [RST Threat Feed](https://rstcloud.net/) (offers a free and a commercial feed)
    - [SANS ISC](https://isc.sans.edu/api/)
    - [ShadowServer Sandbox API](http://www.shadowserver.org/wiki/pmwiki.php/Services/Sandboxapi)
    - [Shodan search API](https://shodan.readthedocs.io/en/latest/tutorial.html#searching-shodan)
    - [Snort](https://www.snort.org/downloads/ip-block-list)
    - [stopforumspam Toxic IP addresses and domains](https://www.stopforumspam.com/downloads)
    - [Spamhaus Botnet Controller List](https://www.spamhaus.org/bcl/)
    - [SteveBlack Hosts File](https://github.com/StevenBlack/hosts)
    - [The Haleys](http://charles.the-haleys.org/ssh_dico_attack_hdeny_format.php/hostsdeny.txt)
    - [Threat Crowd](https://www.threatcrowd.org/feeds/hashes.txt)
    - [Threat Grid](http://www.threatgrid.com/)
    - [Threatstream](https://ui.threatstream.com/)
    - [TotalHash](http://totalhash.com)
    - [UCE Protect](http://wget-mirrors.uceprotect.net/)
    - [Unit 42 Public Report IOCs](https://github.com/pan-unit42/iocs)
    - [URI BL](http://rss.uribl.com/index.shtml)
    - [urlscan.io](https://urlscan.io/products/phishingfeed/)
    - [Virustotal](https://www.virustotal.com/gui/home/search)
    - [virustream](https://github.com/ntddk/virustream)
    - [VoIP Blacklist](http://www.voipbl.org/update/)
    - [YourCMC](http://vmx.yourcmc.ru/BAD_HOSTS.IP4)
