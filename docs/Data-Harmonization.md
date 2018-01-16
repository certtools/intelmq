## Table of Contents

1. [Overview](#overview)
2. [Rules for keys](#rules)
3. [Sections](#sections)
4. [Data types](#basicdatatypes)
5. [Fields List and data types](#fields-list-and-data-types)
6. [Type/Taxonomy Mapping](#mapping)
7. [Minimum required fields](#requirements)


<a name="overview"></a>

## Overview

All messages (reports and events) are Python/JSON dictionaries. The key names and according types are defined by the so called *harmonization*.

The purpose of this document is to list and clearly define known **fields** in Abusehelper as well as IntelMQ or similar systems. A field is a ```key=value``` pair. For a clear and unique definition of a field, we must define the **key** (field-name) as well as the possible **values**. A field belongs to an **event**. An event is basically a  structured log record in the form ```key=value, key=value, key=value, …```. In the [List of known fields](#fields), each field is grouped by a **section**. We describe these sections briefly below.
Every event **MUST** contain a timestamp field.

[IOC](https://en.wikipedia.org/wiki/Indicator_of_compromise) (Indicator of compromise) is a single observation like a log line.

<a name="rules"></a>

## Rules for keys

The keys can be grouped together in sub-fields, e.g. `source.ip` or `source.geolocation.latitude`. Thus, keys must match `^[a-z_](.[a-z0-9_]+)*$`.


<a name="sections"></a>
## Sections

As stated above, every field is organized under some section. The following is a description of the sections and what they imply.

### Feed

Fields listed under this grouping list details about the source feed where information came from.

### Time

The time section lists all fields related to time information.
This document requires that all the timestamps MUST be normalized to UTC. If the source reports only a date, do not attempt to invent timestamps.

### Source Identity

This section lists all fields related to identification of the source. **XXX FIXME: not clear!! XXX**
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

<a name="fields-list-and-data-types"></a>
## Fields List and data types

A list of allowed fields and data types can be found in [Harmonization-fields.md](Harmonization-fields.md)

<a name="mapping"></a>
## Classification

IntelMQ classifies events using three labels: taxonomy, type and identifier. This tuple of three values can be used for deduplication of events and describes what happened.
TODO: examples from chat

The taxonomy can be automatically added by the taxonomy expert bot based on the given type. The following taxonomy-type mapping is based on [eCSIRT II Taxonomy](https://www.trusted-introducer.org/Incident-Classification-Taxonomy.pdf):

|Type|Taxonomy|Description|
|----|--------|-----------|
|backdoor|intrusions|This refers to hosts, which have been compromized and backdoored with a remote administration software or trojan in the traditional sense.|
|blacklist|other|Some sources provide blacklists, which clearly refer to abusive behavior, such as spamming, but fail to denote the exact reason why a given identity has been blacklisted. The reason may be that the justification is anecdotal or missing entirely. This type should only be used if the typing fits the definition of a blacklist, but an event specific denomination is not possible for one reason or another.|
|botnet drone|malicious code|This is a compromized machine, which has been observed to make a connection to a command and control server.|
|brute-force|intrusion attempts|This IOC refers to a resource, which has been observed to perform brute-force attacks over a given application protocol. Please see the IOC protocol below.|
|c&c|malicious code|This is a command and control server in charge of a given number of botnet drones.|
|compromised|intrusions|This IOC refers to compromised system.|
|ddos|availability|This IOC refers to various parts of the DDOS infrastructure.|
|defacement|intrusions|This IOC refers to hacktivism related activity.|
|dga domain|malicious code|DGA Domains are seen various families of malware that are used to periodically generate a large number of domain names that can be used as rendezvous points with their command and control servers.|
|dropzone|information content Security|This IOC refers to place where the compromized machines store the stolen user data.|
|exploit|intrusion attempts|An exploit is often executed through a malicious URL.|
|ids alert|intrusion attempts|IOCs based on a sensor network. This is a generic IOC denomination, should it be difficult to reliably denote the exact type of activity involved for example due to an anecdotal nature of the rule that triggered the alert.|
|malware configuration|malicious code|This is a resource which updates botnet drones with a new configuration.|
|malware|malicious code|A URL is the most common resource with reference to malware binary distribution.|
|phishing|fraud|This IOC most often refers to a URL, which is phishing for user credentials.|
|proxy|other|This refers to the use of proxies from inside your network.|
|ransomware|malicious code|This IOC refers to a specific type of compromized machine, where the computer has been hijacked for ransom by the criminals.|
|scanner|information gathering|This IOC refers to port scanning activity specifically.|
|spam|abusive content|This IOC refers to resources, which make up a SPAM infrastructure, be it a harvester, dictionary attacker, URL etc.|
|test|test|This is a value for testing purposes.|
|unknown|other|unknown events|
|vulnerable service|vulnerable|This attribute refers to a badly configured or vulnerable network service, which may be abused by a third party. For example, these services relate to open proxies, open dns resolvers, network time servers (ntp) or character generation services (chargen), simple network management services (snmp). In addition, to specify the network service and its potential abuse, one should use the protocol, destination port and description attributes for that purpose respectively.|

Meaning of source, destination and local values for each classification type and possible identifiers. The identifier is often a normalized malware name, grouping many variants.

|Type|Source|Destination|Local|Possible identifiers|
|----|------|-----------|-----|--------------------|
|backdoor|*backdoored device*||||
|blacklist|*blacklisted device*||||
|botnet drone|*infected device*||||
|brute-force|*attacker*|target|||
|c&c|*(sinkholed) c&c server*|||zeus, palevo, feodo|
|compromised|*server*||||
|ddos|*attacker*|target|||
|defacement|*defaced website*||||
|dga domain|*infected device*||||
|dropzone|*server hosting stolen data*||||
|exploit|*hosting server*||||
|ids alert|*triggering device*||||
|malware|*infected device*||internal at source|zeus, palevo, feodo|
|malware configuration|*infected device*||||
|other||||||
|phishing|*phishing website*||||
|proxy|*server allowing policy and security bypass*||||
|ransomware|*infected device*||||
|scanner|*scanning device*|scanned device|||
|spam|*infected device*|targeted server|internal at source||
|test||||||
|unknown||||||
|vulnerable service|*vulnerable device*||| heartbleed, openresolver, snmp |

Field in italics is the interesting one for CERTs.

Example:

If you know of an IP address that connects to a zeus c&c server, it's about the infected device, thus type malware and identifier zeus. If you want to complain about the c&c server, it's type c&c and identifier zeus. The `malware.name` can have the full name, eg. 'zeus_p2p'.

<a name="requirements"></a>
## Minimum requirements for events

Below, we have enumerated the minimum requirements for an actionable abuse event. These keys need to be present for the abuse report to make sense for the end recipient. Please note that if you choose to anonymize your sources, you can substitute **feed** with **feed code** and that only one of the identity keys **ip**, **domain name**, **url**, **email address** must be present. All the rest of the keys are **optional**.

|Category|Key|Terminology|
|--------|---|-----------|
|Feed|feed|Must|
|Classification|classification.type|Must|
|Classification|classification.taxonomy|Must|
|Time|time.source|Must|
|Time|time.observation|Must|
|Identity|source.ip|Must*|
|Identity|source.fqdn|Must*|
|Identity|source.url|Must*|
|Identity|source.account|Must*|

This list of required fields is *not* enforced by IntelMQ.

**NOTE:** This document was copied from [AbuseHelper repository](https://github.com/abusesa/abusehelper/blob/master/docs/Harmonization.md) and improved.

