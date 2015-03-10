## Table of Contents

1. [Sections](#sections)
2. [Fields List](#fields)
3. [Type/Taxonomy Mapping](#mapping)
4. [Minimum Requirements](#requirements)


<a name="sections"></a>
## Sections


#### Feed

Details about the source feed where information came from.

#### Time

All the timestamps should be normalized to UTC. If the source reports only a date, please do not invent timestamps

#### Source Identity

The abuse type of an event defines the way these IOC needs to be interpreted. For a botnet drone they refer to the compromized machine, whereas for a command and control server they refer the server itself.

#### Source Geolocation Identity

We recognize that ip geolocation is not an exact science and analysis of the abuse data has shown that different sources attribution sources have different opinions of the geolocation of an ip. This is why we recommend to enrich the data with as many sources as you have available and make the decision which value to use for the cc IOC based on those answers.

#### Source Local Identity

Some sources report an internal (NATed) IP address.

#### Destination Identity

The abuse type of an event defines the way these IOCs needs to be interpreted. For a botnet drone they refer to the compromized machine, whereas for a command and control server they refer the server itself.

#### Destination Geolocation Identity

We recognize that ip geolocation is not an exact science and analysis of the abuse data has shown that different sources attribution sources have different opinions of the geolocation of an ip. This is why we recommend to enrich the data with as many sources as you have available and make the decision which value to use for the cc IOC based on those answers.

#### Destination Local Identity

Some sources report an internal (NATed) IP address.


#### Reported Source Identity

As stated above, each abuse handling organization should define a policy, which IOC to use as the primary element describing an abuse event. Often the sources have done their attribution, but you may choose to correlate their attributive elements with your own. In practice this means that your sanitation should prefix the elements with the '''reported''' keyword, to denote that you've decided the attribute these yourself. The list below is not comprehensive, rather than a list of common things you may want to attribute yourself. Moreover, if you choose to perform your own attribution, the observation time will become your authoritative point of reference related to these IOC.

#### Reported Destination Identity

As stated above, each abuse handling organization should define a policy, which IOC to use as the primary elements describing an abuse event. Often the sources have done their attribution, but you may choose to correlate their attributive elements with your own. In practice this means that your sanitation should prefix the elements with the '''reported''' keyword, to denote that you've decided the attribute these yourself. The list below is not comprehensive, rather than a list of common things you may want to attribute yourself. Moreover, if you choose to perform your own attribution, the observation time will become your authoritative point of reference related to these IOC.


#### Additional Fields

... text ...

#### Malware Elements

... text ...

#### Artifact Elements

... text ...

#### Extra Elements

... text ...

#### Specific Elements

The elements listed below are additional keys used to describe abusive behavior, which are topic specific. They may refer to the source of information, such as notified by, an augmentation source such a cymru cc or internal integration source, such as|rtir id||. The reason why they are separated from the the other IOCs is that they are not generic, rather than topic or provider specific. Their communicative function is defined as an optional way to understand what other abuse handling pipelines are most likely to call these elements.

#### Classification

Having a functional ontology to work with, especially for the abuse types is important for you to be able to classify, prioritize and report relevant actionable intelligence to the parties who need to be informed. The driving idea for this ontology has been to use a minimal set of values with maximal usability. Below, is a list of harmonized values for the abuse types.

<a name="fields"></a>
## Fields List

### Rules

All keys MUST be written in lowercase.


### List

|Section|Fields|Format|Syntax|Description|
|:---:|:---:|:---:|:----------:|:-----------:|
|Feed|feed|varchar(2000)|printable ASCII string|Lower case name for the feeder, e.g. abusech or phishtank.|
|Feed|feed_code|varchar(2000)|printable ASCII string|Code name for the feed, e.g.  DFGS, HSDAG etc.|
|Feed|feed_url|varchar(2000)|a valid URL (see RFC3987 or similar). It is recommended to use libaries such as [faup](https://github.com/stricaud/faup) for validation|The URL of a given abuse feed, where applicable|
|Time|source_time|timestamp with time zone|according to [wikipedia](https://en.wikipedia.org/wiki/ISO_8601)| Time reported by a source. Some sources only report a date, which '''may''' be used here if there is no better observation (ISO8660)|
|Time|observation_time|timestamp with time zone|see source_time|The time a source bot saw the event. This timestamp becomes especially important should you perform your own attribution on a host DNS name for example. The mechanism to denote the attributed elements with reference to the source provided is detailed below in Reported Identity IOC.(ISO8660)|
|Source Identity|source_ip|inet|valid IPv4 or IPv6 address: ```[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}``` or better validate it via python: [stackoverflow](https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python)|The ip observed to initiate the connection|
|Source Identity|source_port|integer|```[0-9]{1,5}```|The port from which the connection originated|
|Source Identity|source_domain_name|varchar(255)|see [RFC1123](http://tools.ietf.org/html/rfc1123): ```^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$```|A DNS name related to the host from which the connection originated|
|Source Identity|source_url|varchar(2000)|see feed_url|A URL denotes an IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
|Source Identity |source_email_address|varchar(2000)|see [RFC5322](http://tools.ietf.org/html/rfc5322#section-3.4): ``` [a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?```|An email address, which has been identified to relate to the source of an abuse event|
|Source Identity|source_reverse_dns|varchar(2000)|printable ASCII string|Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. Record types other than PTR records may also appear in the reverse DNS tree. Furthermore, unfortunately, there is no rule prohibiting people from writing anything in a PTR record. Even Javascript will work.|
|Source Identity|source_asn|integer|1-4294967295 (32 bit)|The autonomous system number from which originated the connection|
|Source Identity|source_as_name|varchar(2000)|printable ASCII string|The autonomous system name from which the connection originated|
|Source Identity|source_bgp_prefix|inet|see regular expression for source_ip + ```/[0-9]{1,3}``` | CIDR for an autonomous system|
|Source Identity|source_registry|varchar(2000)|printable ASCII string|The IP registry a given ip address is allocated by|
|Source Identity|source_allocated|timestamp|see source_time|Allocation date corresponding to bgp prefix|
|Source Local Identity|source_local_ip|inet|see source_ip|Some sources report a internal (NATed) IP address related a compromized system|
|Source Local Identity|source_local_hostname|varchar(2000)|printable ASCII string|Some sources report a internal hostname within a NAT related to the name configured for a compromized system. N.B.: this can be any Windows machine name. So we do not restrict ourselves here to DNS names / DNS regular expressions|
|Source Geolocation|source_cc|varchar(2)|```[a-zA-Z0-9]{2}```|MaxMind Country Code (ISO3166)|
|Source Geolocation|source_country|printable ASCII string| varchar(2000)|The country name derived from the ISO3166 country code (assigned to cc field)|
|Source Geolocation|source_longitude|float|```[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?```|Longitude coordinates derived from a geolocation service, such as MaxMind geoip db|
|Source Geolocation|source_latitude|float|```[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?```|Latitude coordinates derived from a geolocation service, such as MaxMind geoip db|
|Source Geolocation|source_region|varchar(2000)|printable ASCII string|Some geolocation services refer to region-level geolocation (where applicable)|
|Source Geolocation|source_state|varchar(2000)|printable ASCII string|Some geolocation services refer to state-level geolocation (where applicable)|
|Source Geolocation|source_city|varchar(2000)|printable ASCII string|Some geolocation services refer to city-level geolocation|
|Source Geolocation|source_cymru_cc|varchar(2)|```[a-zA-Z0-9]{2}```|The country code denoted for the ip by the Team Cymru asn to ip mapping service.|
|Source Geolocation|source_geoip_cc|varchar(2)|```[a-zA-Z0-9]{2}```|The country code denoted for the ip by the MaxMind geoip database.|
|Destination Identity|destination_ip|inet|see source_ip|The ip observed to initiate the connection|
|Destination Identity|destination_port|integer|see source_port|The port from which the connection originated|
|Destination Identity|destination_domain_name|varchar(2000)|see source_domain_name|A DNS name related to the host from which the connection originated|
|Destination Identity|destination_url|varchar(2000)|see source_url|A URL denotes on IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
|Destination Identity|destination_email_address|varchar(2000)|see source_email_address|An email address, which has been identified to relate to the source of an abuse event|
|Destination Identity|destination_reverse_dns|varchar(2000)|see source_reverse_dns|Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. "Record types other than PTR records may also appear in the reverse DNS tree."|
|Destination Identity|destination_asn|integer|see source_asn|The autonomous system number from which originated the connection|
|Destination Identity|destination_as_name|varchar(2000)|see source_as_name|The autonomous system name from which the connection originated|
|Destination Identity|destination_bgp_prefix|inet|see source_bgp_prefix|CIDR for an autonomous system|
|Destination Identity|destination_registry|varchar(2000)|see source_registry|The IP registry a given ip address is allocated by|
|Destination Identity|destination_allocated|timestamp|see source_allocated|Allocation date corresponding to bgp prefix|
|Destination Local Identity|destination_local_ip|inet|see source_ip|Some sources report a internal (NATed) IP address related a compromized system. N.B. [RFC1918](https://www.rfc-editor.org/info/rfc1918) IPs are OK here.|
|Destination Local Identity|destination_local_hostname|varchar(2000)|see source_local_hostname|Some sources report a internal hostname within a NAT related to the name configured for a compromized system|
|Destination Geolocation|destination_cc|varchar(2)|see source_cc|MaxMind Country Code (ISO3166)|
|Destination Geolocation|destination_country|varchar(2000)|see source_country|The country name derived from the ISO3166 country code (assigned to cc field)|
|Destination Geolocation|destination_longitude|integer|see source_longitude|Longitude coordinates derived from a geolocation service, such as MaxMind geoip db|
|Destination Geolocation|destination_latitude|integer|see source_latitude|Latitude coordinates derived from a geolocation service, such as MaxMind geoip db|
|Destination Geolocation|destination_region|varchar(2000)|see source_region|Some geolocation services refer to region-level geolocation (where applicable)|
|Destination Geolocation|destination_state|varchar(2000)|see source_state|Some geolocation services refer to state-level geolocation (where applicable)|
|Destination Geolocation|destination_city|varchar(2000)|see source_city|Some geolocation services refer to city-level geolocation|
|Destination Geolocation|destination_cymru_cc|varchar(2000)|see source_cymru_cc|The country code denoted for the ip by the Team Cymru asn to ip mapping service.|
|Destination Geolocation|destination_geoip_cc|varchar(2000)|see source_geoip_cc|The country code denoted for the ip by the MaxMind geoip database.|
|Reported Source Identity|reported_source_ip|varchar(2000)|see source_ip|The ip observed to initiate the connection|
|Reported Source Identity|reported_source_port|varchar(2000)|see source_port|The port from which the connection originated|
|Reported Source Identity|reported_source_domain_name|varchar(2000)|see source_domain_name|A DNS name related to the host from which the connection originated|
|Reported Source Identity|reported_source_url|varchar(2000)|see source_url|A URL denotes on IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
|Reported Source Identity|reported_source_email_address|varchar(2000)|see source_email|An email address, which has been identified to relate to the source of an abuse event|
|Reported Source Identity|reported_source_reverse_dns|varchar(2000)|see source_reverse_dns|Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. "Record types other than PTR records may also appear in the reverse DNS tree."|
|Reported Source Identity|reported_source_asn|varchar(2000)|see source_asn|The autonomous system number from which originated the connection|
|Reported Source Identity|reported_source_as_name|varchar(2000)|see source_as_name|The autonomous system name from which the connection originated|
|Reported Source Identity|reported_source_cc|varchar(2000)|see source_cc|The country code of the ip from which the connection originated|
|Reported Source Identity|reported_source_bgp_prefix|varchar(2000)|see source_bgp_prefix|CIDR for an autonomous system|
|Reported Source Identity|reported_source_registry|varchar(2000)|see source_registry|The IP registry a given ip address is allocated by|
|Reported Source Identity|reported_source_allocated|varchar(2000)|see source_allocated|Allocation date corresponding to bgp prefix|
|Reported Destination Identity|reported_destination_ip|varchar(2000)|see source_ip|The ip observed to initiate the connection|
|Reported Destination Identity|reported_destination_port|varchar(2000)|see source_port|The port from which the connection originated|
|Reported Destination Identity|reported_destination_domain_name|varchar(2000)|see source_domain_name|A DNS name related to the host from which the connection originated|
|Reported Destination Identity|reported_destination_url|varchar(2000)|see source_url|A URL denotes on IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
|Reported Destination Identity|reported_destination_email_address|varchar(2000)|see source_email_address|An email address, which has been identified to relate to the source of an abuse event|
|Reported Destination Identity|reported_destination_reverse_dns|varchar(2000)|see source_reverse_dns|Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. "Record types other than PTR records may also appear in the reverse DNS tree."|
|Reported Destination Identity|reported_destination_asn|varchar(2000)|see source_asn|The autonomous system number from which originated the connection|
|Reported Destination Identity|reported_destination_as_name|varchar(2000)|see source_as_name|The autonomous system name from which the connection originated|
|Reported Destination Identity|reported_destination_cc|varchar(2000)|see source_cc|The country code of the ip from which the connection originated|
|Reported Destination Identity|reported_destination_bgp_prefix|varchar(2000)|see source_bgp_prefix|CIDR for an autonomous system|
|Reported Destination Identity|reported_destination_registry|varchar(2000)|see source_registry|The IP registry a given ip address is allocated by|
|Reported Destination Identity|reported_destination_allocated|varchar(2000)|see source_allocated|Allocation date corresponding to bgp prefix|
|Additional Fields|description|varchar(2000)| printable ASCII characters|A free-form textual description of an abuse event.|
|Additional Fields|description_url|varchar(2000)| see source_url|A description URL is a link to a further description of the the abuse event in question.|
|Additional Fields|status|varchar(2000)| printable ASCII characters|Status of the malicious resource (phishing, dropzone, etc), e.g. online, offline.|
|Additional Fields|application_protocol|varchar(2000)|printable ASCII characters|e.g. vnc, ssh, sip, irc, http or p2p.|
|Additional Fields|transport_protocol|varchar(2000)|printable ASCII characters|e.g. tcp, udp, icmp|
|Additional Fields|target|varchar(2000)|printable ASCII characters|Some sources denominate the target (organization) of a an attack.|
|Additional Fields|os_name|varchar(2000)|printable ASCII characters|Operating system name.|
|Additional Fields|os_version|varchar(2000)|printable ASCII characters|Operating system version.|
|Additional Fields|user_agent|varchar(2000)|printable ASCII characters|Some feeds report the user agent string used by the host to access a malicious resource, such as a command and control server.|
|Additional Fields|additional_information|varchar(2000)|printable ASCII characters|All anecdotal information, which cannot be parsed into the data harmonization elements.|
|Additional Fields|missing_data|varchar(2000)|printable ASCII characters|If the sanitation is missing a known piece of data, such as a description url for example, the reference to this fact may be inserted here.|
|Additional Fields|comment|varchar(2000)|printable ASCII characters|Free text commentary about the abuse event inserted by an analyst.|
|Additional Fields|screenshot_url|varchar(2000)|see source_url|Some source may report URLs related to a an image generated of a resource without any metadata.|
|Additional Fields|webshot_url|varchar(2000)|see source_url|A URL pointing to resource, which has been rendered into a webshot, e.g. a PNG image and the relevant metadata related to its retrieval/generation.|
|Malware Elements|malware|varchar(2000)|printable ASCII characters|A malware family name in lower case.|
|Artifact Elements|artifact_hash|varchar(2000)|```[a-fA-F0-9]+``` (a hex string)|A string depicting a checksum for a file, be it a malware sample for example.|
|Artifact Elements|artifact_hash_type|varchar(2000)|printable ASCII characters|The hashing algorithm used for artifact hash type above, be it MD5 or SHA-* etc. At the moment, it seems that the hash type should default to SHA-1.|
|Artifact Elements|artifact_version|varchar(2000)|printable ASCII characters|A version string for an identified artifact generation, e.g. a crime-ware kit.|
|Extra Elements|abuse_contact|varchar(2000)|see source_email_address|An abuse contact email address for an IP network.|
|Extra Elements|event_hash|varchar(2000)|see artifact_hash|Computed event hash with specific keys and values that identify a unique event. At present, the hash should default to using the SHA1 function. Please note that for an event hash to be able to match more than one event (deduplication) the receiver of an event should calculate it based on a minimal set of keys and values present in the event. Using for example the observation time in the calculation will most likely render the checksum useless for deduplication purposes.|
|Extra Elements|shareable_key|varchar(2000)|printable ASCII character|Sometimes it is necessary to communicate a set of IOC which can be passed on freely to the end recipient. The most effective way to use this is to make it a multi-value within an event.|
|Specific Elements|rtir_id|integer|```[0-9]+```|RTIR incident id.|
|Specific Elements|misp_id|integer|```[0-9]+```|MISP id.|
|Specific Elements|original_logline|varchar(2000)|printable ASCII character|In case we received this event as a (CSV) log line, we can store the original line here.|
|Classification|type|varchar(2000)|printable ASCII character|The abuse type IOC is one of the most crucial pieces of information for any given abuse event. The main idea of dynamic typing is to keep our ontology flexible, since we need to evolve with the evolving threatscape of abuse data. In contrast with the static taxonomy below, the dynamic typing is used to perform business decisions in the abuse handling pipeline. Furthermore, the value data set should be kept as minimal as possible to avoid "type explosion", which in turn dilutes the business value of the dynamic typing. In general, we normally have two types of abuse type IOC: ones referring to a compromized resource or ones referring to pieces of the criminal infrastructure, such as a command and control servers for example.|
|Classification|taxonomy|varchar(2000)|printable ASCII character|We recognize the need for the CSIRT teams to apply a static (incident) taxonomy to abuse data. With this goal in mind the type IOC will serve as a basis for this activity. Each value of the dynamic type mapping translates to a an element in the static taxonomy. The European CSIRT teams for example have decided to apply the eCSIRT.net incident classification. The value of the taxonomy key is thus a derivative of the dynamic type above. For more information about check [ENISA taxonomies](http://www.enisa.europa.eu/activities/cert/support/incident-management/browsable/incident-handling-process/incident-taxonomy/existing-taxonomies).|
 

<a name="mapping"></a>
## Type/Taxonomy Mapping

The following mapping is based on eCSIRT Taxonomy.
 
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
|compromised|Intrusions|This IOC refers to compromised system.|
|backdoor|Intrusions|This refers to hosts, which have been compromized and backdoored with a remote administration software or trojan in the traditional sense.|
|ddos|Availability|This IOC refers to various parts of the DDOS infrastructure.|
|dropzone|Information Content Security|This IOC refers to place where the compromized machines store the stolen user data.|
|phishing|Fraud|This IOC most often refers to a URL, which is phishing for user credentials.|
|vulnerable service|Vulnerable|This attribute refers to a badly configured or vulnerable network service, which may be abused by a third party. For example, these services relate to open proxies, open dns resolvers, network time servers (ntp) or character generation services (chargen), simple network management services (snmp). In addition, to specify the network service and its potential abuse, one should use the protocol, destination port and description attributes for that purpose respectively.|
|blacklist|Other|Some sources provide blacklists, which clearly refer to abusive behavior, such as spamming, but fail to denote the exact reason why a given identity has been blacklisted. The reason may be that the justification is anecdotal or missing entirely. This type should only be used if the typing fits the definition of a blacklist, but an event specific denomination is not possible for one reason or another.|
|unknown|Other|unknown events|
|test|Test|This is a value for testing purposes.|

<a name="requirements"></a>
## Minimum Requirements

Below, we have enumerated the minimum requirements for an actionable abuse event. These keys need to be present for the abuse report to make sense for the end recipient. Please note that if you choose to anonymize your sources, you can substitute **feed** with **feed code** and that only one of the identity keys **ip**, **domain name**, **url**, **email address** must be present. All the rest of the keys enumerated above are **optional**.

|Category|Key|Terminology|
|--------|---|-----------|
|Feed|feed|Must|
|Classification|type|Must|
|Classification|taxonomy|Must|
|Time|source time|Must|
|Time|observation time|Must|
|Identity|source_ip|Must*|
|Identity|source_domain_name|Must*|
|Identity|source_url|Must*|
|Identity|source_email_address|Must*|



**NOTE:** This document was copied from [AbuseHelper repository](https://bitbucket.org/clarifiednetworks/abusehelper/wiki/Data Harmonization Ontology) and improved.
