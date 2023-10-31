<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
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

## Feeds Wishlist

This is a list with potentially interesting data sources, which are either currently not supported or the usage is not clearly documented in IntelMQ. If you want to **contribute** new feeds to IntelMQ, this is a great place to start!

!!! note
    Some of the following data sources might better serve as an expert bot for enriching processed events.

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
    - [Greynoise](https://developer.greynoise.io/reference/community-api)
    - [HP Feeds](https://github.com/rep/hpfeeds)
    - [IBM X-Force Exchange](https://exchange.xforce.ibmcloud.com/)
    - [ImproWare AntiSpam](https://antispam.imp.ch/)
    - [ISightPartners](http://www.isightpartners.com/)
    - [James Brine](https://jamesbrine.com.au/)
    - [Joewein](http://www.joewein.net)
    - Maltrail:
        - [Malware](https://github.com/stamparm/maltrail/tree/master/trails/static/images/malware)
        - [Suspicious](https://github.com/stamparm/maltrail/tree/master/trails/static/images/suspicious)
        - [Mass Scanners](https://github.com/stamparm/maltrail/blob/master/trails/static/images/mass_scanner.txt)
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
    - [Snort](http://labs.snort.org/feeds/ip-filter.blf)
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
