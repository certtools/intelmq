|Section|Fields|Format|Description|
|:---:|:---:|:---:|:-----------:|
|Feed|feed|varchar(30)|Lower case name for the feeder, e.g. abusech or phishtank.|
|Feed|feed_code|varchar(10)|Code name for the feed, e.g.  DFGS, HSDAG etc.|
|Feed|feed_url|varchar(200)|The URL of a given abuse feed, where applicable|
|Time|source_time|timestamp with time zone|Time reported by a source. Some sources only report a date, which '''may''' be used here if there is no better observation (ISO8660)|
|Time|observation_time|timestamp with time zone|The time a source bot saw the event. This timestamp becomes especially important should you perform your own attribution on a host DNS name for example. The mechanism to denote the attributed elements with reference to the source provided is detailed below in Reported Identity IOC.(ISO8660)|
|Source Identity|source_ip|inet|The ip observed to initiate the connection|
|Source Identity|source_port|integer|The port from which the connection originated|
|Source Identity|source_domain_name|varchar(255)|A DNS name related to the host from which the connection originated|
|Source Identity|source_url|varchar(2000)|A URL denotes on IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
|Source Identity|source_email_address|varchar(200)|An email address, which has been identified to relate to the source of an abuse event|
|Source Identity|source_reverse dns|varchar(200)|Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. "Record types other than PTR records may also appear in the reverse DNS tree."|
|Source Identity|source_asn|integer|The autonomous system number from which originated the connection|
|Source Identity|source_as_name|varchar(200)|The autonomous system name from which the connection originated|
|Source Identity|source_cc|varchar(2)|The country code of the ip from which the connection originated|
|Source Identity|source_bgp_prefix|inet|CIDR for an autonomous system|
|Source Identity|source_registry|varchar(20)|The IP registry a given ip address is allocated by|
|Source Identity|source_allocated|timestamp|Allocation date corresponding to bgp prefix|
|Source Local Identity|source_local_ip|inet|Some sources report a internal (NATed) IP address related a compromized system|
|Source Local Identity|source_local_hostname|varchar(200)|Some sources report a internal hostname within a NAT related to the name configured for a compromized system|
|Source Geolocation|source_cc|varchar(2)|MaxMind Country Code (ISO3166)|
|Source Geolocation|source_country|varchar(100)|The country name derived from the ISO3166 country code (assigned to cc field)|
|Source Geolocation|source_longitude|integer|Longitude coordinates derived from a geolocation service, such as MaxMind geoip db|
|Source Geolocation|source_latitude|integer|Latitude coordinates derived from a geolocation service, such as MaxMind geoip db|
|Source Geolocation|source_region|varchar(100)|Some geolocation services refer to region-level geolocation (where applicable)|
|Source Geolocation|source_state|varchar(100)|Some geolocation services refer to state-level geolocation (where applicable)|
|Source Geolocation|source_city|varchar(100)|Some geolocation services refer to city-level geolocation|
|Source Geolocation|source_cymru_cc|varchar(2)|The country code denoted for the ip by the Team Cymru asn to ip mapping service.|
|Source Geolocation|source_geoip_cc|varchar(2)|The country code denoted for the ip by the MaxMind geoip database.|
|Destination Identity|destination_ip|inet|The ip observed to initiate the connection|
|Destination Identity|destination_port|integer|The port from which the connection originated|
|Destination Identity|destination_domain_name|varchar(255)|A DNS name related to the host from which the connection originated|
|Destination Identity|destination_url|varchar(2000)|A URL denotes on IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
|Destination Identity|destination_email_address|varchar(200)|An email address, which has been identified to relate to the source of an abuse event|
|Destination Identity|destination_reverse dns|varchar(200)|Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. "Record types other than PTR records may also appear in the reverse DNS tree."|
|Destination Identity|destination_asn|integer|The autonomous system number from which originated the connection|
|Destination Identity|destination_as_name|varchar(200)|The autonomous system name from which the connection originated|
|Destination Identity|destination_cc|varchar(2)|The country code of the ip from which the connection originated|
|Destination Identity|destination_bgp_prefix|inet|CIDR for an autonomous system|
|Destination Identity|destination_registry|varchar(20)|The IP registry a given ip address is allocated by|
|Destination Identity|destination_allocated|timestamp|Allocation date corresponding to bgp prefix|
|Destination Local Identity|destination_local_ip|inet|Some sources report a internal (NATed) IP address related a compromized system|
|Destination Local Identity|destination_local_hostname|varchar(200)|Some sources report a internal hostname within a NAT related to the name configured for a compromized system|
|Destination Geolocation|destination_cc|varchar(2)|MaxMind Country Code (ISO3166)|
|Destination Geolocation|destination_country|varchar(100)|The country name derived from the ISO3166 country code (assigned to cc field)|
|Destination Geolocation|destination_longitude|integer|Longitude coordinates derived from a geolocation service, such as MaxMind geoip db|
|Destination Geolocation|destination_latitude|integer|Latitude coordinates derived from a geolocation service, such as MaxMind geoip db|
|Destination Geolocation|destination_region|varchar(100)|Some geolocation services refer to region-level geolocation (where applicable)|
|Destination Geolocation|destination_state|varchar(100)|Some geolocation services refer to state-level geolocation (where applicable)|
|Destination Geolocation|destination_city|varchar(100)|Some geolocation services refer to city-level geolocation|
|Destination Geolocation|destination_cymru_cc|varchar(2)|The country code denoted for the ip by the Team Cymru asn to ip mapping service.|
|Destination Geolocation|destination_geoip_cc|varchar(2)|The country code denoted for the ip by the MaxMind geoip database.|
|Reported Source Identity|reported_source_ip|inet|The ip observed to initiate the connection|
|Reported Source Identity|reported_source_port|integer|The port from which the connection originated|
|Reported Source Identity|reported_source_domain_name|varchar(255)|A DNS name related to the host from which the connection originated|
|Reported Source Identity|reported_source_url|varchar(2000)|A URL denotes on IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
|Reported Source Identity|reported_source_email_address|varchar(200)|An email address, which has been identified to relate to the source of an abuse event|
|Reported Source Identity|reported_source_reverse dns|varchar(200)|Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. "Record types other than PTR records may also appear in the reverse DNS tree."|
|Reported Source Identity|reported_source_asn|integer|The autonomous system number from which originated the connection|
|Reported Source Identity|reported_source_as_name|varchar(200)|The autonomous system name from which the connection originated|
|Reported Source Identity|reported_source_cc|varchar(2)|The country code of the ip from which the connection originated|
|Reported Source Identity|reported_source_bgp_prefix|inet|CIDR for an autonomous system|
|Reported Source Identity|reported_source_registry|varchar(20)|The IP registry a given ip address is allocated by|
|Reported Source Identity|reported_source_allocated|timestamp|Allocation date corresponding to bgp prefix|
|Reported Destination Identity|reported_destination_ip|inet|The ip observed to initiate the connection|
|Reported Destination Identity|reported_destination_port|integer|The port from which the connection originated|
|Reported Destination Identity|reported_destination_domain_name|varchar(255)|A DNS name related to the host from which the connection originated|
|Reported Destination Identity|reported_destination_url|varchar(2000)|A URL denotes on IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.|
|Reported Destination Identity|reported_destination_email_address|varchar(200)|An email address, which has been identified to relate to the source of an abuse event|
|Reported Destination Identity|reported_destination_reverse dns|varchar(200)|Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. "Record types other than PTR records may also appear in the reverse DNS tree."|
|Reported Destination Identity|reported_destination_asn|integer|The autonomous system number from which originated the connection|
|Reported Destination Identity|reported_destination_as_name|varchar(200)|The autonomous system name from which the connection originated|
|Reported Destination Identity|reported_destination_cc|varchar(2)|The country code of the ip from which the connection originated|
|Reported Destination Identity|reported_destination_bgp_prefix|inet|CIDR for an autonomous system|
|Reported Destination Identity|reported_destination_registry|varchar(20)|The IP registry a given ip address is allocated by|
|Reported Destination Identity|reported_destination_allocated|timestamp|Allocation date corresponding to bgp prefix|
|Additional Fields|description|varchar(10000)| A free-form textual description of an abuse event.|
|Additional Fields|description_url|varchar(1000)| A description URL is a link to a further description of the the abuse event in question.|
|Additional Fields|status|varchar(1000)| Status of the malicious resource (phishing, dropzone, etc), e.g. online, offline.|
|Additional Fields|application_protocol|varchar(1000)|e.g. vnc, ssh, sip, irc, http or p2p.|
|Additional Fields|transport_protocol|varchar(1000)|e.g. tcp, udp, icmp|
|Additional Fields|target|varchar(1000)|Some sources denominate the target (organization) of a an attack.|
|Additional Fields|os_name|varchar(1000)|Operating system name.|
|Additional Fields|os_version|varchar(1000)|Operating system version.|
|Additional Fields|user_agent|varchar(1000)|Some feeds report the user agent string used by the host to access a malicious resource, such as a command and control server.|
|Additional Fields|additional_information|varchar(1000)|All anecdotal information, which cannot be parsed into the data harmonization elements.|
|Additional Fields|missing_data|varchar(1000)|If the sanitation is missing a known piece of data, such as a description url for example, the reference to this fact may be inserted here.|
|Additional Fields|comment|varchar(1000)|Free text commentary about the abuse event inserted by an analyst.|
|Additional Fields|screenshot_url|varchar(1000)|Some source may report URLs related to a an image generated of a resource without any metadata.|
|Additional Fields|webshot_url|varchar(1000)|A URL pointing to resource, which has been rendered into a webshot, e.g. a PNG image and the relevant metadata related to its retrieval/generation.|
|Malware Elements|malware|varchar(1000)|A malware family name in lower case.|
|Artifact Elements|artifact_hash|varchar(1000)|A string depicting a checksum for a file, be it a malware sample for example.|
|Artifact Elements|artifact_hash type|varchar(1000)|The hashing algorithm used for artifact hash type above, be it MD5 or SHA-* etc. At the moment, it seems that the hash type should default to SHA-1.|
|Artifact Elements|artifact_version|varchar(1000)|A version string for an identified artifact generation, e.g. a crime-ware kit.|
|Extra Elements|abuse_contact|varchar(1000)|An abuse contact email address for an IP network.|
|Extra Elements|event_hash|varchar(1000)|Computed event hash with specific keys and values that identify a unique event. At present, the hash should default to using the SHA1 function. Please note that for an event hash to be able to match more than one event (deduplication) the receiver of an event should calculate it based on a minimal set of keys and values present in the event. Using for example the observation time in the calculation will most likely render the checksum useless for deduplication purposes.|
|Extra Elements|shareable_key|varchar(1000)|Sometimes it is necessary to communicate a set of IOC which can be passed on freely to the end recipient. The most effective way to use this is to make it a multi-value within an event.|
|Specific Elements|rtir_id|integer|RTIR incident id.|
|Specific Elements|misp_id|integer|MISP id.|
|Specific Elements|original_logline|varchar(1000)|In case we received this event as a (CSV) log line, we can store the original line here.|
|Classification|type|varchar(1000)|The abuse type IOC is one of the most crucial pieces of information for any given abuse event. The main idea of dynamic typing is to keep our ontology flexible, since we need to evolve with the evolving threatscape of abuse data. In contrast with the static taxonomy below, the dynamic typing is used to perform business decisions in the abuse handling pipeline. Furthermore, the value data set should be kept as minimal as possible to avoid "type explosion", which in turn dilutes the business value of the dynamic typing. In general, we normally have two types of abuse type IOC: ones referring to a compromized resource or ones referring to pieces of the criminal infrastructure, such as a command and control servers for example.|
C|lassification|taxonomy|varchar(1000)|We recognize the need for the CSIRT teams to apply a static (incident) taxonomy to abuse data. With this goal in mind the type IOC will serve as a basis for this activity. Each value of the dynamic type mapping translates to a an element in the static taxonomy. The European CSIRT teams for example have decided to apply the eCSIRT.net incident classification. The value of the taxonomy key is thus a derivative of the dynamic type above. For more information about check [ENISA taxonomies](http://www.enisa.europa.eu/activities/cert/support/incident-management/browsable/incident-handling-process/incident-taxonomy/existing-taxonomies).|
