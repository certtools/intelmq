# -*- coding: utf-8 -*-
"""
This is a configuration File for the shadowserver parser

Mappings are "straight forward" each mapping is a dict
of at least three keys:
 1) required fields:
    the parser will work this keys first.
 2) optional fields:
    the parser will try to interpret these values.
    if it fails, the value is written to the extra field
 3) The classification type of this field.

 The first value is the IntelMQ key,
the second value is the row in the shadowserver csv.

TODOs:
    There is a bunch of inline todos.
    Most of them show lines of code were the mapping  has to be validated

"""


def get_feed(feedname):
    # TODO should this be case insensitive?
    feed_idx = {
        "Botnet-Drone-Hadoop": botnet_drone_hadoop,
        "Open-Memcached": open_memcached,
        "Ssl-Scan": ssl_scan,  # Aka Poodle
        "NTP-Monitor": ntp_monitor,
        "DNS-open-resolvers": dns_open_resolvers,  # TODO not yet implemented
        "Open-Elasticsearch": open_elasticsearch,  # TODO not yet implemented
        "Open-Net BIOS": open_net_bios,  # TODO not yet implemented
        "Open-Mongo DB": open_mongo_db,  # TODO not yet implemented
        "Open-MSSQL": open_mssql,  # TODO not yet implemented
        "Open-SNMP": open_snmp,  # TODO not yet implemented
        "Open-SSDP": open_ssdp,  # TODO not yet implemented
        "Open-IPMI": open_ipmi,  # TODO not yet implemented
        "Open-Portmapper": open_portmapper,  # TODO not yet implemented
        "Open-Redis": open_redis,  # TODO not yet implemented
        "Microsoft-Sinkhole": microsoft_sinkhole,  # TODO not yet implemented
        "Open-TFTP": open_tftp,  # TODO not yet implemented
        "Open-Chargen": open_chargen,  # TODO not yet implemented
        "Sinkhole-HTTP-Drone": sinkhole-http-drone,  # TODO not yet implemented
        "Open-m DNS": open_m_dns,  # TODO not yet implemented
    }

    return feed_idx.get(feedname)


def add_UTC_to_timestamp(value):
    return value + ' UTC'

# https://www.shadowserver.org/wiki/pmwiki.php/Services/NTP-Monitor
ntp_monitor = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),  # TODO
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
    ],
    'classification_type': 'exploit'  # TODO
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Ssl-Scan
ssl_scan = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),  # TODO
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
    ],
    'classification_type': 'vulnerable service'
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Memcached
open_memcached = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),  # TODO
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
    ],
    'classification_type': 'vulnerable service'
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Botnet-Drone-Hadoop
botnet_drone_hadoop = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port', 'port')
    ],
    'optional_fields': [
        ('destination.asn', 'cc_asn'),
        ('destination.geolocation.cc', 'cc_geo'),
        ('destination.ip', 'cc_ip'),
        ('destination.port', 'cc_port'),
        ('destination.fqdn', 'cc_dns'),
        ('destination.url', 'url'),
        ('malware.name', 'infection'),
        ('protocol.application', 'application'),
        ('protocol.transport', 'type'),
        ('source.asn', 'asn'),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.reverse_dns', 'hostname'),  # TODO
        ('source.local_hostname', 'machine_name')
    ],
    'classification_type': 'botnet drone'
}
