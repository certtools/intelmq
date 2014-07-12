# Data Harmonization Ontology

## Core Fields

### Feed

|Key|Format|Description|
|--------|---|-----------|
|Feed|
|feed|string(30)|Lower case name for the feeder, e.g. abusech or phishtank.|
|feed_code|string(10)|Code name for the feed, e.g.  DFGS, HSDAG etc.|
|feed_url|string(200)|The URL of a given abuse feed, where applicable|

### Time

All the timestamps should be normalized to UTC. If the source reports only a date, please do not invent timestamps.

|Key|Format|Description|
|--------|---|-----------|
|source_time|datetime|Time reported by a source. Some sources only report a date, which '''may''' be used here if there is no better observation (ISO8660)
|observation_time|datetime|The time a source bot saw the event. This timestamp becomes especially important should you perform your own attribution on a host DNS name for example. The mechanism to denote the attributed elements with reference to the source provided is detailed below in Reported Identity IOC.(ISO8660)|

### Identity

The abuse type of an event defines the way these IOC needs to be interpreted. For a botnet drone they refer to the compromized machine, whereas for a command and control server they refer the server itself.

|Key|Format|Description|
|--------|---|-----------|
|ip|ip|IPv4 or IPv6 address|
|port|int|The port through which the abuse activity is taking place. For example a command and control server report will most likely contain a port, which is directly related to the reported ip or host.|
|url|string(2000)|A URL denotes on IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
|domain_name|string(255)|DNS domain name. http://en.wikipedia.org/wiki/Domain_name|
|email_address|string(200)|An email address, whose interpretation is based on the abuse type.|
|reverse dns|string(200)|Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. "Record types other than PTR records may also appear in the reverse DNS tree." http://en.wikipedia.org/wiki/Reverse_DNS_lookup|
|asn|int|Autonomous system number|
|as_name|string(200)|Registered name for an autonomous system|
|bgp_prefix|inet|CIDR for an autonomous system|
|registry|string(20)|The IP registry a given ip address is allocated by|
|allocated|string(20)|Allocation date corresponding to bgp prefix|

### Source Identity

|Key|Format|Description|
|--------|---|-----------|
|source_ip|ip|The ip observed to initiate the connection|
|source_port|int|The port from which the connection originated|
|source_domain_name|string(255)|A DNS name related to the host from which the connection originated|
|source_email_address|string(200)|An email address, which has been identified to relate to the source of an abuse event|
|source_asn|int|The autonomous system number from which originated the connection|
|source_as_name|string(200)|The autonomous system name from which the connection originated|
|source_cc|string(2)|The country code of the ip from which the connection originated|


### Destination Identity

Since many of the sources report IOC related to a compromized machine, such as a botnet drone, they may report relevant information in relation to the command and control infrastructure as well. The meaning of each IOC needs to be interpreted with reference to the abuse type. A destination ip and port in the context of a botnet drone for example usually denote the command and control server.

|Key|Format|Description|
|--------|---|-----------|
|destination_ip|ip|The end-point of the connection|
|destination_port|int|The destination port of the connection|
|destination_domain_name|string(255)|The DNS name related to the end-point of a connection|
|destination_email_address|string(200)|An email address, which has been identified to relate to the destiantion of an abuse event|
|destination_asn|int|The autonomous system number to which the connection was destined|
|destination_as_name|string(200)|The autonomous system name to which the connection was destined|
|destination_cc|string(2)|The country code of the ip which was the end-point of the connection|


### Behing the NAT Identity

|Key|Format|Description|
|--------|---|-----------|
|local_ip|ip|Some sources report a internal (NATed) IP address related a compromized system|
|local_hostname|string(200)|Some sources report a internal hostname within a NAT related to the name configured for a compromized system|


### Reported Identity

As stated above, each abuse handling organization should define a policy, which IOC to use as the primary elements describing an abuse event. Often the sources have done their attribution, but you may choose to correlate their attributive elements with your own. In practice this means that your sanitation should prefix the elements with the '''reported''' keyword, to denote that you've decided the attribute these yourself. The list below is not comprehensive, rather than a list of common things you may want to attribute yourself. Moreover, if you choose to perform your own attribution, the observation time will become your authoritative point of reference related to these IOC.

|Key|Format|Description|
|--------|---|-----------|
|reported_ip|ip|Should you perform your own attribution on a DNS name referred to by host, the ip reported by the source is replaced|
|reported_asn|int|The autonomous system number related to the resource, which was reported by the source|
|reported_as_name|string(200)|The autonomous system name registered to the reported asn above|
|reported_cc|string(2)|The country codeof the reported IOC above|


### Geolocation

We recognize that ip geolocation is not an exact science and analysis of the abuse data has shown that different sources attribution sources have different opinions of the geolocation of an ip. This is why we recommend to enrich the data with as many sources as you have available and make the decision which value to use for the cc IOC based on those answers.

|Key|Format|Description|
|--------|---|-----------|
|cc|string(2)|MaxMind Country Code (ISO3166)|
|country|string(100)|The country name derived from the ISO3166 country code (assigned to cc field)|
|longitude|int|Longitude coordinates derived from a geolocation service, such as MaxMind geoip db|
|latitude|int|Latitude coordinates derived from a geolocation service, such as MaxMind geoip db|
|region|string(100)|Some geolocation services refer to region-level geolocation (where applicable)|
|state|string(100)|Some geolocation services refer to state-level geolocation (where applicable)|
|city|string(100)|Some geolocation services refer to city-level geolocation|


## Additional Fields

|Key|Format|Description|
|--------|---|-----------|
|description|| A free-form textual description of an abuse event.
|description url|| A description URL is a link to a further description of the the abuse event in question.
|status|| Status of the malicious resource (phishing, dropzone, etc), e.g. online, offline.
|protocol|| Used for (brute forcing) bots, e.g. vnc, ssh, sip, irc, http or p2p, as well as to describe the transport protocol of a given commmand and control mechanism. N.B. the interpretation of the protocol field depends largely on the abuse type. For some abuse types, such as brute-force, this refers to the application protocol, which is the target of the brute-forcing and for botnet drones it may refer to the transport protocol of the control mechanism for example. If both protocol and transport protocol are needed, they should be noted separately.
|transport protocol|| Some feeds report a protocol, which often denotes the observed transport. This should be noted appropriately if the protocol key should denote the vulnerable service for example.
|target|| Some sources denominate the target (organization) of a an attack.
|os name|| Operating system name.
|os version|| Operating system version.
|user agent|| Some feeds report the user agent string used by the host to access a malicious resource, such as a command and control server.
|additional information|| All anecdotal information, which cannot be parsed into the data harmonization elements.
|missing data|| If the sanitation is missing a known piece of data, such as a description url for example, the reference to this fact may be inserted here.
|comment|| Free text commentary about the abuse event inserted by an analyst.
|screenshot url|| Some source may report URLs related to a an image generated of a resource without any metadata.
|webshot url|| A URL pointing to resource, which has been rendered into a webshot, e.g. a PNG image and the relevant metadata related to its retrieval/generation.

### Malware Elements

|Key|Format|Description|
|--------|---|-----------|
|malware|| A malware family name in lower case.

### Artifact Elements

|Key|Format|Description|
|--------|---|-----------|
|artifact hash|| A string depicting a checksum for a file, be it a malware sample for example.
|artifact hash type|| The hashing algorithm used for artifact hash type above, be it MD5 or SHA-* etc. At the moment, it seems that the hash type should default to SHA-1.
|artifact version|| A version string for an identified artifact generation, e.g. a crime-ware kit.

### Extra Elements

|Key|Format|Description|
|--------|---|-----------|
|abuse contact|| An abuse contact email address for an IP network.
|event hash|| Computed event hash with specific keys and values that identify a unique event. At present, the hash should default to using the SHA1 function. Please note that for an event hash to be able to match more than one event (deduplication) the receiver of an event should calculate it based on a minimal set of keys and values present in the event. Using for example the observation time in the calculation will most likely render the checksum useless for deduplication purposes.
|shareable key|| Sometimes it is necessary to communicate a set of IOC which can be passed on freely to the end recipient. The most effective way to use this is to make it a multi-value within an event.


### Topic or Provider Specific Elements

The elements listed below are additional keys used to describe abusive behavior, which are topic specific. They may refer to the source of information, such as|notified by||, an augmentation source such as|cymru cc|| or internal integration source, such as|rtir id||. The reason why they are separated from the the other IOC is that they are not generic, rather than topic or provider specific. Their communicative function is defined as an optional way to understand what other abuse handling pipelines are most likely to call these elements.

|Key|Format|Description|
|--------|---|-----------|
|dns version|| A string describing the version of a DNS server.
|min amplification|| Minimum amplification value related to an open DNS resolver.
|notified by|| The reporter of a given abuse event, e.g. ZONE-H defacer attribution.
|cymru cc|| The country code denoted for the ip by the Team Cymru asn to ip mapping service.
|geoip cc|| The country code denoted for the ip by the MaxMind geoip database.
|rtir id|| RTIR incident id.
|misp id|| MISP id.
|original logline|| In case we received this event as a (CSV) log line, we can store the original line here.

## Classification Fields

Having a functional ontology to work with, especially for the abuse types is important for you to be able to classify, prioritize and report relevant actionable intelligence to the parties who need to be informed. The driving idea for this ontology has been to use a minimal set of values with maximal usability. Below, is a list of harmonized values for the abuse types.

|Key|Format|Description|
|--------|---|-----------|
|type|| The abuse type IOC is one of the most crucial pieces of information for any given abuse event. The main idea of dynamic typing is to keep our ontology flexible, since we need to evolve with the evolving threatscape of abuse data. In contrast with the static taxonomy below, the dynamic typing is used to perform business decisions in the abuse handling pipeline. Furthermore, the value data set should be kept as minimal as possible to avoid "type explosion", which in turn dilutes the business value of the dynamic typing. In general, we normally have two types of abuse type IOC: ones referring to a compromized resource or ones referring to pieces of the criminal infrastructure, such as a command and control servers for example.
|taxonomy|| We recognize the need for the CSIRT teams to apply a static (incident) taxonomy to abuse data. With this goal in mind the type IOC will serve as a basis for this activity. Each value of the dynamic type mapping translates to a an element in the static taxonomy. The European CSIRT teams for example have decided to apply the eCSIRT.net incident classification. The value of the taxonomy key is thus a derivative of the dynamic type above. For more information about check [ENISA taxonomies](http://www.enisa.europa.eu/activities/cert/support/incident-management/browsable/incident-handling-process/incident-taxonomy/existing-taxonomies).
 

 
|Type|Taxonomy|Description|
|----|--------|-----------|
|spam|Abusive Content|This IOC refers to resources, which make up a SPAM infrastructure, be it a harvester, dictionary attacker, URL etc.|
|malware|Malicious Code|A URL is the most common resource with reference to malware binary distribution.|
|botnet drone|Malicious Code|This is a compromized machine, which has been observed to make a connection to a command and control server.|
|ransomware|Malicious Code|This IOC refers to a specific type of compromized machine, where the computer has been hijacked for ransom by the criminals.|
|malware configuration|Malicious Code|This is a resource which updates botnet drones with a new configuration.|
|c&c|Malicious Code|This is a command and control server in charge of a given number of botnet drones.|
|scanner|Information Gathering|This IOC refers to port scanning activity specifically.|
|exploit|Intrusion Attempts|An exploit is often executed through a malicious URL.|
|brute-force|Intrusion Attempts|This IOC refers to a resource, which has been observed to perform brute-force attacks over a given application protocol. Please see the IOC protocol below.|
|ids alert|Intrusion Attempts|IOCs based on a sensor network. This is a generic IOC denomination, should it be difficult to reliably denote the exact type of activity involved for example due to an anecdotal nature of the rule that triggered the alert.|
|defacement|Intrusions|This IOC refers to hacktivism related activity.|
|backdoor|Intrusions|This refers to hosts, which have been compromized and backdoored with a remote administration software or trojan in the traditional sense.|
|ddos|Availability|This IOC refers to various parts of the DDOS infrastructure.|
|dropzone|Information Content Security|This IOC refers to place where the compromized machines store the stolen user data.|
|phishing|Fraud|This IOC most often refers to a URL, which is phishing for user credentials.|
|vulnerable service|Vulnerable|This attribute refers to a badly configured or vulnerable network service, which may be abused by a third party. For example, these services relate to open proxies, open dns resolvers, network time servers (ntp) or character generation services (chargen), simple network management services (snmp). In addition, to specify the network service and its potential abuse, one should use the protocol, destination port and description attributes for that purpose respectively.|
|blacklist|Other|Some sources provide blacklists, which clearly refer to abusive behavior, such as spamming, but fail to denote the exact reason why a given identity has been blacklisted. The reason may be that the justification is anecdotal or missing entirely. This type should only be used if the typing fits the definition of a blacklist, but an event specific denomination is not possible for one reason or another.|
|test|Test|This is a value for testing purposes.|

## Minimum Requirements

Below, we have enumerated the minimum requirements for an actionable abuse event. These keys need to be present for the abuse report to make sense for the end recipient. Please note that if you choose to anonymize your sources, you can substitute **feed** with **feed code** and that only one of the identity keys **ip**, **domain name**, **url**, **email address** must be present. All the rest of the keys enumerated above are **optional**.

|Category|Key|Terminology|
|--------|---|-----------|
|Feed|feed|Must|
|Classification|type|Must|
|Classification|taxonomy|Must|
|Time|observation time|Must|
|Identity|ip|Must*|
|Identity|domain name|Must*|
|Identity|url|Must*|
|Identity|email address|Must*|



**NOTE:** This document was copied from [AbuseHelper repository](https://bitbucket.org/clarifiednetworks/abusehelper/wiki/Data Harmonization Ontology)
