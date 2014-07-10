CREATE table logentry (
   "feed" varchar(1000), 		-- Lower case name for the feeder",    e.g. abusech or phishtank.
   "feed_code" varchar(1000), 		-- Code name for the feed, e.g.  DFGS",    HSDAG etc.
   "feed_url" varchar(1000), 		-- The URL of a given abuse feed",    where applicable.
   "source_time" timestamp with time zone, -- Time reported by a source. Some sources only report a date",    which '''may''' be used here if there is no better observation.
   "observation_time" timestamp with time zone,    -- The time a source bot saw the event. This timestamp becomes especially important should you perform your own attribution on a host   inet ,     DNS name for example. The me
   "ip" inet,   			-- IPv4 or IPv6 address.
   "domain_name" varchar(1000),  	-- DNS domain name. http://en.wikipedia.org/wiki/Domain_name
   "port" integer, 			-- The port through which the abuse activity is taking place. For example a command and control server report will most likely contain a port",    which is directly related to the reported ip or host.
   "url" varchar(1000), 		-- A URL denotes on IOC, which refers to a malicious resource, whose interpretation is defined by the abuse type. A URL with the abuse type phishing refers to a phishing resource.
   "email_address" varchar(1000), 	-- An email address,    whose interpretation is based on the abuse type.
   "reverse_dns" varchar(1000),   	-- Reverse DNS name acquired through a reverse DNS query on an IP address. N.B. "Record types other than PTR records may also appear in the reverse DNS tree." http://en.wikipedia.org/wiki/Reverse_DNS_lookup
   "asn" integer, 			 -- Autonomous system number.
   "as_name" varchar(1000),    -- Registered name for an autonomous system.
   "bgp_prefix" inet,    -- A number of CIDRs for an autonomous system.
   "registry" varchar(1000),    -- The IP registry a given ip address is allocated by.
   "allocated" timestamp, 	-- coming from cymru whois
   "source_ip" inet,    -- The ip observed to initiate the connection.
   "source_port" integer,    -- The port from which the connection originated.
   "source_domain_name" varchar(1000),    -- A DNS name related to the host from which the connection originated.
   "source_email address" varchar(1000), -- An email address,  which has been identified to relate to the source of an abuse event.
   "source_asn" integer,    -- The autonomous system number from which originated the connection.
   "source_as_name" varchar(1000),    -- The autonomous system name from which the connection originated.
   "source_cc" varchar(100),    -- The country code of the ip from which the connection originated.
   "destination_ip" inet,    -- The end-point of the connection.
   "destination_port" integer,    -- The destination port of the connection.
   "destination_domain_name" varchar(1000),    -- The DNS name related to the end-point of a connection.
   "destination_email_address" varchar(1000), -- An email address,    which has been identified to relate to the destiantion of an abuse event.
   "destination_asn" integer,    -- The autonomous system number to which the connection was destined.
   "destination_as_name" varchar(1000),    -- The autonomous system name to which the connection was destined.
   "destination_cc" varchar(100),    -- The country code of the ip which was the end-point of the connection.
   "local_ip" inet,    -- Some sources report a internal (NATed) IP address related a compromized system.
   "local_hostname" varchar(1000),    -- Some sources report a internal hostname within a NAT related to the name configured for a compromized system.
   "reported_ip" inet, 		-- Should you perform your own attribution on a DNS name referred to by host,    the ip reported by the source is replaced.
   "reported_asn" integer, -- The autonomous system number related to the resource,    which was reported by the source.
   "reported_as_name" varchar(1000),    --  The autonomous system name registered to the reported asn above.
   "reported_cc" varchar(100),    -- The country codeof the reported IOC above.
   "cc" varchar(100), -- Each abuse handling pipeline,    should define a logic how to assign a value for this IOC. You may decide to trust the opinion of a single source or apply logical operations on multiple sources. The country code is expressed as an ISO 3166 two letter country code.
   "country" varchar(1000),    -- The country name derived from the ISO 3166 country code (assigned to cc above).
   "longitude" float, -- Longitude coordinates derived from a geolocation service, such as MaxMind geoip db.
   "latitude" float, -- Latitude coordinates derived from a geolocation service, such as MaxMind geoip db.
   "region" varchar(1000),    -- Some geolocation services refer to region-level geolocation (where applicable).
   "state" varchar(1000),    -- Some geolocation services refer to state-level geolocation (where applicable).
   "city" varchar(1000),    -- Some geolocation services refer to city-level geolocation.
   "description" varchar(10000),    -- A free-form textual description of an abuse event.
   "description_url" varchar(1000),    -- A description URL is a link to a further description of the the abuse event in question.
   "status" varchar(1000), -- Status of the malicious resource (phishing, dropzone, etc), e.g. online",    offline.
   "protocol" varchar(1000), -- Used for (brute forcing) bots, e.g. vnc, ssh, sip, irc, http or p2p, as well as to describe the transport protocol of a given commmand and control mechanism. N.B. the interpretation of the protocol field depends largely on the abuse type. For some abuse types, such as brute-force, this refers to the application protocol, which is the target of the brute-forcing and for botnet drones it may refer to the transport protocol of the control mechanism for example. If both protocol and transport protocol are needed,  they should be noted separately.
   "transport_protocol" varchar(1000), -- Some feeds report a protocol",    which often denotes the observed transport. This should be noted appropriately if the protocol key should denote the vulnerable service for example.
   "target" varchar(1000),    -- Some sources denominate the target (organization) of a an attack.
   "os_name" varchar(1000),    -- Operating system name.
   "os_version" varchar(1000),    -- Operating system version.
   "user_agent" varchar(1000), -- Some feeds report the user agent string used by the host to access a malicious resource, such as a command and control server.
   "additional_information" varchar(10000), -- All anecdotal information,    which cannot be parsed into the data harmonization elements.
   "missing_data" varchar(1000), -- If the sanitation is missing a known piece of data, such as a description url for example, the reference to this fact may be inserted here.
   "comment" varchar(10000),    -- Free text commentary about the abuse event inserted by an analyst.
   "screenshot_url" varchar(1000),    -- Some source may report URLs related to a an image generated of a resource without any metadata.
   "webshot_url" varchar(1000), -- A URL pointing to resource, which has been rendered into a webshot, e.g. a PNG image and the relevant metadata related to its retrieval/generation.
   "malware" varchar(1000),    -- A malware family name in lower case.
   "artifact_hash" varchar(1000), -- A string depicting a checksum for a file",    be it a malware sample for example.
   "artifact_hash_type" varchar(1000), -- The hashing algorithm used for artifact hash type above, be it MD5 or SHA-* etc. At the moment",    it seems that the hash type should default to SHA-1.
   "artifact_version" varchar(1000), -- A version string for an identified artifact generation",    e.g. a crime-ware kit.
   "abuse_contact" varchar(1000),    -- An abuse contact email address for an IP network.
   "event_hash" varchar(1000), -- Computed event hash with specific keys and values that identify a unique event. At present, the hash should default to using the SHA1 function. Please note that for an event hash to be able to match more than one event (deduplication) the receiver of an event should calculate it based on a minimal set of keys and values present in the event. Using for example the observation time in the calculation will most likely render the checksum useless for deduplication purposes.
   "shareable_key" varchar(1000),    -- Sometimes it is necessary to communicate a set of IOC which can be passed on freely to the end recipient. The most effective way to use this is to make it a multi-value within an event.
   "dns_version" varchar(1000),    -- A string describing the version of a DNS server.
   "min_amplification" varchar(1000),    -- Minimum amplification value related to an open DNS resolver.
   "notified_by" varchar(1000), -- The reporter of a given abuse event",    e.g. ZONE-H defacer attribution.
   "cymru_cc" varchar(100),    -- The country code denoted for the ip by the Team Cymru asn to ip mapping service.
   "geoip_cc" varchar(100),    -- The country code denoted for the ip by the MaxMind geoip database.
   "rtir_id" integer,    -- RTIR incident id.
   "misp_id" integer,    -- MISP id.
   "original_logline" varchar(30000), -- In case we received this event as a (CSV) log line,  we can store the original line here.
   --
   -- Type & taxonomy
   --
   "type" varchar(100), -- The abuse type IOC is one of the most crucial pieces of information for any given abuse event. The main idea of dynamic typing is to keep our ontology flexible, since we need to evolve with the evolving threatscape of abuse data. In contrast with the static taxonomy below, the dynamic typing is used to perform business decisions in the abuse handling pipeline. Furthermore, the value data set should be kept as minimal as possible to avoid "type explosion", which in turn dilutes the business value of the dynamic typing. In general, we normally have two types of abuse type IOC: ones referring to a compromized resource or ones referring to pieces of the criminal infrastructure, such as a command and control servers for example.
   "taxonomy" varchar(100) -- We recognize the need for the CSIRT teams to apply a static (incident) taxonomy to abuse data. With this goal in mind the type IOC will serve as a basis for this activity. Each value of the dynamic type mapping translates to a an element in the static taxonomy. The European CSIRT teams for example have decided to apply the eCSIRT.net incident classification. The value of the taxonomy key is thus a derivative of the dynamic type above. For more information about check [ENISA taxonomies](http://www.enisa.europa.eu/activities/cert/support/incident-management/browsable/incident-handling-process/incident-taxonomy/existing-taxonomies).
);
