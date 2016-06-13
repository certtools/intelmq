# -*- coding: utf-8 -*-
"""
This is a configuration File for the shadowserver parser

Mappings are "straight forward" Each Mapping is a dict
of at least three keys:
 1) required fields:
    the parser will work this keys first.
 2) optional fields:
    the parser will try to interpret these values.
    if it fails, the value is written to the extra field
 3) The classification Type of this field.
 The first value is the IntelMQ key,
the second value is the row in the shadowserver csv.

TODO: Add possibilities to convert a value

"""


def get_feed(feedname):
    # TODO to Lowercase?
    feed_idx = {
        "Botnet-Drone-Hadoop": botnet_drone_hadoop
    }

    return feed_idx.get(feedname)

def add_UTC_to_timestamp(value):
    return value + ' UTC'

botnet_drone_hadoop = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip'),
        ('source.port','port')
    ],
    'optional_fields' : [
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
        ('source.reverse_dns', 'hostname'),
        ('source.local_hostname', 'machine_name')
    ],
    'classification_type': 'botnet drone'
}

