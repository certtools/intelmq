Harmonization field names
=========================

|Section|Name|Type|Description|
|:------|:---|:---|:----------|
||comment|String|Free text commentary about the abuse event inserted by an analyst.|
|Source Geolocation|source.geolocation.latitude|Float|Latitude coordinates derived from a geolocation service, such as MaxMind geoip db.|
|Source Geolocation|source.geolocation.region|String|Some geolocation services refer to region-level geolocation.|
|Feed|feed.url|URL|The URL of a given abuse feed, where applicable|
||abuse_contact|String|Abuse contact which is relevant for this event. TODO: list?|
|Source|source.fqdn|FQDN|A DNS name related to the host from which the connection originated.|
|Source Geolocation|source.geolocation.longitude|Float|Longitude coordinates derived from a geolocation service, such as MaxMind geoip db.|
|Destination|destination.port|Integer|The port to which the connection headed.|
|Event_Description|event_description.text|String|A free-form textual description of an abuse event.|
||additional_information|String|All anecdotal information, which cannot be parsed into the data harmonization elements.|
|Malware|malware.version|String|A version string for an identified artifact generation, e.g. a crime-ware kit.|
|Protocol|protocol.application|String|e.g. vnc, ssh, sip, irc, http or p2p.|
|Destination|destination.as_name|String|The autonomous system name to which the connection headed.|
|Source|source.account|String|TODO: Description|
|Destination Geolocation|destination.geolocation.city|String|Some geolocation services refer to city-level geolocation.|
||screenshot_url|URL|Some source may report URLs related to a an image generated of a resource without any metadata. Or an URL pointing to resource, which has been rendered into a webshot, e.g. a PNG image and the relevant metadata related to its retrieval/generation.|
|Time|time.observation|DateTime|The time a source bot saw the event. This timestamp becomes especially important should you perform your own attribution on a host DNS name for example. The mechanism to denote the attributed elements with reference to the source provided is detailed below in Reported Identity IOC.(ISO8660).|
|Malware|malware.hash|String|A string depicting a checksum for a file, be it a malware sample for example.|
|Source|source.local_hostname|String|Some sources report a internal hostname within a NAT related to the name configured for a compromized system|
|Source|source.ip|IPAddress|The ip observed to initiate the connection|
|Classification|classification.taxonomy|String|We recognize the need for the CSIRT teams to apply a static (incident) taxonomy to abuse data. With this goal in mind the type IOC will serve as a basis for this activity. Each value of the dynamic type mapping translates to a an element in the static taxonomy. The European CSIRT teams for example have decided to apply the eCSIRT.net incident classification. The value of the taxonomy key is thus a derivative of the dynamic type above. For more information about check [ENISA taxonomies](http://www.enisa.europa.eu/activities/cert/support/incident-management/browsable/incident-handling-process/incident-taxonomy/existing-taxonomies).|
|Source|source.tor_node|Boolean|If the source IP was a known tor node.|
|Source|source.local_ip|IPAddress|Some sources report a internal (NATed) IP address related a compromized system. N.B. RFC1918 IPs are OK here.|
|Source Geolocation|source.geolocation.cymru_cc|String|The country code denoted for the ip by the Team Cymru asn to ip mapping service.|
||rtir_id|Integer|FRTIR incident id.|
|Destination|destination.fqdn|FQDN|A DNS name related to the host to which the connection headed.|
|Destination|destination.allocated|DateTime|Allocation date corresponding to bgp prefix.|
|Source Geolocation|source.geolocation.geoip_cc|String|MaxMind Country Code (ISO3166).|
|Destination Geolocation|destination.geolocation.latitude|Float|Latitude coordinates derived from a geolocation service, such as MaxMind geoip db.|
|Victim|victim.user_agent|String|Some feeds report the user agent string used by the host to access a malicious resource, such as a command and control server.|
|Destination|destination.ip|IPAddress|The ip observed to initiate the connection.|
|Malware|malware.name|MalwareName|A malware family name in lower case.|
|Source|source.asn|Integer|The autonomous system number from which originated the connection.|
|Feed|feed.name|String|Name for the feed, usually found in collector bot configuration.|
|Event_Description|event_description.target|String|Some sources denominate the target (organization) of a an attack.|
|Time|time.source|DateTime|Time reported by a source. Some sources only report a date, which may be used here if there is no better observation.|
|Destination Geolocation|destination.geolocation.state|String|Some geolocation services refer to state-level geolocation.|
|Source Geolocation|source.geolocation.city|String|Some geolocation services refer to city-level geolocation.|
|Destination|destination.email_address|String|An email address, which has been identified to relate to the destination of an abuse event.|
|Destination|destination.network|IPNetwork|CIDR for an autonomous system.|
|Source|source.url|URL|A URL denotes an IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
|Destination|destination.local_ip|IPAddress|Some sources report a internal (NATed) IP address related a compromized system. N.B. RFC1918 IPs are OK here.|
|Destination|destination.local_hostname|String|Some sources report a internal hostname within a NAT related to the name configured for a compromized system|
|Destination Geolocation|destination.geolocation.longitude|Float|Longitude coordinates derived from a geolocation service, such as MaxMind geoip db.|
|Destination|destination.reverse_dns|FQDN|TODO: Description|
|Source|source.port|Integer|The port from which the connection originated.|
|Source|source.network|IPNetwork|CIDR for an autonomous system.|
|Destination|destination.asn|Integer|The autonomous system number from which originated the connection.|
|Source|source.email_address|String|An email address, which has been identified to relate to the source of an abuse event.|
|Source|source.registry|String|The IP registry a given ip address is allocated by.|
|Victim Os|victim.os.name|String|Operating system name.|
|Protocol|protocol.transport|String|e.g. tcp, udp, icmp.|
|Source|source.as_name|String|The autonomous system name from which the connection originated.|
|Feed|feed.code|String|Code name for the feed, e.g.  DFGS, HSDAG etc.|
||event_hash|String|Computed event hash with specific keys and values that identify a unique event. At present, the hash should default to using the SHA1 function. Please note that for an event hash to be able to match more than one event (deduplication) the receiver of an event should calculate it based on a minimal set of keys and values present in the event. Using for example the observation time in the calculation will most likely render the checksum useless for deduplication purposes.|
||misp_ip|Integer|MISP id.|
|Source|source.reverse_dns|FQDN|Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. Record types other than PTR records may also appear in the reverse DNS tree. Furthermore, unfortunately, there is no rule prohibiting people from writing anything in a PTR record. Even Javascript will work.|
||raw|Base64|The original line of the event from encoded in base64.|
|Destination Geolocation|destination.geolocation.region|String|Some geolocation services refer to region-level geolocation.|
||status|String|Status of the malicious resource (phishing, dropzone, etc), e.g. online, offline.|
|Source Geolocation|source.geolocation.country|String|The country name derived from the ISO3166 country code (assigned to cc field).|
|Destination|destination.url|URL|A URL denotes on IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
|Destination|destination.registry|String|The IP registry a given ip address is allocated by.|
|Source Geolocation|source.geolocation.cc|String|Country Code (ISO3166) as found in source.|
|Destination|destination.tor_node|Boolean|If the destination IP was a known tor node.|
|Source|source.allocated|DateTime|Allocation date corresponding to bgp prefix.|
|Destination Geolocation|destination.geolocation.country|String|The country name derived from the ISO3166 country code (assigned to cc field).|
|Destination|destination.account|String|TODO: Description|
|Classification|classification.type|ClassificationType|The abuse type IOC is one of the most crucial pieces of information for any given abuse event. The main idea of dynamic typing is to keep our ontology flexible, since we need to evolve with the evolving threatscape of abuse data. In contrast with the static taxonomy below, the dynamic typing is used to perform business decisions in the abuse handling pipeline. Furthermore, the value data set should be kept as minimal as possible to avoid “type explosion”, which in turn dilutes the business value of the dynamic typing. In general, we normally have two types of abuse type IOC: ones referring to a compromized resource or ones referring to pieces of the criminal infrastructure, such as a command and control servers for example.|
|Victim Os|victim.os.version|String|Operating system version.|
|Source Geolocation|source.geolocation.state|String|Some geolocation services refer to state-level geolocation.|
|Event_Description|event_description.url|URL|A description URL is a link to a further description of the the abuse event in question.|


Harmonization types
-------------------


### Base64
    

    
### Boolean
    
Boolean type. Without sanitation only python bool is accepted.

Sanitation accepts string 'true' and 'false' and integers 0 and 1.


    
### ClassificationType
    

    
### DateTime
    

    
### FQDN
    

    
### Float
    
Float type. Without sanitation only python float/integer/long is
accepted. Boolean is excplicitly denied.

Sanitation accepts strings and everything float() accepts.


    
### IPAddress
    

    
### IPNetwork
    

    
### Integer
    
Integer type. Without sanitation only python integer/long is accepted.
Bool is excplicitly denied.

Sanitation accepts strings and everything int() accepts.


    
### MalwareName
    

    
### String
    

    
### URL
    

    
