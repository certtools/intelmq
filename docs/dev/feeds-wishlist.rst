..
   SPDX-FileCopyrightText: 2020 Sebastian Wagner <wagner@cert.at>
   SPDX-License-Identifier: AGPL-3.0-or-later

###############
Feeds wishlist
###############

This is a list with various feeds, which are either currently not supported or the usage is not clearly documented in IntelMQ.

If you want to **contribute** documenting how to configure existing bots in order to collect new feeds or by creating new parsers, here is a list of potentially interesting feeds.
See :ref:`feeds documentation` for more information on this.

This list evolved from the issue :issue:`Contribute: Feeds List (#384) <384>`.

- Lists of feeds:

  - `threatfeeds.io <https://threatfeeds.io>`_
  - `TheCyberThreat <http://thecyberthreat.com/cyber-threat-intelligence-feeds/>`_
  - `sbilly: Awesome Security <https://github.com/sbilly/awesome-security#threat-intelligence>`_
  - `pannoniait: Backlists <https://doku.pannoniait.at/doku.php?id=know-how:blacklists>`_
  - `hslatman: awesome-threat-intelligence <https://github.com/hslatman/awesome-threat-intelligence>`_
  - `Zeek Intelligence Feeds <https://github.com/CriticalPathSecurity/Zeek-Intelligence-Feeds>`_
  - `imuledx OSING feeds <https://github.com/imuledx/OSINT_sources>`_

- Some third party intelmq bots: `NRDCS' IntelMQ fork <https://github.com/NRDCS/intelmq/tree/certlt/intelmq/bots>`_

- List of potentially interesting data sources:

  - `Abuse.ch SSL Blacklists <https://sslbl.abuse.ch/blacklist/>`_
  - `AbuseIPDB <https://www.abuseipdb.com/pricing>`_
  - `Adblock Plus <https://adblockplus.org/en/subscriptions>`_
  - `apivoid IP Reputation API <https://www.apivoid.com/api/ip-reputation/>`_
  - `Anomali Limo Free Intel Feed <https://www.anomali.com/resources/limo>`_
  - `APWG's ecrimex <https://www.ecrimex.net>`_
  - `Berkeley <https://security.berkeley.edu/aggressive_ips/ips>`_
  - `Binary Defense <https://www.binarydefense.com/>`_
  - `Bot Invaders Realtime tracker <http://www.marc-blanchard.com/BotInvaders/index.php>`_
  - `Botherder Targetedthreats <https://github.com/botherder/targetedthreats/>`_
  - `Botscout Last Caught <http://botscout.com/last_caught_cache.htm>`_
  - `botvrij <https://www.botvrij.eu/>`_
  - `Carbon Black Feeds <https://github.com/carbonblack/cbfeeds>`_
  - `CERT.pl Phishing Warning List <http://hole.cert.pl/domains/>`_
  - `Chaos Reigns <http://www.chaosreigns.com/spam/>`_
  - `Critical Stack <https://intel.criticalstack.com>`_
  - `Cruzit <http://www.cruzit.com/xwbl2txt.php>`_
  - `Cyber Crime Tracker <http://cybercrime-tracker.net/all.php>`_
  - `drb-ra C2IntelFeeds <https://github.com/drb-ra/C2IntelFeeds>`_
  - `DNS DB API <https://api.dnsdb.info>`_
  - `ESET Malware Indicators of Compromise <https://github.com/eset/malware-ioc>`_
  - `Facebook Threat Exchange <https://developers.facebook.com/docs/threat-exchange>`_
  - `FilterLists <https://filterlists.com>`_
  - `Firehol IPLists <https://iplists.firehol.org/>`_
  - `Google Webmaster Alerts <https://www.google.com/webmasters/>`_
  - `GPF Comics DNS Blacklist <https://www.gpf-comics.com/dnsbl/export.php>`_
  - `Greensnow <https://blocklist.greensnow.co/greensnow.txt>`_
  - `Greynoise <https://developer.greynoise.io/reference/community-api>`_
  - `HP Feeds <https://github.com/rep/hpfeeds>`_
  - `IBM X-Force Exchange <https://exchange.xforce.ibmcloud.com/>`_
  - `ImproWare AntiSpam <https://antispam.imp.ch/>`_
  - `ISightPartners <http://www.isightpartners.com/>`_
  - `James Brine <https://jamesbrine.com.au/>`_
  - `Joewein <http://www.joewein.net>`_
  - Maltrail:

    - `Malware <https://github.com/stamparm/maltrail/tree/master/trails/static/malware>`_
    - `Suspicious <https://github.com/stamparm/maltrail/tree/master/trails/static/suspicious>`_
    - `Mass Scanners <https://github.com/stamparm/maltrail/blob/master/trails/static/mass_scanner.txt>`_ (for whitelisting)
  - `Malshare <https://malshare.com/>`_
  - `MalSilo Malware URLs <https://malsilo.gitlab.io/feeds/dumps/url_list.txt>`_
  - `Malware Config <http://malwareconfig.com>`_
  - `Malware DB (cert.pl) <https://mwdb.cert.pl/>`_
  - `MalwareInt <http://malwareint.com>`_
  - `Malware Must Die <https://malwared.malwaremustdie.org/rss.php>`_
  - `Manity Spam IP addresses <http://www.dnsbl.manitu.net/download/nixspam-ip.dump.gz>`_
  - `Marc Blanchard DGA Domains <http://www.marc-blanchard.com/BotInvaders/index.php>`_
  - `MaxMind Proxies <https://www.maxmind.com/en/anonymous_proxies>`_
  - `mIRC Servers <http://www.mirc.com/servers.ini>`_
  - `Monzymerza <https://github.com/monzymerza/parthenon>`_
  - `Multiproxy <http://multiproxy.org/txt_all/proxy.txt>`_
  - `Neo23x0 signature-base <https://github.com/Neo23x0/signature-base/tree/master/iocs>`_
  - `OpenBugBounty <https://www.openbugbounty.org/>`_
  - `Phishing Army <https://phishing.army/>`_
  - `Phishstats <https://phishstats.info/>`_, offers JSON ("API) and CSV download.
  - `Project Honeypot (#284) <http://www.projecthoneypot.org/list_of_ips.php?rss=1>`_
  - `RST Threat Feed <https://rstcloud.net/>`_ (offers a free and a commercial feed)
  - `SANS ISC <https://isc.sans.edu/api/>`_
  - `ShadowServer Sandbox API <http://www.shadowserver.org/wiki/pmwiki.php/Services/Sandboxapi>`_
  - `Shodan search API <https://shodan.readthedocs.io/en/latest/tutorial.html#searching-shodan>`_
  - `Snort <http://labs.snort.org/feeds/ip-filter.blf>`_
  - `stopforumspam Toxic IP addresses and domains <https://www.stopforumspam.com/downloads>`_
  - `Spamhaus Botnet Controller List <https://www.spamhaus.org/bcl/>`_
  - `SteveBlack Hosts File <https://github.com/StevenBlack/hosts>`_
  - `The Haleys <http://charles.the-haleys.org/ssh_dico_attack_hdeny_format.php/hostsdeny.txt>`_
  - `Threat Crowd <https://www.threatcrowd.org/feeds/hashes.txt>`_
  - `Threat Grid <http://www.threatgrid.com/>`_
  - `Threatstream <https://ui.threatstream.com/>`_
  - `TOR Project Exit addresses <https://check.torproject.org/exit-addresses>`_
  - `TotalHash <http://totalhash.com>`_
  - `UCE Protect <http://wget-mirrors.uceprotect.net/>`_
  - `Unit 42 Public Report IOCs <https://github.com/pan-unit42/iocs>`_
  - `URI BL <http://rss.uribl.com/index.shtml>`_
  - `urlscan.io <https://urlscan.io/products/phishingfeed/>`_
  - `Virustotal <https://www.virustotal.com/gui/home/search>`_
  - `virustream <https://github.com/ntddk/virustream>`_
  - `VoIP Blacklist <http://www.voipbl.org/update/>`_
  - `YourCMC <http://vmx.yourcmc.ru/BAD_HOSTS.IP4>`_
