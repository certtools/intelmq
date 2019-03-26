## Table of Contents

**Table of Contents:**
- [Overview](#overview)
- [Rules for keys](#rules-for-keys)
- [Sections](#sections)
- [Feed](#feed)
- [Time](#time)
- [Source Identity](#source-identity)
  - [Source Geolocation Identity](#source-geolocation-identity)
  - [Source Local Identity](#source-local-identity)
- [Destination Identity](#destination-identity)
  - [Destination Geolocation Identity](#destination-geolocation-identity)
  - [Destination Local Identity](#destination-local-identity)
- [Extra values](#extra-values)
- [Fields List and data types](#fields-list-and-data-types)
- [Classification](#classification)
- [Minimum recommended requirements for events](#minimum-recommended-requirements-for-events)


## Overview

All messages (reports and events) are Python/JSON dictionaries. The key names and according types are defined by the so called *harmonization*.

The purpose of this document is to list and clearly define known **fields** in Abusehelper as well as IntelMQ or similar systems. A field is a ```key=value``` pair. For a clear and unique definition of a field, we must define the **key** (field-name) as well as the possible **values**. A field belongs to an **event**. An event is basically a  structured log record in the form ```key=value, key=value, key=value, …```. In the [List of known fields](#fields), each field is grouped by a **section**. We describe these sections briefly below.
Every event **MUST** contain a timestamp field.

[IOC](https://en.wikipedia.org/wiki/Indicator_of_compromise) (Indicator of compromise) is a single observation like a log line.

## Rules for keys

The keys can be grouped together in sub-fields, e.g. `source.ip` or `source.geolocation.latitude`. Thus, keys must match `^[a-z_](.[a-z0-9_]+)*$`.


## Sections

As stated above, every field is organized under some section. The following is a description of the sections and what they imply.

### Feed

Fields listed under this grouping list details about the source feed where information came from.

### Time

The time section lists all fields related to time information.
This document requires that all the timestamps MUST be normalized to UTC. If the source reports only a date, do not attempt to invent timestamps.

### Source Identity

This section lists all fields related to identification of the source. The source is the identity the IoC is about, as opposed to the destination identity, which is another identity.

For examples see the table below.

The abuse type of an event defines the way these events needs to be interpreted. For example, for a botnet drone they refer to the compromised machine, whereas for a command and control server they refer the server itself.

#### Source Geolocation Identity

We recognize that ip geolocation is not an exact science and analysis of the abuse data has shown that different sources attribution sources have different opinions of the geolocation of an ip. This is why we recommend to enrich the data with as many sources as you have available and make the decision which value to use for the cc IOC based on those answers.

#### Source Local Identity

Some sources report an internal (NATed) IP address.

### Destination Identity

The abuse type of an event defines the way these IOCs needs to be interpreted. For a botnet drone they refer to the compromised machine, whereas for a command and control server they refer the server itself.

#### Destination Geolocation Identity

We recognize that ip geolocation is not an exact science and analysis of the abuse data has shown that different sources attribution sources have different opinions of the geolocation of an ip. This is why we recommend to enrich the data with as many sources as you have available and make the decision which value to use for the cc IOC based on those answers.

#### Destination Local Identity

Some sources report an internal (NATed) IP address.

### Extra values
Data which does not fit in the harmonization can be saved in the 'extra' namespace. All keys must begin with `extra.`, there are no other rules on key names and values. The values can be get/set like all other fields.

## Fields List and data types

A list of allowed fields and data types can be found in [Harmonization-fields.md](Harmonization-fields.md)

## Classification

IntelMQ classifies events using three labels: taxonomy, type and identifier. This tuple of three values can be used for deduplication of events and describes what happened.
TODO: examples from chat

The taxonomy can be automatically added by the taxonomy expert bot based on the given type. The following taxonomy-type mapping is based on [eCSIRT II Taxonomy](https://www.trusted-introducer.org/Incident-Classification-Taxonomy.pdf):

|Taxonomy|Type|Description|
|--------|----|-----------|
|abusive content|spam|Or 'Unsolicited Bulk Email', this means that the recipient has not granted verifiable permission for the message to be sent and that the message is sent as part of a larger collection of messages, all having a functionally comparable content.|
|abusive-content|harmful-speech|Discreditation or discrimination of somebody, e.g. cyber stalking, racism or threats against one or more individuals.|
|abusive-content|violence|Child pornography, glorification of violence, etc.|
|availability|ddos|Distributed Denial of Service attack, e.g. SYN-Flood or UDP-based reflection/amplification attacks.|
|availability|dos|Denial of Service attack, e.g. sending specially crafted requests to a web application which causes the application to crash or slow down.|
|availability|outage|Outage caused e.g. by air condition failure or natural disaster.|
|availability|sabotage|Physical sabotage, e.g cutting wires or malicious arson.|
|fraud|copyright|Offering or Installing copies of unlicensed commercial software or other copyright protected materials (Warez).|
|fraud|masquerade|Type of attack in which one entity illegitimately impersonates the identity of another in order to benefit from it.|
|fraud|phishing|Masquerading as another entity in order to persuade the user to reveal private credentials.|
|fraud|unauthorized-use-of-resources|Using resources for unauthorized purposes including profit-making ventures, e.g. the use of e-mail to participate in illegal profit chain letters or pyramid schemes.|
|information content security|Unauthorised-information-access|Unauthorized access to information, e.g. by abusing stolen login credentials for a system or application, intercepting traffic or gaining access to physical documents.|
|information content security|Unauthorised-information-modification|Unauthorised modification of information, e.g. by an attacker abusing stolen login credentials for a system or application or a ransomware encrypting data.|
|information content security|data-loss|Loss of data, e.g. caused by harddisk failure or physical theft.|
|information content security|dropzone|This IOC refers to place where the compromised machines store the stolen user data. Not in ENISA eCSIRT-II taxonomy.|
|information content security|leak|IOCs relating to leaked credentials or personal data. Not in ENISA eCSIRT-II taxonomy.|
|information gathering|scanner|Attacks that send requests to a system to discover weaknesses. This also includes testing processes to gather information on hosts, services and accounts. Examples: fingerd, DNS querying, ICMP, SMTP (EXPN, RCPT, ...), port scanning.|
|information-gathering|sniffing|Observing and recording of network traffic (wiretapping).|
|information-gathering|social-engineering|Gathering information from a human being in a non-technical way (e.g. lies, tricks, bribes, or threats). This IOC refers to a resource, which has been observed to perform brute-force attacks over a given application protocol.|
|intrusion attempts|brute-force|Multiple login attempts (Guessing / cracking of passwords, brute force).|
|intrusion attempts|exploit|An attack using an unknown exploit.|
|intrusion attempts|ids alert|IOCs based on a sensor network. This is a generic IOC denomination, should it be difficult to reliably denote the exact type of activity involved for example due to an anecdotal nature of the rule that triggered the alert. ENISA eCSIRT-II taxonomy: 'ids-alert'.|
|intrusions|application-compromise|Compromise of an application by exploiting (un)known software vulnerabilities, e.g. SQL injection.|
|intrusions|backdoor|This refers to hosts, which have been compromised and backdoored with a remote administration software or Trojan in the traditional sense. Not in ENISA eCSIRT-II taxonomy.|
|intrusions|burglary|Physical intrusion, e.g. into corporate building or data center.|
|intrusions|compromised|This IOC refers to compromised system. Not in ENISA eCSIRT-II taxonomy.|
|intrusions|defacement|This IOC refers to hacktivism related activity. Not in ENISA eCSIRT-II taxonomy.|
|intrusions|privileged-account-compromise|Compromise of a system where the attacker gained administrative privileges.|
|intrusions|unauthorized-command|The possibly infected device sent unauthorized commands to a remote device with malicious intent. Not in ENISA eCSIRT-II taxonomy.|
|intrusions|unauthorized-login|A possibly infected device logged in to a remote device without authorization. Not in ENISA eCSIRT-II taxonomy.|
|intrusions|unprivileged-account-compromise|Compromise of a system using an unprivileged (user/service) account.|
|malicious code|botnet drone|This is a compromised machine, which has been observed to make a connection to a command and control server. Not in ENISA eCSIRT-II taxonomy and deprecated, use 'infected system instead'.|
|malicious code|c&c|This is a command and control server in charge of a given number of botnet drones. ENISA eCSIRT-II taxonomy: 'c2server'.|
|malicious code|dga domain|DGA Domains are seen various families of malware that are used to periodically generate a large number of domain names that can be used as rendezvous points with their command and control servers. Not in ENISA eCSIRT-II taxonomy.|
|malicious code|infected system|This is a compromised machine, which has been observed to make a connection to a command and control server. ENISA eCSIRT-II taxonomy: 'infected-system'.|
|malicious code|malware|A URL is the most common resource with reference to malware binary distribution. Not in ENISA eCSIRT-II taxonomy.|
|malicious code|malware configuration|This is a resource which updates botnet drones with a new configuration.|
|malicious code|malware-distribution|URI used for malware distribution, e.g. a download URL included in fake invoice malware spam.|
|malicious code|ransomware|This IOC refers to a specific type of compromised machine, where the computer has been hijacked for ransom by the criminals. Not in ENISA eCSIRT-II taxonomy and deprecated, use 'infected system instead'.|
|other|blacklist|Some sources provide blacklists, which clearly refer to abusive behavior, such as spamming, but fail to denote the exact reason why a given identity has been blacklisted. The reason may be that the justification is anecdotal or missing entirely. This type should only be used if the typing fits the definition of a blacklist, but an event specific denomination is not possible for one reason or another.|
|other|other|All incidents which don't fit in one of the given categories should be put into this class. Not in ENISA eCSIRT-II taxonomy.|
|other|proxy|This refers to the use of proxies from inside your network. Not in ENISA eCSIRT-II taxonomy.|
|other|tor|This IOC refers to incidents related to TOR network infrastructure. Not in ENISA eCSIRT-II taxonomy.|
|other|unknown|Unknown classification. Not in ENISA eCSIRT-II taxonomy.|
|test|test|Meant for testing.|
|vulnerable|ddos-amplifier|Publicly accessible services that can be abused for conducting DDoS reflection/amplification attacks, e.g. DNS open-resolvers or NTP servers with monlist enabled.|
|vulnerable|information-disclosure|Publicly accessible services potentially disclosing sensitive information, e.g. SNMP or Redis.|
|vulnerable|potentially-unwanted-accessible|Potentially unwanted publicly accessible services, e.g. Telnet, RDP or VNC.|
|vulnerable|vulnerable client|This attribute refers to a badly configured or vulnerable clients, which may be vulnerable and can be compromised by a third party. For example, not-up-to-date clients or client which are misconfigured, such as clients querying public domains for WPAD configurations. In addition, to specify the vulnerability and its potential abuse, one should use the classification.identifier, description and other attributes for that purpose respectively. Not in ENISA eCSIRT-II taxonomy.|
|vulnerable|vulnerable service|This attribute refers to a badly configured or vulnerable network service, which may be abused by a third party. For example, these services relate to open proxies, open dns resolvers, network time servers (NTP) or character generation services (chargen), simple network management services (SNMP). In addition, to specify the network service and its potential abuse, one should use the protocol, destination port and description attributes for that purpose respectively. Not in ENISA eCSIRT-II taxonomy.|
|vulnerable|vulnerable-system|A system which is vulnerable to certain attacks. Example: misconfigured client proxy settings (example: WPAD), outdated operating system version, etc.|
|vulnerable|weak-crypto|Publicly accessible services offering weak crypto, e.g. web servers susceptible to POODLE/FREAK attacks.|

Meaning of source, destination and local values for each classification type and possible identifiers. The identifier is often a normalized malware name, grouping many variants.

|Type|Source|Destination|Local|Possible identifiers|
|----|------|-----------|-----|--------------------|
|backdoor|*backdoored device*||||
|blacklist|*blacklisted device*||||
|botnet drone|*infected device*|*contacted c2c server*|||
|brute-force|*attacker*|target|||
|c&c|*(sinkholed) c&c server*|||zeus, palevo, feodo|
|compromised|*server*||||
|ddos|*attacker*|target|||
|defacement|*defaced website*||||
|dga domain|*infected device*||||
|dropzone|*server hosting stolen data*||||
|exploit|*hosting server*||||
|ids alert|*triggering device*||||
|infected system|*infected device*|*contacted c2c server*|||
|malware|*infected device*||internal at source|zeus, palevo, feodo|
|malware configuration|*infected device*||||
|other||||||
|phishing|*phishing website*||||
|proxy|*server allowing policy and security bypass*||||
|ransomware|*infected device*||||
|scanner|*scanning device*|scanned device||http,modbus,wordpress|
|spam|*infected device*|targeted server|internal at source||
|test||||||
|unknown||||||
|vulnerable service|*vulnerable device*||| heartbleed, openresolver, snmp |
|vulnerable client|*vulnerable device*||| wpad |

Field in italics is the interesting one for CERTs.

Example:

If you know of an IP address that connects to a zeus c&c server, it's about the infected device, thus type malware and identifier zeus. If you want to complain about the c&c server, it's type c&c and identifier zeus. The `malware.name` can have the full name, eg. 'zeus_p2p'.

## Minimum recommended requirements for events

Below, we have enumerated the minimum recommended requirements for an actionable abuse event. These keys should to be present for the abuse report to make sense for the end recipient. Please note that if you choose to anonymize your sources, you can substitute **feed** with **feed.code** and that only one of the identity keys **ip**, **domain name**, **url**, **email address** must be present. All the rest of the keys are **optional**.

|Category|Key|Terminology|
|--------|---|-----------|
|Feed|feed|Should|
|Classification|classification.type|Should|
|Classification|classification.taxonomy|Should|
|Time|time.source|Should|
|Time|time.observation|Should|
|Identity|source.ip|Should*|
|Identity|source.fqdn|Should*|
|Identity|source.url|Should*|
|Identity|source.account|Should*|

* only one of them

This list of required fields is *not* enforced by IntelMQ.

**NOTE:** This document was copied from [AbuseHelper repository](https://github.com/abusesa/abusehelper/blob/master/docs/Harmonization.md) and improved.

