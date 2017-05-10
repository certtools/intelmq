
Harmonization field names
=========================

|Section|Name|Type|Description|
|:------|:---|:---|:----------|
|Classification|classification.identifier|[String](#string)|The lowercase identifier defines the actual software or service (e.g. 'heartbleed' or 'ntp_version') or standardized malware name (e.g. 'zeus'). Note that you MAY overwrite this field during processing for your individual setup. This field is not standardized across IntelMQ setups/users.|
|Classification|classification.taxonomy|[LowercaseString](#lowercasestring)|We recognize the need for the CSIRT teams to apply a static (incident) taxonomy to abuse data. With this goal in mind the type IOC will serve as a basis for this activity. Each value of the dynamic type mapping translates to a an element in the static taxonomy. The European CSIRT teams for example have decided to apply the eCSIRT.net incident classification. The value of the taxonomy key is thus a derivative of the dynamic type above. For more information about check [ENISA taxonomies](http://www.enisa.europa.eu/activities/cert/support/incident-management/browsable/incident-handling-process/incident-taxonomy/existing-taxonomies).|
|Classification|classification.type|[ClassificationType](#classificationtype)|The abuse type IOC is one of the most crucial pieces of information for any given abuse event. The main idea of dynamic typing is to keep our ontology flexible, since we need to evolve with the evolving threatscape of abuse data. In contrast with the static taxonomy below, the dynamic typing is used to perform business decisions in the abuse handling pipeline. Furthermore, the value data set should be kept as minimal as possible to avoid “type explosion”, which in turn dilutes the business value of the dynamic typing. In general, we normally have two types of abuse type IOC: ones referring to a compromised resource or ones referring to pieces of the criminal infrastructure, such as a command and control servers for example.|
| |comment|[String](#string)|Free text commentary about the abuse event inserted by an analyst.|
|Destination|destination.abuse_contact|[LowercaseString](#lowercasestring)|Abuse contact for destination address. A comma separated list.|
|Destination|destination.account|[String](#string)|An account name or email address, which has been identified to relate to the destination of an abuse event.|
|Destination|destination.allocated|[DateTime](#datetime)|Allocation date corresponding to BGP prefix.|
|Destination|destination.as_name|[String](#string)|The autonomous system name to which the connection headed.|
|Destination|destination.asn|[Integer](#integer)|The autonomous system number to which the connection headed.|
|Destination|destination.fqdn|[FQDN](#fqdn)|A DNS name related to the host from which the connection originated. DNS allows even binary data in DNS, so we have to allow everything. A final point is stripped, string is converted to lower case characters.|
|Destination Geolocation|destination.geolocation.cc|[UppercaseString](#uppercasestring)|Country-Code according to ISO3166-1 alpha-2 for the destination IP.|
|Destination Geolocation|destination.geolocation.city|[String](#string)|Some geolocation services refer to city-level geolocation.|
|Destination Geolocation|destination.geolocation.country|[String](#string)|The country name derived from the ISO3166 country code (assigned to cc field).|
|Destination Geolocation|destination.geolocation.latitude|[Float](#float)|Latitude coordinates derived from a geolocation service, such as MaxMind geoip db.|
|Destination Geolocation|destination.geolocation.longitude|[Float](#float)|Longitude coordinates derived from a geolocation service, such as MaxMind geoip db.|
|Destination Geolocation|destination.geolocation.region|[String](#string)|Some geolocation services refer to region-level geolocation.|
|Destination Geolocation|destination.geolocation.state|[String](#string)|Some geolocation services refer to state-level geolocation.|
|Destination|destination.ip|[IPAddress](#ipaddress)|The IP which is the target of the observed connections.|
|Destination|destination.local_hostname|[String](#string)|Some sources report a internal hostname within a NAT related to the name configured for a compromized system|
|Destination|destination.local_ip|[IPAddress](#ipaddress)|Some sources report a internal (NATed) IP address related a compromized system. N.B. RFC1918 IPs are OK here.|
|Destination|destination.network|[IPNetwork](#ipnetwork)|CIDR for an autonomous system. Also known as BGP prefix. If multiple values are possible, select the most specific.|
|Destination|destination.port|[Integer](#integer)|The port to which the connection headed.|
|Destination|destination.registry|[Registry](#registry)|The IP registry a given ip address is allocated by.|
|Destination|destination.reverse_dns|[FQDN](#fqdn)|Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. Record types other than PTR records may also appear in the reverse DNS tree. Furthermore, unfortunately, there is no rule prohibiting people from writing anything in a PTR record. Even JavaScript will work. A final point is stripped, string is converted to lower case characters.|
|Destination|destination.tor_node|[Boolean](#boolean)|If the destination IP was a known tor node.|
|Destination|destination.url|[URL](#url)|A URL denotes on IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
|Event_Description|event_description.target|[String](#string)|Some sources denominate the target (organization) of a an attack.|
|Event_Description|event_description.text|[String](#string)|A free-form textual description of an abuse event.|
|Event_Description|event_description.url|[URL](#url)|A description URL is a link to a further description of the the abuse event in question.|
| |event_hash|[UppercaseString](#uppercasestring)|Computed event hash with specific keys and values that identify a unique event. At present, the hash should default to using the SHA1 function. Please note that for an event hash to be able to match more than one event (deduplication) the receiver of an event should calculate it based on a minimal set of keys and values present in the event. Using for example the observation time in the calculation will most likely render the checksum useless for deduplication purposes.|
| |extra|[JSON](#json)|All anecdotal information, which cannot be parsed into the data harmonization elements. E.g. os.name, os.version, etc.  **Note**: this is only intended for mapping any fields which can not map naturally into the data harmonization. It is not intended for extending the data harmonization with your own fields.|
|Feed|feed.accuracy|[Accuracy](#accuracy)|A float between 0 and 100 that represents how accurate the data in the feed is|
|Feed|feed.code|[String](#string)|Code name for the feed, e.g. DFGS, HSDAG etc.|
|Feed|feed.documentation|[String](#string)|A URL or hint where to find the documentation of this feed.|
|Feed|feed.name|[String](#string)|Name for the feed, usually found in collector bot configuration.|
|Feed|feed.provider|[String](#string)|Name for the provider of the feed, usually found in collector bot configuration.|
|Feed|feed.url|[URL](#url)|The URL of a given abuse feed, where applicable|
|Malware Hash|malware.hash.md5|[String](#string)|A string depicting an MD5 checksum for a file, be it a malware sample for example.|
|Malware Hash|malware.hash.sha1|[String](#string)|A string depicting a SHA1 checksum for a file, be it a malware sample for example.|
|Malware Hash|malware.hash.sha256|[String](#string)|A string depicting a SHA256 checksum for a file, be it a malware sample for example.|
|Malware|malware.name|[LowercaseString](#lowercasestring)|A malware family name in lower case.|
|Malware|malware.version|[String](#string)|A version string for an identified artifact generation, e.g. a crime-ware kit.|
|Misp|misp.attribute_uuid|[LowercaseString](#lowercasestring)|MISP - Malware Information Sharing Platform & Threat Sharing UUID of an attribute.|
|Misp|misp.event_uuid|[LowercaseString](#lowercasestring)|MISP - Malware Information Sharing Platform & Threat Sharing UUID.|
| |output|[JSON](#json)|Event data converted into foreign format, intended to be exported by output plugin.|
|Protocol|protocol.application|[LowercaseString](#lowercasestring)|e.g. vnc, ssh, sip, irc, http or p2p.|
|Protocol|protocol.transport|[LowercaseString](#lowercasestring)|e.g. tcp, udp, icmp.|
| |raw|[Base64](#base64)|The original line of the event from encoded in base64.|
| |rtir_id|[Integer](#integer)|Request Tracker Incident Response incident id.|
| |screenshot_url|[URL](#url)|Some source may report URLs related to a an image generated of a resource without any metadata. Or an URL pointing to resource, which has been rendered into a webshot, e.g. a PNG image and the relevant metadata related to its retrieval/generation.|
|Source|source.abuse_contact|[LowercaseString](#lowercasestring)|Abuse contact for source address. A comma separated list.|
|Source|source.account|[String](#string)|An account name or email address, which has been identified to relate to the source of an abuse event.|
|Source|source.allocated|[DateTime](#datetime)|Allocation date corresponding to BGP prefix.|
|Source|source.as_name|[String](#string)|The autonomous system name from which the connection originated.|
|Source|source.asn|[Integer](#integer)|The autonomous system number from which originated the connection.|
|Source|source.fqdn|[FQDN](#fqdn)|A DNS name related to the host from which the connection originated. DNS allows even binary data in DNS, so we have to allow everything. A final point is stripped, string is converted to lower case characters.|
|Source Geolocation|source.geolocation.cc|[UppercaseString](#uppercasestring)|Country-Code according to ISO3166-1 alpha-2 for the source IP.|
|Source Geolocation|source.geolocation.city|[String](#string)|Some geolocation services refer to city-level geolocation.|
|Source Geolocation|source.geolocation.country|[String](#string)|The country name derived from the ISO3166 country code (assigned to cc field).|
|Source Geolocation|source.geolocation.cymru_cc|[UppercaseString](#uppercasestring)|The country code denoted for the ip by the Team Cymru asn to ip mapping service.|
|Source Geolocation|source.geolocation.geoip_cc|[UppercaseString](#uppercasestring)|MaxMind Country Code (ISO3166-1 alpha-2).|
|Source Geolocation|source.geolocation.latitude|[Float](#float)|Latitude coordinates derived from a geolocation service, such as MaxMind geoip db.|
|Source Geolocation|source.geolocation.longitude|[Float](#float)|Longitude coordinates derived from a geolocation service, such as MaxMind geoip db.|
|Source Geolocation|source.geolocation.region|[String](#string)|Some geolocation services refer to region-level geolocation.|
|Source Geolocation|source.geolocation.state|[String](#string)|Some geolocation services refer to state-level geolocation.|
|Source|source.ip|[IPAddress](#ipaddress)|The ip observed to initiate the connection|
|Source|source.local_hostname|[String](#string)|Some sources report a internal hostname within a NAT related to the name configured for a compromised system|
|Source|source.local_ip|[IPAddress](#ipaddress)|Some sources report a internal (NATed) IP address related a compromised system. N.B. RFC1918 IPs are OK here.|
|Source|source.network|[IPNetwork](#ipnetwork)|CIDR for an autonomous system. Also known as BGP prefix. If multiple values are possible, select the most specific.|
|Source|source.port|[Integer](#integer)|The port from which the connection originated.|
|Source|source.registry|[Registry](#registry)|The IP registry a given ip address is allocated by.|
|Source|source.reverse_dns|[FQDN](#fqdn)|Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. Record types other than PTR records may also appear in the reverse DNS tree. Furthermore, unfortunately, there is no rule prohibiting people from writing anything in a PTR record. Even JavaScript will work. A final point is stripped, string is converted to lower case characters.|
|Source|source.tor_node|[Boolean](#boolean)|If the source IP was a known tor node.|
|Source|source.url|[URL](#url)|A URL denotes an IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
| |status|[String](#string)|Status of the malicious resource (phishing, dropzone, etc), e.g. online, offline.|
|Time|time.observation|[DateTime](#datetime)|The time a source bot saw the event. This timestamp becomes especially important should you perform your own attribution on a host DNS name for example. The mechanism to denote the attributed elements with reference to the source provided is detailed below in Reported Identity IOC.(ISO8660).|
|Time|time.source|[DateTime](#datetime)|Time reported by a source. Some sources only report a date, which may be used here if there is no better observation.|


Harmonization types
-------------------

### Accuracy

Accuracy type. A Float between 0 and 100.


### Base64

Base64 type. Always gives unicode strings.

Sanitation encodes to base64 and accepts binary and unicode strings.


### Boolean

Boolean type. Without sanitation only python bool is accepted.

Sanitation accepts string 'true' and 'false' and integers 0 and 1.


### ClassificationType


### DateTime


### FQDN

Fully qualified domain name type.

All valid lowercase domains are accepted, no IP addresses or URLs. Trailing
dot is not allowed.


### Float

Float type. Without sanitation only python float/integer/long is
accepted. Boolean is explicitly denied.

Sanitation accepts strings and everything float() accepts.


### IPAddress

Type for IP addresses, all families. Uses the ipaddress module.

Sanitation accepts strings and objects of ipaddress.IPv4Address and ipaddress.IPv4Address.

Valid values are only strings. 0.0.0.0 is explicitly not allowed.


### IPNetwork

Type for IP networks, all families. Uses the ipaddress module.

Sanitation accepts strings and objects of ipaddress.IPv4Network and ipaddress.IPv4Network.
If host bits in strings are set, they will be ignored (e.g 127.0.0.1/32).

Valid values are only strings.


### Integer

Integer type. Without sanitation only python integer/long is accepted.
Bool is explicitly denied.

Sanitation accepts strings and everything int() accepts.


### JSON

JSON type.

Sanitation accepts pythons dictionaries and JSON strings.

Valid values are only unicode strings with JSON dictionaries.


### LowercaseString


### Registry

Registry type. Derived from UppercaseString.

Only valid values: AFRINIC, APNIC, ARIN, LACNIC, RIPE.
RIPE-NCC and RIPENCC are normalized to RIPE.


### String


### URL

URI type. Local and remote.

Sanitation converts hxxp and hxxps to http and https.
For local URIs (file) a missing host is replaced by localhost.

Valid values must have the host (network location part).


### UppercaseString



