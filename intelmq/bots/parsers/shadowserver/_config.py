# SPDX-FileCopyrightText: 2016-2018 by Bundesamt für Sicherheit in der Informationstechnik (BSI)
#
# SPDX-License-Identifier: AGPL-3.0-or-later
# -*- coding: utf-8 -*-
"""
Copyright (c)2016-2018 by Bundesamt für Sicherheit in der Informationstechnik (BSI)

Software engineering by BSI & Intevation GmbH

This is a configuration File for the shadowserver parser

In the following, *intelmqkey* are arbitrary keys from intelmq's harmonization
and *shadowkey* is a column name from shadowserver's data.

Every bot-type is defined by a dictionary with three values:
- `required_fields`: A list of tuples containing intelmq's field name, field
  name from data and an optional conversion function. Errors are raised, if the
  field does not exists in data.
- `optional_fields`: Same format as above, but does not raise errors if the
  field does not exist. If there's no mapping to an intelmq field, you can set
  the intelmqkey to `extra.` and the field will be added to the extra field
  using the original field name. See section below for possible tuple-values.
- `constant_fields`: A dictionary with a static mapping of field name to data,
  e.g. to set classifications or protocols.

The tuples can be of following format:

- `('intelmqkey', 'shadowkey')`, the data from the column *shadowkey* will be
  saved in the event's field *intelmqkey*. Logically equivalent to:
  `event[`*intelmqkey*`] = row[`*shadowkey*`]`.
- `('intelmqkey', 'shadowkey', conversion_function)`, the given function will be
  used to convert and/or validate the data. Logically equivalent to:
  `event[`*intelmqkey*`] = conversion_function(row[`*shadowkey*`)]`.
- `('intelmqkey', 'shadowkey', conversion_function, True)`, the function gets
  two parameters here, the second one is the full row (as dictionary). Logically
  equivalent to:
  `event[`*intelmqkey*`] = conversion_function(row[`*shadowkey*`, row)]`.
- `('extra.', 'shadowkey', conversion_function)`, the data will be added to
  extra in this case, the resulting name is `extra.[shadowkey]`. The
  `conversion_function` is optional. Logically equivalent to:
  `event[extra.`*intelmqkey*`] = conversion_function(row[`*shadowkey*`)]`.
- `(False, 'shadowkey')`, the column will be ignored.

Mappings are "straight forward" each mapping is a dict
of at least three keys:

1. required fields:
   the parser will work this keys first.
2. optional fields:
   the parser will try to interpret these values.
   if it fails, the value is written to the extra field
3. constant fields:
   Some information about an event may not be explicitly stated in a
   feed because it is implicit in the nature of the feed. For instance
   a feed that is exclusively about HTTP may not have a field for the
   protocol because it's always TCP.

The first value is the IntelMQ key,
the second value is the row in the shadowserver csv.

Reference material:
    * when setting the classification.* fields,
      please use the taxonomy from the Data Harmonization
      :ref:`data format classification`
      or upstream from https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/
    * please respect the Data format ontology: :doc:`/dev/data-format`


TODOs:
    There is a bunch of inline todos.
    Most of them show lines of code were the mapping has to be validated

    @ Check-Implementation Tags for parser configs.
    dmth thinks it's not sufficient. Some CERT-Expertise is needed to
    check if the mappings are correct.

    feed_idx is not complete.

"""
import re
import base64
import binascii
from typing import Optional, Dict, Tuple, Any

import intelmq.lib.harmonization as harmonization


def get_feed_by_feedname(given_feedname: str) -> Optional[Dict[str, Any]]:
    return feedname_mapping.get(given_feedname, None)


def get_feed_by_filename(given_filename: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    return filename_mapping.get(given_filename, None)


def add_UTC_to_timestamp(value: str) -> str:
    return value + ' UTC'


def convert_bool(value: str) -> Optional[bool]:
    value = value.lower()
    if value in {'y', 'yes', 'true', 'enabled', '1'}:
        return True
    elif value in {'n', 'no', 'false', 'disabled', '0'}:
        return False

    return None


def validate_to_none(value: str) -> Optional[str]:
    return None if (not value or value in {'0', 'unknown'}) else value


def convert_int(value: str) -> Optional[int]:
    """ Returns an int or None for empty strings. """
    return int(value) if value else None


def convert_float(value: str) -> Optional[float]:
    """ Returns an float or None for empty strings. """
    return float(value) if value else None


def convert_http_host_and_url(value: str, row: Dict[str, str]) -> str:
    """
    URLs are split into hostname and path. The column names differ in reports.
    Compromised-Website: http_host, url
    Drone: cc_dns, url
    IPv6-Sinkhole-HTTP-Drone: http_host, http_url
    Microsoft-Sinkhole: http_host, url
    Sinkhole-HTTP-Drone: http_host, url
    With some reports, url/http_url holds only the path, with others the full HTTP request.
    """
    if "cc_dns" in row:
        hostname = row.get('cc_dns', '')
    elif "http_host" in row:
        hostname = row.get('http_host', '')
    else:
        hostname = ''

    if "url" in row:
        path = row.get('url', '')
    elif "http_url" in row:
        path = row.get('http_url', '')
    else:
        path = ''

    if hostname and path:
        # remove potential leading/trailing HTTP request information
        path = re.sub(r'^[^/]*', '', path)
        path = re.sub(r'\s.*$', '', path)

        if "application" in row and row['application'] in {'http', 'https'}:
            application = row['application']
        else:
            application = 'http'

        return application + "://" + hostname + path

    return value


def invalidate_zero(value: str) -> Optional[int]:
    """ Returns an int or None for empty strings or '0'. """
    return int(value) if value and int(value) != 0 else None


# TODO this function is a wild guess...
def set_tor_node(value: str) -> Optional[bool]:
    return True if value else None


def validate_ip(value: str) -> Optional[str]:
    """Remove "invalid" IP."""
    # FIX: https://github.com/certtools/intelmq/issues/1720 # TODO: Find better fix
    if not (value == '0.0.0.0' or '/' in value) and harmonization.IPAddress.is_valid(value, sanitize=True):
        return value

    return None


def validate_network(value: str) -> Optional[str]:
    # FIX: https://github.com/certtools/intelmq/issues/1720 # TODO: Find better fix
    if '/' in value and harmonization.IPNetwork.is_valid(value, sanitize=True):
        return value

    return None


def validate_fqdn(value: str) -> Optional[str]:
    if value and harmonization.FQDN.is_valid(value, sanitize=True):
        return value

    return None


def convert_date(value: str) -> Optional[str]:
    return harmonization.DateTime.sanitize(value)


def convert_date_utc(value: str) -> Optional[str]:
    """
    Parses a datetime from the value and assumes UTC by appending the TZ to the value.
    Not the same as add_UTC_to_timestamp, as convert_date_utc also does the sanitiation
    """
    return harmonization.DateTime.sanitize(value + '+00:00')


def force_base64(value: Optional[str]) -> Optional[str]:
    """
    Takes input strings that may be either base64-encoded bytestrings or plaintext string,
    and leaves the base64-encoded values untouched while encoding the non-encoded values,
    uniformly converting the data in the field to be base64-encoded
    """
    if not value:
        return None

    try:
        base64.b64decode(value, validate=True)  # return value intentionally ignored
    except binascii.Error:
        return base64.b64encode(value.encode()).decode()
    else:
        return value


def scan_exchange_taxonomy(field):
    if field == 'exchange;webshell':
        return 'intrusions'
    return 'vulnerable'


def scan_exchange_type(field):
    if field == 'exchange;webshell':
        return 'system-compromise'
    return 'infected-system'


def scan_exchange_identifier(field):
    if field == 'exchange;webshell':
        return 'exchange-server-webshell'
    return 'vulnerable-exchange-server'


# BEGIN CONFGEN

# https://www.shadowserver.org/what-we-do/network-reporting/blocklist-report/
blocklist = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
    ],
    'optional_fields': [
        ('source.network', 'ip', validate_network),
        ('extra.', 'tag', validate_to_none),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'source', validate_to_none),
        ('extra.', 'reason', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.identifier': 'blacklisted-ip',
        'classification.taxonomy': 'other',
        'classification.type': 'blacklist',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/compromised-website-report/
compromised_website = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.application', 'application', validate_to_none),
        ('source.url', 'url', convert_http_host_and_url, True),
        ('source.fqdn', 'http_host', validate_fqdn),
        ('source.reverse_dns', 'hostname'),
        ('malware.name', 'tag'),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('event_description.text', 'category', validate_to_none),
        ('extra.', 'system', validate_to_none),
        ('extra.', 'detected_since', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'redirect_target', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'cc_url', validate_to_none),
        ('extra.', 'family', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'intrusions',
        'classification.type': 'system-compromise',
        'classification.identifier': 'compromised-website',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/device-identification-report/
device_id = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'undetermined',
        'classification.identifier': 'device-id',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/ddos-participant-report/
event_ddos_participant = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip', validate_ip),
        ('source.port', 'src_port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'duration', convert_int),
        ('extra.', 'attack_src_port', convert_int),
        ('extra.', 'http_usessl', convert_bool),
        ('extra.', 'ip_header_seqnum', convert_int),
        ('extra.', 'ip_header_ttl', convert_int),
        ('extra.', 'number_of_connections', convert_int),
        ('extra.', 'packet_length', convert_int),
        ('extra.', 'packet_randomized', convert_bool),
        ('extra.', 'tag', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('source.reverse_dns', 'src_hostname'),
        ('extra.source.naics', 'src_naics', invalidate_zero),
        ('extra.source.sector', 'src_sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', invalidate_zero),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.geolocation.city', 'dst_city'),
        ('destination.reverse_dns', 'dst_hostname', validate_to_none),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'domain_source', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('malware.name', 'infection'),
        ('extra.', 'family', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'event_id', validate_to_none),
        ('extra.', 'dst_network', validate_to_none),
        ('extra.', 'dst_netmask', validate_to_none),
        ('extra.', 'attack', validate_to_none),
        ('extra.', 'attack_src_ip', validate_to_none),
        ('extra.', 'domain', validate_to_none),
        ('extra.', 'domain_transaction_id', validate_to_none),
        ('extra.', 'gcip', validate_to_none),
        ('extra.', 'http_method', validate_to_none),
        ('extra.', 'http_path', validate_to_none),
        ('extra.', 'http_postdata', validate_to_none),
        ('extra.', 'ip_header_ack', validate_to_none),
        ('extra.', 'ip_header_acknum', validate_to_none),
        ('extra.', 'ip_header_dont_fragment', validate_to_none),
        ('extra.', 'ip_header_fin', validate_to_none),
        ('extra.', 'ip_header_identity', validate_to_none),
        ('extra.', 'ip_header_psh', validate_to_none),
        ('extra.', 'ip_header_rst', validate_to_none),
        ('extra.', 'ip_header_syn', validate_to_none),
        ('extra.', 'ip_header_tos', validate_to_none),
        ('extra.', 'ip_header_urg', validate_to_none),
        ('extra.', 'http_agent', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'availability',
        'classification.type': 'ddos',
        'classification.identifier': 'ddos-participant',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/honeypot-brute-force-events-report/
event_honeypot_brute_force = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip', validate_ip),
        ('source.port', 'src_port', convert_int),
    ],
    'optional_fields': [
        ('classification.identifier', 'application'),
        ('destination.account', 'username', validate_to_none),
        ('extra.', 'tag', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('source.reverse_dns', 'src_hostname'),
        ('extra.source.naics', 'src_naics', invalidate_zero),
        ('extra.source.sector', 'src_sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', invalidate_zero),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.geolocation.city', 'dst_city'),
        ('destination.reverse_dns', 'dst_hostname', validate_to_none),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('malware.name', 'infection'),
        ('extra.', 'family', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'event_id', validate_to_none),
        ('extra.', 'service', validate_to_none),
        ('extra.', 'start_time', convert_date_utc),
        ('extra.', 'end_time', convert_date_utc),
        ('extra.', 'client_version', validate_to_none),
        ('extra.', 'password', validate_to_none),
        ('extra.', 'payload_url', validate_to_none),
        ('extra.', 'payload_md5', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'intrusion-attempts',
        'classification.type': 'brute-force',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/honeypot-darknet-events-report/
event_honeypot_darknet = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip', validate_ip),
        ('source.port', 'src_port', convert_int),
    ],
    'optional_fields': [
        ('classification.identifier', 'tag', validate_to_none),
        ('extra.', 'tag', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('source.reverse_dns', 'src_hostname'),
        ('extra.source.naics', 'src_naics', invalidate_zero),
        ('extra.source.sector', 'src_sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', invalidate_zero),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.geolocation.city', 'dst_city'),
        ('destination.reverse_dns', 'dst_hostname', validate_to_none),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('malware.name', 'infection'),
        ('extra.', 'family', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'event_id', validate_to_none),
        ('extra.', 'count', convert_int),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/honeypot-ddos-events/
event_honeypot_ddos = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip', validate_ip),
        ('source.port', 'src_port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'duration', convert_int),
        ('extra.', 'attack_src_port', convert_int),
        ('extra.', 'http_usessl', convert_bool),
        ('extra.', 'ip_header_seqnum', convert_int),
        ('extra.', 'ip_header_ttl', convert_int),
        ('extra.', 'number_of_connections', convert_int),
        ('extra.', 'packet_length', convert_int),
        ('extra.', 'packet_randomized', convert_bool),
        ('extra.', 'tag', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('source.reverse_dns', 'src_hostname'),
        ('extra.source.naics', 'src_naics', invalidate_zero),
        ('extra.source.sector', 'src_sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', invalidate_zero),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.geolocation.city', 'dst_city'),
        ('destination.reverse_dns', 'dst_hostname', validate_to_none),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'domain_source', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('malware.name', 'infection'),
        ('extra.', 'family', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'event_id', validate_to_none),
        ('extra.', 'dst_network', validate_to_none),
        ('extra.', 'dst_netmask', validate_to_none),
        ('extra.', 'attack', validate_to_none),
        ('extra.', 'attack_src_ip', validate_to_none),
        ('extra.', 'domain', validate_to_none),
        ('extra.', 'domain_transaction_id', validate_to_none),
        ('extra.', 'gcip', validate_to_none),
        ('extra.', 'http_method', validate_to_none),
        ('extra.', 'http_path', validate_to_none),
        ('extra.', 'http_postdata', validate_to_none),
        ('extra.', 'ip_header_ack', validate_to_none),
        ('extra.', 'ip_header_acknum', validate_to_none),
        ('extra.', 'ip_header_dont_fragment', validate_to_none),
        ('extra.', 'ip_header_fin', validate_to_none),
        ('extra.', 'ip_header_identity', validate_to_none),
        ('extra.', 'ip_header_psh', validate_to_none),
        ('extra.', 'ip_header_rst', validate_to_none),
        ('extra.', 'ip_header_syn', validate_to_none),
        ('extra.', 'ip_header_tos', validate_to_none),
        ('extra.', 'ip_header_urg', validate_to_none),
        ('extra.', 'http_agent', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'availability',
        'classification.type': 'ddos',
        'classification.identifier': 'honeypot-ddos',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/honeypot-amplification-ddos-events-report/
event_honeypot_ddos_amp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip', validate_ip),
        ('source.port', 'src_port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'avg_pps', convert_float),
        ('extra.', 'max_pps', convert_float),
        ('extra.', 'tag', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('source.reverse_dns', 'src_hostname'),
        ('extra.source.naics', 'src_naics', invalidate_zero),
        ('extra.source.sector', 'src_sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', invalidate_zero),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.geolocation.city', 'dst_city'),
        ('destination.reverse_dns', 'dst_hostname', validate_to_none),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('malware.name', 'infection'),
        ('extra.', 'family', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'event_id', validate_to_none),
        ('extra.', 'request', validate_to_none),
        ('extra.', 'count', convert_int),
        ('extra.', 'bytes', convert_int),
        ('extra.', 'end_time', convert_date_utc),
        ('extra.', 'duration', convert_int),
    ],
    'constant_fields': {
        'classification.identifier': 'amplification-ddos-victim',
        'classification.taxonomy': 'availability',
        'classification.type': 'ddos',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/honeypot-ddos-target-events-report/
event_honeypot_ddos_target = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip', validate_ip),
        ('source.port', 'src_port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'attack_src_port', convert_int),
        ('extra.', 'http_usessl', convert_bool),
        ('extra.', 'ip_header_seqnum', convert_int),
        ('extra.', 'ip_header_ttl', convert_int),
        ('extra.', 'number_of_connections', convert_int),
        ('extra.', 'packet_length', convert_int),
        ('extra.', 'packet_randomized', convert_bool),
        ('extra.', 'tag', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', invalidate_zero),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.geolocation.city', 'dst_city'),
        ('destination.reverse_dns', 'dst_hostname', validate_to_none),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('source.reverse_dns', 'src_hostname'),
        ('extra.source.naics', 'src_naics', invalidate_zero),
        ('extra.source.sector', 'src_sector', validate_to_none),
        ('extra.', 'domain_source', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('malware.name', 'infection'),
        ('extra.', 'family', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'event_id', validate_to_none),
        ('extra.', 'dst_network', validate_to_none),
        ('extra.', 'dst_netmask', validate_to_none),
        ('extra.', 'attack', validate_to_none),
        ('extra.', 'duration', convert_int),
        ('extra.', 'attack_src_ip', validate_to_none),
        ('extra.', 'domain', validate_to_none),
        ('extra.', 'domain_transaction_id', validate_to_none),
        ('extra.', 'gcip', validate_to_none),
        ('extra.', 'http_method', validate_to_none),
        ('extra.', 'http_path', validate_to_none),
        ('extra.', 'http_postdata', validate_to_none),
        ('extra.', 'ip_header_ack', validate_to_none),
        ('extra.', 'ip_header_acknum', validate_to_none),
        ('extra.', 'ip_header_dont_fragment', validate_to_none),
        ('extra.', 'ip_header_fin', validate_to_none),
        ('extra.', 'ip_header_identity', validate_to_none),
        ('extra.', 'ip_header_psh', validate_to_none),
        ('extra.', 'ip_header_rst', validate_to_none),
        ('extra.', 'ip_header_syn', validate_to_none),
        ('extra.', 'ip_header_tos', validate_to_none),
        ('extra.', 'ip_header_urg', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'availability',
        'classification.type': 'ddos',
        'classification.identifier': 'honeypot-ddos-target',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/honeypot-http-scanner-events/
event_honeypot_http_scan = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip', validate_ip),
        ('source.port', 'src_port', convert_int),
    ],
    'optional_fields': [
        ('user_agent', 'http_agent', validate_to_none),
        ('extra.method', 'http_request_method', validate_to_none),
        ('extra.', 'tag', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('source.reverse_dns', 'src_hostname'),
        ('extra.source.naics', 'src_naics', invalidate_zero),
        ('extra.source.sector', 'src_sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', invalidate_zero),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.geolocation.city', 'dst_city'),
        ('destination.reverse_dns', 'dst_hostname', validate_to_none),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('malware.name', 'infection'),
        ('extra.', 'family', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'event_id', validate_to_none),
        ('extra.', 'pattern', validate_to_none),
        ('destination.url', 'http_url', convert_http_host_and_url, True),
        ('extra.', 'url_scheme', validate_to_none),
        ('extra.', 'session_tags', validate_to_none),
        ('extra.', 'vulnerability_enum', validate_to_none),
        ('extra.', 'vulnerability_id', validate_to_none),
        ('extra.', 'vulnerability_class', validate_to_none),
        ('extra.', 'vulnerability_score', validate_to_none),
        ('extra.', 'vulnerability_severity', validate_to_none),
        ('extra.', 'vulnerability_version', validate_to_none),
        ('extra.', 'threat_framework', validate_to_none),
        ('extra.', 'threat_tactic_id', validate_to_none),
        ('extra.', 'threat_technique_id', validate_to_none),
        ('extra.', 'target_vendor', validate_to_none),
        ('extra.', 'target_product', validate_to_none),
        ('extra.', 'target_class', validate_to_none),
        ('extra.', 'file_md5', validate_to_none),
        ('extra.', 'file_sha256', validate_to_none),
        ('extra.', 'request_raw', force_base64),
        ('extra.', 'body_raw', force_base64),
    ],
    'constant_fields': {
        'classification.taxonomy': 'information-gathering',
        'classification.type': 'scanner',
        'protocol.application': 'http',
        'classification.identifier': 'honeypot-http-scan',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/honeypot-ics-scanner-events-report/
event_honeypot_ics_scan = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip', validate_ip),
        ('source.port', 'src_port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'tag', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('source.reverse_dns', 'src_hostname'),
        ('extra.source.naics', 'src_naics', invalidate_zero),
        ('extra.source.sector', 'src_sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', invalidate_zero),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.geolocation.city', 'dst_city'),
        ('destination.reverse_dns', 'dst_hostname', validate_to_none),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('malware.name', 'infection'),
        ('extra.', 'family', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'event_id', validate_to_none),
        ('extra.', 'state', validate_to_none),
        ('extra.', 'sensor_id', validate_to_none),
        ('extra.', 'slave_id', validate_to_none),
        ('extra.', 'function_code', validate_to_none),
        ('extra.', 'request', validate_to_none),
        ('extra.', 'response', validate_to_none),
    ],
    'constant_fields': {
        'classification.identifier': 'ics',
        'classification.taxonomy': 'information-gathering',
        'classification.type': 'scanner',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/ip-spoofer-events-report/
event_ip_spoofer = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip', validate_ip),
        ('source.port', 'src_port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'infection', validate_to_none),
        ('source.network', 'network', validate_network),
        ('extra.', 'tag', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('source.reverse_dns', 'src_hostname'),
        ('extra.source.naics', 'src_naics', invalidate_zero),
        ('extra.source.sector', 'src_sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', invalidate_zero),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.geolocation.city', 'dst_city'),
        ('destination.reverse_dns', 'dst_hostname', validate_to_none),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('extra.', 'family', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'event_id', validate_to_none),
        ('extra.', 'routedspoof', validate_to_none),
        ('extra.', 'session', validate_to_none),
        ('extra.', 'nat', convert_bool),
    ],
    'constant_fields': {
        'classification.taxonomy': 'fraud',
        'classification.type': 'masquerade',
        'classification.identifier': 'ip-spoofer',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/sinkhole-events-report/
event_sinkhole = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip', validate_ip),
        ('source.port', 'src_port', convert_int),
    ],
    'optional_fields': [
        ('classification.identifier', 'infection', validate_to_none),
        ('malware.name', 'family', validate_to_none),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'infection', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('source.reverse_dns', 'src_hostname'),
        ('extra.source.naics', 'src_naics', invalidate_zero),
        ('extra.source.sector', 'src_sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', invalidate_zero),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.geolocation.city', 'dst_city'),
        ('destination.reverse_dns', 'dst_hostname', validate_to_none),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'event_id', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'malicious-code',
        'classification.type': 'infected-system',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/sinkhole-dns-events-report/
event_sinkhole_dns = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip', validate_ip),
        ('source.port', 'src_port', convert_int),
    ],
    'optional_fields': [
        ('extra.naics', 'src_naics', invalidate_zero),
        ('extra.sector', 'src_sector', validate_to_none),
        ('extra.dns_query_type', 'query_type'),
        ('extra.dns_query', 'query'),
        ('malware.name', 'family', validate_to_none),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'infection', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('source.reverse_dns', 'src_hostname'),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('extra.', 'count', convert_int),
    ],
    'constant_fields': {
        'classification.identifier': 'sinkholedns',
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'protocol.application': 'dns',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/sinkhole-http-events-report/
event_sinkhole_http = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'src_ip', validate_ip),
        ('source.port', 'src_port', convert_int),
    ],
    'optional_fields': [
        ('classification.identifier', 'tag'),
        ('malware.name', 'family', validate_to_none),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'infection', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('source.reverse_dns', 'src_hostname'),
        ('extra.source.naics', 'src_naics', invalidate_zero),
        ('extra.source.sector', 'src_sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', invalidate_zero),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.geolocation.city', 'dst_city'),
        ('destination.reverse_dns', 'dst_hostname', validate_to_none),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'event_id', validate_to_none),
        ('destination.url', 'http_url', convert_http_host_and_url, True),
        ('destination.fqdn', 'http_host', validate_fqdn),
        ('extra.', 'http_agent', validate_to_none),
        ('extra.', 'forwarded_by', validate_to_none),
        ('extra.', 'ssl_cipher', validate_to_none),
        ('extra.', 'http_referer', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'malicious-code',
        'classification.type': 'infected-system',
        'protocol.application': 'http',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/sinkhole-http-referer-events-report/
event_sinkhole_http_referer = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
    ],
    'optional_fields': [
        ('malware.name', 'family', validate_to_none),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'infection', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('extra.', 'http_referer_ip', validate_ip),
        ('extra.', 'http_referer_port', convert_int),
        ('extra.', 'http_referer_asn', invalidate_zero),
        ('extra.', 'http_referer_geo', validate_to_none),
        ('extra.', 'http_referer_region', validate_to_none),
        ('extra.', 'http_referer_city', validate_to_none),
        ('extra.', 'http_referer_hostname', validate_to_none),
        ('extra.', 'http_referer_naics', invalidate_zero),
        ('extra.', 'http_referer_sector', validate_to_none),
        ('destination.ip', 'dst_ip', validate_ip),
        ('destination.port', 'dst_port', convert_int),
        ('destination.asn', 'dst_asn', invalidate_zero),
        ('destination.geolocation.cc', 'dst_geo'),
        ('destination.geolocation.region', 'dst_region'),
        ('destination.geolocation.city', 'dst_city'),
        ('destination.reverse_dns', 'dst_hostname', validate_to_none),
        ('extra.destination.naics', 'dst_naics', invalidate_zero),
        ('extra.destination.sector', 'dst_sector', validate_to_none),
        ('extra.', 'public_source', validate_to_none),
        ('extra.', 'application', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'event_id', validate_to_none),
        ('destination.url', 'http_url', convert_http_host_and_url, True),
        ('destination.fqdn', 'http_host', validate_fqdn),
        ('extra.', 'http_referer', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'classification.identifier': 'sinkhole-http-referer',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/malware-url-report/
malware_url = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
    ],
    'optional_fields': [
        ('source.url', 'url', convert_http_host_and_url, True),
        ('source.fqdn', 'host', validate_fqdn),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('malware.name', 'tag'),
        ('extra.', 'source', validate_to_none),
        ('malware.hash.sha256', 'sha256', validate_to_none),
        ('extra.', 'application', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'malicious-code',
        'classification.type': 'malware-distribution',
        'classification.identifier': 'malware-url',
    },
}

phish_url = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
    ],
    'optional_fields': [
        ('source.url', 'url', convert_http_host_and_url, True),
        ('source.fqdn', 'host', validate_fqdn),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'source', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'fraud',
        'classification.type': 'phishing',
        'classification.identifier': 'phish-url',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-http-proxy-report/
population_http_proxy = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('malware.name', 'tag'),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.', 'http', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'connection', validate_to_none),
        ('extra.', 'proxy_authenticate', validate_to_none),
        ('extra.', 'via', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'content_length', convert_int),
        ('extra.', 'transfer_encoding', validate_to_none),
        ('extra.', 'http_date', convert_date),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-http-proxy',
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'protocol.application': 'http',
    },
}

# http://www.shadowserver.org/wiki/pmwiki.php/Services/Sandbox-Connection
sandbox_conn = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('destination.fqdn', 'host', validate_fqdn),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('malware.hash.md5', 'md5', validate_to_none),
        ('protocol.transport', 'protocol'),
        ('extra.', 'bytes_in', validate_to_none),
        ('extra.', 'bytes_out', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'malicious-code',
        'classification.type': 'malware-distribution',
        'classification.identifier': 'sandbox-conn',
    },
}

sandbox_dns = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
    ],
    'optional_fields': [
        ('extra.dns_query_type', 'type', validate_to_none),
        ('malware.hash.md5', 'md5hash', validate_to_none),
        ('extra.', 'request', validate_to_none),
        ('extra.', 'response', validate_to_none),
        ('extra.', 'family', validate_to_none),
        ('malware.name', 'tag'),
        ('extra.', 'source', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'protocol.application': 'dns',
        'classification.identifier': 'sandbox-dns',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/sandbox-url-report/
sandbox_url = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
    ],
    'optional_fields': [
        ('destination.fqdn', 'host', validate_fqdn),
        ('extra.http_request_method', 'method', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('malware.hash.md5', 'md5', validate_to_none),
        ('destination.url', 'url', convert_http_host_and_url, True),
        ('user_agent', 'user_agent', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'malicious-code',
        'classification.type': 'malware-distribution',
        'classification.identifier': 'sandbox-url',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-adb-report/
scan_adb = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'name', validate_to_none),
        ('extra.', 'model', validate_to_none),
        ('extra.', 'device', validate_to_none),
        ('extra.', 'features', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('extra.', 'device_version', validate_to_none),
        ('extra.', 'device_sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-adb',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'adb',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-afp-report/
scan_afp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'machine_type', validate_to_none),
        ('extra.', 'afp_versions', validate_to_none),
        ('extra.', 'uams', validate_to_none),
        ('extra.', 'flags', validate_to_none),
        ('extra.', 'server_name', validate_to_none),
        ('extra.', 'signature', validate_to_none),
        ('extra.', 'directory_service', validate_to_none),
        ('extra.', 'utf8_servername', validate_to_none),
        ('extra.', 'network_address', validate_to_none),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-afp',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'afp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-amqp-report/
scan_amqp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'channel', validate_to_none),
        ('extra.', 'message_length', convert_int),
        ('extra.', 'class', validate_to_none),
        ('extra.', 'method', validate_to_none),
        ('extra.', 'version_major', validate_to_none),
        ('extra.', 'version_minor', validate_to_none),
        ('extra.', 'capabilities', validate_to_none),
        ('extra.', 'cluster_name', validate_to_none),
        ('extra.', 'platform', validate_to_none),
        ('extra.', 'product', validate_to_none),
        ('extra.', 'product_version', validate_to_none),
        ('extra.', 'mechanisms', validate_to_none),
        ('extra.', 'locales', validate_to_none),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-amqp',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'amqp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-apple-remote-desktop-ard-report/
scan_ard = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'machine_name', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-ard',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-chargen-report/
scan_chargen = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.response_size', 'size', convert_int),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'chargen',
        'classification.identifier': 'open-chargen',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-cisco-smart-install-report/
scan_cisco_smart_install = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-cisco-smart-install',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'cisco-smart-install',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-coap-report/
scan_coap = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'response', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-coap',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'coap',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-couchdb-report/
scan_couchdb = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'server_version', validate_to_none),
        ('extra.', 'couchdb_message', validate_to_none),
        ('extra.', 'couchdb_version', validate_to_none),
        ('extra.', 'git_sha', validate_to_none),
        ('extra.', 'features', validate_to_none),
        ('extra.', 'vendor', validate_to_none),
        ('extra.', 'visible_databases', validate_to_none),
        ('extra.', 'error', validate_to_none),
        ('extra.', 'error_reason', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'protocol.application': 'CouchDB',
        'classification.identifier': 'open-couchdb',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-cwmp-report/
scan_cwmp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'http', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'connection', validate_to_none),
        ('extra.', 'www_authenticate', validate_to_none),
        ('extra.', 'set_cookie', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'content_length', convert_int),
        ('extra.', 'transfer_encoding', validate_to_none),
        ('extra.', 'date', validate_to_none),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'cwmp',
        'classification.identifier': 'open-cwmp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-db2-discovery-service-report/
scan_db2 = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'size', convert_int),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'db2_hostname', validate_to_none),
        ('extra.', 'servername', validate_to_none),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.identifier': 'open-db2-discovery-service',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'db2',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/vulnerable-ddos-middlebox-report/
scan_ddos_middlebox = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.application', 'tag'),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'source_port', validate_to_none),
        ('extra.', 'bytes', convert_int),
        ('extra.', 'amplification', convert_float),
        ('extra.', 'method', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'classification.identifier': 'open-ddos-middlebox',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/dns-open-resolvers-report/
scan_dns = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'min_amplification', convert_float),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'dns_version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.identifier': 'dns-open-resolver',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'dns',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-docker-service-report/
scan_docker = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'http', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'date', validate_to_none),
        ('extra.', 'experimental', validate_to_none),
        ('extra.', 'api_version', validate_to_none),
        ('extra.', 'arch', validate_to_none),
        ('extra.', 'go_version', validate_to_none),
        ('extra.os.name', 'os', validate_to_none),
        ('extra.', 'kernel_version', validate_to_none),
        ('extra.', 'git_commit', validate_to_none),
        ('extra.', 'min_api_version', validate_to_none),
        ('extra.', 'build_time', validate_to_none),
        ('extra.', 'pkg_version', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'docker',
        'classification.identifier': 'open-docker',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-dvr-dhcpdiscover-report/
scan_dvr_dhcpdiscover = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.application', 'tag'),
        ('extra.', 'video_input_channels', convert_int),
        ('extra.', 'alarm_input_channels', convert_int),
        ('extra.', 'video_output_channels', convert_int),
        ('extra.', 'alarm_output_channels', convert_int),
        ('extra.', 'remote_video_input_channels', convert_int),
        ('extra.', 'ipv4_dhcp_enable', convert_bool),
        ('extra.', 'ipv6_dhcp_enable', convert_bool),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('extra.', 'device_version', validate_to_none),
        ('extra.', 'device_id', validate_to_none),
        ('extra.', 'device_serial', validate_to_none),
        ('extra.', 'machine_name', validate_to_none),
        ('extra.', 'manufacturer', validate_to_none),
        ('extra.', 'method', validate_to_none),
        ('extra.', 'http_port', convert_int),
        ('extra.', 'internal_port', convert_int),
        ('extra.', 'mac_address', validate_to_none),
        ('extra.', 'ipv4_address', validate_to_none),
        ('extra.', 'ipv4_gateway', validate_to_none),
        ('extra.', 'ipv4_subnet_mask', validate_to_none),
        ('extra.', 'ipv6_address', validate_to_none),
        ('extra.', 'ipv6_link_local', validate_to_none),
        ('extra.', 'ipv6_gateway', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'classification.identifier': 'open-dvr-dhcpdiscover',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-elasticsearch-report/
scan_elasticsearch = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'build_snapshot', convert_bool),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'ok', convert_bool),
        ('extra.', 'name', validate_to_none),
        ('extra.', 'cluster_name', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'build_hash', validate_to_none),
        ('extra.', 'build_timestamp', validate_to_none),
        ('extra.', 'lucene_version', validate_to_none),
        ('extra.', 'tagline', validate_to_none),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'elasticsearch',
        'classification.identifier': 'open-elasticsearch',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-erlang-port-mapper-report-daemon/
scan_epmd = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'nodes', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'protocol.application': 'Erlang Port Mapper Daemon',
        'classification.identifier': 'open-epmd',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/vulnerable-exchange-server-report/
scan_exchange = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('classification.taxonomy', 'tag', scan_exchange_taxonomy),
        ('classification.type', 'tag', scan_exchange_type),
        ('classification.identifier', 'tag', scan_exchange_identifier),
        ('extra.', 'tag', validate_to_none),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'servername', validate_to_none),
        ('destination.url', 'url', convert_http_host_and_url, True),
    ],
    'constant_fields': {
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-ftp-report/
scan_ftp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'banner', validate_to_none),
        ('extra.', 'handshake', validate_to_none),
        ('extra.', 'cipher_suite', validate_to_none),
        ('extra.', 'cert_length', convert_int),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'ssl_version', convert_int),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'subject_organization_name', validate_to_none),
        ('extra.', 'subject_organization_unit_name', validate_to_none),
        ('extra.', 'subject_country', validate_to_none),
        ('extra.', 'subject_state_or_province_name', validate_to_none),
        ('extra.', 'subject_locality_name', validate_to_none),
        ('extra.', 'subject_street_address', validate_to_none),
        ('extra.', 'subject_postal_code', validate_to_none),
        ('extra.', 'subject_surname', validate_to_none),
        ('extra.', 'subject_given_name', validate_to_none),
        ('extra.', 'subject_email_address', validate_to_none),
        ('extra.', 'subject_business_category', validate_to_none),
        ('extra.', 'subject_serial_number', validate_to_none),
        ('extra.', 'issuer_organization_name', validate_to_none),
        ('extra.', 'issuer_organization_unit_name', validate_to_none),
        ('extra.', 'issuer_country', validate_to_none),
        ('extra.', 'issuer_state_or_province_name', validate_to_none),
        ('extra.', 'issuer_locality_name', validate_to_none),
        ('extra.', 'issuer_street_address', validate_to_none),
        ('extra.', 'issuer_postal_code', validate_to_none),
        ('extra.', 'issuer_surname', validate_to_none),
        ('extra.', 'issuer_given_name', validate_to_none),
        ('extra.', 'issuer_email_address', validate_to_none),
        ('extra.', 'issuer_business_category', validate_to_none),
        ('extra.', 'issuer_serial_number', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'cert_valid', convert_bool),
        ('extra.', 'self_signed', convert_bool),
        ('extra.', 'cert_expired', convert_bool),
        ('extra.', 'validation_level', validate_to_none),
        ('extra.', 'auth_tls_response', validate_to_none),
        ('extra.', 'auth_ssl_response', validate_to_none),
        ('extra.', 'tlsv13_support', validate_to_none),
        ('extra.', 'tlsv13_cipher', validate_to_none),
        ('extra.', 'jarm', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('extra.', 'device_version', validate_to_none),
        ('extra.', 'device_sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-ftp',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'ftp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-hadoop-report/
scan_hadoop = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'total_disk', convert_int),
        ('extra.', 'used_disk', convert_int),
        ('extra.', 'free_disk', convert_int),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'server_type', validate_to_none),
        ('extra.', 'clusterid', validate_to_none),
        ('extra.', 'livenodes', validate_to_none),
        ('extra.', 'namenodeaddress', validate_to_none),
        ('extra.', 'volumeinfo', validate_to_none),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-hadoop',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'hadoop',
        'protocol.transport': 'tcp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-http-report/
scan_http = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.', 'http', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'connection', validate_to_none),
        ('extra.', 'www_authenticate', validate_to_none),
        ('extra.', 'set_cookie', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'content_length', convert_int),
        ('extra.', 'transfer_encoding', validate_to_none),
        ('extra.', 'http_date', convert_date),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-http',
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'protocol.application': 'http',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-http-proxy-report/
scan_http_proxy = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.', 'http', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'connection', validate_to_none),
        ('extra.', 'proxy_authenticate', validate_to_none),
        ('extra.', 'via', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'content_length', convert_int),
        ('extra.', 'transfer_encoding', validate_to_none),
        ('extra.', 'http_date', convert_date),
    ],
    'constant_fields': {
        'classification.identifier': 'open-http-proxy',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'http',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/vulnerable-http-report/
scan_http_vulnerable = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'http', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'connection', validate_to_none),
        ('extra.', 'www_authenticate', validate_to_none),
        ('extra.', 'set_cookie', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'content_length', convert_int),
        ('extra.', 'transfer_encoding', validate_to_none),
        ('extra.', 'http_date', convert_date),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'build_date', validate_to_none),
        ('extra.', 'detail', validate_to_none),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-http',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'http',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-ics-report/
scan_ics = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.application', 'tag'),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('extra.', 'device_version', validate_to_none),
        ('extra.', 'device_id', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'raw_response', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'classification.identifier': 'open-ics',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-ipmi-report/
scan_ipmi = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'none_auth', convert_bool),
        ('extra.', 'md2_auth', convert_bool),
        ('extra.', 'md5_auth', convert_bool),
        ('extra.', 'passkey_auth', convert_bool),
        ('extra.', 'oem_auth', convert_bool),
        ('extra.', 'permessage_auth', convert_bool),
        ('extra.', 'userlevel_auth', convert_bool),
        ('extra.', 'usernames', convert_bool),
        ('extra.', 'nulluser', convert_bool),
        ('extra.', 'anon_login', convert_bool),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'ipmi_version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'defaultkg', validate_to_none),
        ('extra.', 'error', validate_to_none),
        ('extra.', 'deviceid', validate_to_none),
        ('extra.', 'devicerev', validate_to_none),
        ('extra.', 'firmwarerev', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'manufacturerid', validate_to_none),
        ('extra.', 'manufacturername', validate_to_none),
        ('extra.', 'productid', validate_to_none),
        ('extra.', 'productname', validate_to_none),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'ipmi',
        'protocol.transport': 'udp',
        'classification.identifier': 'open-ipmi',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-ipp-report/
scan_ipp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'ipp_version', validate_to_none),
        ('extra.', 'cups_version', validate_to_none),
        ('extra.', 'printer_uris', validate_to_none),
        ('extra.', 'printer_name', validate_to_none),
        ('extra.', 'printer_info', validate_to_none),
        ('extra.', 'printer_more_info', validate_to_none),
        ('extra.', 'printer_make_and_model', validate_to_none),
        ('extra.', 'printer_firmware_name', validate_to_none),
        ('extra.', 'printer_firmware_string_version', validate_to_none),
        ('extra.', 'printer_firmware_version', validate_to_none),
        ('extra.', 'printer_organization', validate_to_none),
        ('extra.', 'printer_organization_unit', validate_to_none),
        ('extra.', 'printer_uuid', validate_to_none),
        ('extra.', 'printer_wifi_ssid', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('extra.', 'device_version', validate_to_none),
        ('extra.', 'device_sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'ipp',
        'classification.identifier': 'open-ipp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/vulnerable-isakmp-report/
scan_isakmp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'spi_size', convert_int),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'initiator_spi', validate_to_none),
        ('extra.', 'responder_spi', validate_to_none),
        ('extra.', 'next_payload', validate_to_none),
        ('extra.', 'exchange_type', validate_to_none),
        ('extra.', 'flags', validate_to_none),
        ('extra.', 'message_id', validate_to_none),
        ('extra.', 'next_payload2', validate_to_none),
        ('extra.', 'domain_of_interpretation', validate_to_none),
        ('extra.', 'protocol_id', validate_to_none),
        ('extra.', 'notify_message_type', validate_to_none),
    ],
    'constant_fields': {
        'classification.identifier': 'open-ike',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'ipsec',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-kubernetes-api-server-report/
scan_kubernetes = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'http', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'date', validate_to_none),
        ('extra.', 'major', validate_to_none),
        ('extra.', 'minor', validate_to_none),
        ('extra.', 'git_version', validate_to_none),
        ('extra.', 'git_commit', validate_to_none),
        ('extra.', 'git_tree_state', validate_to_none),
        ('extra.', 'build_date', validate_to_none),
        ('extra.', 'go_version', validate_to_none),
        ('extra.', 'compiler', validate_to_none),
        ('extra.', 'platform', validate_to_none),
        ('extra.', 'handshake', validate_to_none),
        ('extra.', 'cipher_suite', validate_to_none),
        ('extra.', 'cert_length', convert_int),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'ssl_version', convert_int),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'subject_organization_name', validate_to_none),
        ('extra.', 'subject_organization_unit_name', validate_to_none),
        ('extra.', 'subject_country', validate_to_none),
        ('extra.', 'subject_state_or_province_name', validate_to_none),
        ('extra.', 'subject_locality_name', validate_to_none),
        ('extra.', 'subject_street_address', validate_to_none),
        ('extra.', 'subject_postal_code', validate_to_none),
        ('extra.', 'subject_surname', validate_to_none),
        ('extra.', 'subject_given_name', validate_to_none),
        ('extra.', 'subject_email_address', validate_to_none),
        ('extra.', 'subject_business_category', validate_to_none),
        ('extra.', 'subject_serial_number', validate_to_none),
        ('extra.', 'issuer_organization_name', validate_to_none),
        ('extra.', 'issuer_organization_unit_name', validate_to_none),
        ('extra.', 'issuer_country', validate_to_none),
        ('extra.', 'issuer_state_or_province_name', validate_to_none),
        ('extra.', 'issuer_locality_name', validate_to_none),
        ('extra.', 'issuer_street_address', validate_to_none),
        ('extra.', 'issuer_postal_code', validate_to_none),
        ('extra.', 'issuer_surname', validate_to_none),
        ('extra.', 'issuer_given_name', validate_to_none),
        ('extra.', 'issuer_email_address', validate_to_none),
        ('extra.', 'issuer_business_category', validate_to_none),
        ('extra.', 'issuer_serial_number', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'cert_valid', convert_bool),
        ('extra.', 'self_signed', convert_bool),
        ('extra.', 'cert_expired', convert_bool),
        ('extra.', 'validation_level', validate_to_none),
        ('extra.', 'browser_trusted', convert_bool),
        ('extra.', 'browser_error', validate_to_none),
        ('extra.', 'raw_cert', validate_to_none),
        ('extra.', 'raw_cert_chain', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'kubernetes',
        'classification.identifier': 'open-kubernetes',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-ldap-tcp-report/
scan_ldap_tcp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('source.local_hostname', 'dns_host_name', validate_to_none),
        ('extra.', 'domain_controller_functionality', convert_int),
        ('extra.', 'domain_functionality', convert_int),
        ('extra.', 'forest_functionality', convert_int),
        ('extra.', 'highest_committed_usn', convert_int),
        ('extra.', 'is_global_catalog_ready', convert_bool),
        ('extra.', 'is_synchronized', convert_bool),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'size', convert_int),
        ('extra.', 'configuration_naming_context', validate_to_none),
        ('extra.', 'current_time', validate_to_none),
        ('extra.', 'default_naming_context', validate_to_none),
        ('extra.', 'ds_service_name', validate_to_none),
        ('extra.', 'ldap_service_name', validate_to_none),
        ('extra.', 'naming_contexts', validate_to_none),
        ('extra.', 'root_domain_naming_context', validate_to_none),
        ('extra.', 'schema_naming_context', validate_to_none),
        ('extra.', 'server_name', validate_to_none),
        ('extra.', 'subschema_subentry', validate_to_none),
        ('extra.', 'supported_capabilities', validate_to_none),
        ('extra.', 'supported_control', validate_to_none),
        ('extra.', 'supported_ldap_policies', validate_to_none),
        ('extra.', 'supported_ldap_version', validate_to_none),
        ('extra.', 'supported_sasl_mechanisms', validate_to_none),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.identifier': 'open-ldap',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'ldap',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-ldap-report/
scan_ldap_udp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('source.local_hostname', 'dns_host_name', validate_to_none),
        ('extra.', 'domain_controller_functionality', convert_int),
        ('extra.', 'domain_functionality', convert_int),
        ('extra.', 'forest_functionality', convert_int),
        ('extra.', 'highest_committed_usn', convert_int),
        ('extra.', 'is_global_catalog_ready', convert_bool),
        ('extra.', 'is_synchronized', convert_bool),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.', 'size', convert_int),
        ('extra.', 'configuration_naming_context', validate_to_none),
        ('extra.', 'current_time', validate_to_none),
        ('extra.', 'default_naming_context', validate_to_none),
        ('extra.', 'ds_service_name', validate_to_none),
        ('extra.', 'ldap_service_name', validate_to_none),
        ('extra.', 'naming_contexts', validate_to_none),
        ('extra.', 'root_domain_naming_context', validate_to_none),
        ('extra.', 'schema_naming_context', validate_to_none),
        ('extra.', 'server_name', validate_to_none),
        ('extra.', 'subschema_subentry', validate_to_none),
        ('extra.', 'supported_capabilities', validate_to_none),
        ('extra.', 'supported_control', validate_to_none),
        ('extra.', 'supported_ldap_policies', validate_to_none),
        ('extra.', 'supported_ldap_version', validate_to_none),
        ('extra.', 'supported_sasl_mechanisms', validate_to_none),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.identifier': 'open-ldap',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'ldap',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-mdns-report/
scan_mdns = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'mdns_name', validate_to_none),
        ('extra.', 'mdns_ipv4', validate_to_none),
        ('extra.', 'mdns_ipv6', validate_to_none),
        ('extra.', 'services', validate_to_none),
        ('extra.', 'workstation_name', validate_to_none),
        ('extra.', 'workstation_ipv4', validate_to_none),
        ('extra.', 'workstation_ipv6', validate_to_none),
        ('extra.', 'workstation_info', validate_to_none),
        ('extra.', 'http_name', validate_to_none),
        ('extra.', 'http_ipv4', validate_to_none),
        ('extra.', 'http_ipv6', validate_to_none),
        ('extra.', 'http_ptr', validate_to_none),
        ('extra.', 'http_info', validate_to_none),
        ('extra.', 'http_target', validate_to_none),
        ('extra.', 'http_port', convert_int),
        ('extra.', 'spotify_name', validate_to_none),
        ('extra.', 'spotify_ipv4', validate_to_none),
        ('extra.', 'spotify_ipv6', validate_to_none),
        ('extra.', 'opc_ua_discovery', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'mdns',
        'classification.identifier': 'open-mdns',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-memcached-report/
scan_memcached = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'pid', convert_int),
        ('extra.', 'pointer_size', convert_int),
        ('extra.', 'uptime', convert_int),
        ('extra.', 'curr_connections', convert_int),
        ('extra.', 'total_connections', convert_int),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'time', validate_to_none),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'memcached',
        'classification.identifier': 'open-memcached',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-mongodb-report/
scan_mongodb = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'gitversion', validate_to_none),
        ('extra.', 'sysinfo', validate_to_none),
        ('extra.', 'opensslversion', validate_to_none),
        ('extra.', 'allocator', validate_to_none),
        ('extra.', 'javascriptengine', validate_to_none),
        ('extra.', 'bits', validate_to_none),
        ('extra.', 'maxbsonobjectsize', validate_to_none),
        ('extra.', 'ok', convert_bool),
        ('extra.', 'visible_databases', validate_to_none),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'mongodb',
        'classification.identifier': 'open-mongodb',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-mqtt-report/
scan_mqtt = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'anonymous_access', convert_bool),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'raw_response', validate_to_none),
        ('extra.', 'hex_code', validate_to_none),
        ('extra.', 'code', validate_to_none),
        ('extra.', 'cipher_suite', validate_to_none),
        ('extra.', 'cert_length', convert_int),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'ssl_version', convert_int),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'subject_organization_name', validate_to_none),
        ('extra.', 'subject_organization_unit_name', validate_to_none),
        ('extra.', 'subject_country', validate_to_none),
        ('extra.', 'subject_state_or_province_name', validate_to_none),
        ('extra.', 'subject_locality_name', validate_to_none),
        ('extra.', 'subject_street_address', validate_to_none),
        ('extra.', 'subject_postal_code', validate_to_none),
        ('extra.', 'subject_surname', validate_to_none),
        ('extra.', 'subject_given_name', validate_to_none),
        ('extra.', 'subject_email_address', validate_to_none),
        ('extra.', 'subject_business_category', validate_to_none),
        ('extra.', 'subject_serial_number', validate_to_none),
        ('extra.', 'issuer_organization_name', validate_to_none),
        ('extra.', 'issuer_organization_unit_name', validate_to_none),
        ('extra.', 'issuer_country', validate_to_none),
        ('extra.', 'issuer_state_or_province_name', validate_to_none),
        ('extra.', 'issuer_locality_name', validate_to_none),
        ('extra.', 'issuer_street_address', validate_to_none),
        ('extra.', 'issuer_postal_code', validate_to_none),
        ('extra.', 'issuer_surname', validate_to_none),
        ('extra.', 'issuer_given_name', validate_to_none),
        ('extra.', 'issuer_email_address', validate_to_none),
        ('extra.', 'issuer_business_category', validate_to_none),
        ('extra.', 'issuer_serialNumber', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'mqtt',
        'classification.identifier': 'open-mqtt',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-mqtt-report/
scan_mqtt_anon = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.', 'raw_response', validate_to_none),
        ('extra.', 'hex_code', validate_to_none),
        ('extra.', 'code', validate_to_none),
        ('extra.', 'cipher_suite', validate_to_none),
        ('extra.', 'cert_length', convert_int),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'ssl_version', convert_int),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'subject_organization_name', validate_to_none),
        ('extra.', 'subject_organization_unit_name', validate_to_none),
        ('extra.', 'subject_country', validate_to_none),
        ('extra.', 'subject_state_or_province_name', validate_to_none),
        ('extra.', 'subject_locality_name', validate_to_none),
        ('extra.', 'subject_street_address', validate_to_none),
        ('extra.', 'subject_postal_code', validate_to_none),
        ('extra.', 'subject_surname', validate_to_none),
        ('extra.', 'subject_given_name', validate_to_none),
        ('extra.', 'subject_email_address', validate_to_none),
        ('extra.', 'subject_business_category', validate_to_none),
        ('extra.', 'subject_serial_number', validate_to_none),
        ('extra.', 'issuer_organization_name', validate_to_none),
        ('extra.', 'issuer_organization_unit_name', validate_to_none),
        ('extra.', 'issuer_country', validate_to_none),
        ('extra.', 'issuer_state_or_province_name', validate_to_none),
        ('extra.', 'issuer_locality_name', validate_to_none),
        ('extra.', 'issuer_street_address', validate_to_none),
        ('extra.', 'issuer_postal_code', validate_to_none),
        ('extra.', 'issuer_surname', validate_to_none),
        ('extra.', 'issuer_given_name', validate_to_none),
        ('extra.', 'issuer_email_address', validate_to_none),
        ('extra.', 'issuer_business_category', validate_to_none),
        ('extra.', 'issuer_serialNumber', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'mqtt',
        'classification.identifier': 'open-mqtt-anon',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-MSSQL
scan_mssql = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('source.local_hostname', 'server_name', validate_to_none),
        ('extra.', 'tcp_port', convert_int),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'instance_name', validate_to_none),
        ('extra.', 'named_pipe', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'mssql',
        'classification.identifier': 'open-mssql',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-mysql-server-report/
scan_mysql = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'client_can_handle_expired_passwords', convert_bool),
        ('extra.', 'client_compress', convert_bool),
        ('extra.', 'client_connect_attrs', convert_bool),
        ('extra.', 'client_connect_with_db', convert_bool),
        ('extra.', 'client_deprecated_eof', convert_bool),
        ('extra.', 'client_found_rows', convert_bool),
        ('extra.', 'client_ignore_sigpipe', convert_bool),
        ('extra.', 'client_ignore_space', convert_bool),
        ('extra.', 'client_interactive', convert_bool),
        ('extra.', 'client_local_files', convert_bool),
        ('extra.', 'client_long_flag', convert_bool),
        ('extra.', 'client_long_password', convert_bool),
        ('extra.', 'client_multi_results', convert_bool),
        ('extra.', 'client_multi_statements', convert_bool),
        ('extra.', 'client_no_schema', convert_bool),
        ('extra.', 'client_odbc', convert_bool),
        ('extra.', 'client_plugin_auth', convert_bool),
        ('extra.', 'client_plugin_auth_len_enc_client_data', convert_bool),
        ('extra.', 'client_protocol_41', convert_bool),
        ('extra.', 'client_ps_multi_results', convert_bool),
        ('extra.', 'client_reserved', convert_bool),
        ('extra.', 'client_secure_connection', convert_bool),
        ('extra.', 'client_session_track', convert_bool),
        ('extra.', 'client_ssl', convert_bool),
        ('extra.', 'client_transactions', convert_bool),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'mysql_protocol_version', validate_to_none),
        ('extra.', 'server_version', validate_to_none),
        ('extra.', 'error_code', validate_to_none),
        ('extra.', 'error_id', validate_to_none),
        ('extra.', 'error_message', validate_to_none),
        ('extra.', 'handshake', validate_to_none),
        ('extra.', 'cipher_suite', validate_to_none),
        ('extra.', 'cert_length', convert_int),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'ssl_version', convert_int),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'subject_organization_name', validate_to_none),
        ('extra.', 'subject_organization_unit_name', validate_to_none),
        ('extra.', 'subject_country', validate_to_none),
        ('extra.', 'subject_state_or_province_name', validate_to_none),
        ('extra.', 'subject_locality_name', validate_to_none),
        ('extra.', 'subject_street_address', validate_to_none),
        ('extra.', 'subject_postal_code', validate_to_none),
        ('extra.', 'subject_surname', validate_to_none),
        ('extra.', 'subject_given_name', validate_to_none),
        ('extra.', 'subject_email_address', validate_to_none),
        ('extra.', 'subject_business_category', validate_to_none),
        ('extra.', 'subject_serial_number', validate_to_none),
        ('extra.', 'issuer_organization_name', validate_to_none),
        ('extra.', 'issuer_organization_unit_name', validate_to_none),
        ('extra.', 'issuer_country', validate_to_none),
        ('extra.', 'issuer_state_or_province_name', validate_to_none),
        ('extra.', 'issuer_locality_name', validate_to_none),
        ('extra.', 'issuer_street_address', validate_to_none),
        ('extra.', 'issuer_postal_code', validate_to_none),
        ('extra.', 'issuer_surname', validate_to_none),
        ('extra.', 'issuer_given_name', validate_to_none),
        ('extra.', 'issuer_email_address', validate_to_none),
        ('extra.', 'issuer_business_category', validate_to_none),
        ('extra.', 'issuer_serial_number', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'cert_valid', convert_bool),
        ('extra.', 'self_signed', convert_bool),
        ('extra.', 'cert_expired', convert_bool),
        ('extra.', 'validation_level', validate_to_none),
        ('extra.', 'browser_trusted', convert_bool),
        ('extra.', 'browser_error', validate_to_none),
        ('extra.', 'raw_cert', validate_to_none),
        ('extra.', 'raw_cert_chain', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'protocol.application': 'mysql',
        'classification.identifier': 'open-mysql',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-NATPMP
scan_nat_pmp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'opcode', validate_to_none),
        ('extra.', 'uptime', convert_int),
        ('extra.', 'external_ip', validate_to_none),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.identifier': 'open-natpmp',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'natpmp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-netbios-report/
scan_netbios = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('source.account', 'username'),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'mac_address', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'workgroup', validate_to_none),
        ('extra.', 'machine_name', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.identifier': 'open-netbios-nameservice',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'netbios-nameservice',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/netcore-netis-router-vulnerability-scan-report/
scan_netis_router = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'response', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.identifier': 'open-netis',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.transport': 'udp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/ntp-version-report/
scan_ntp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'clk_wander', convert_float),
        ('extra.', 'frequency', convert_float),
        ('extra.', 'jitter', convert_float),
        ('extra.', 'leap', convert_float),
        ('extra.', 'offset', convert_float),
        ('extra.', 'peer', convert_int),
        ('extra.', 'poll', convert_int),
        ('extra.', 'precision', convert_int),
        ('extra.', 'rootdelay', convert_float),
        ('extra.', 'rootdispersion', convert_float),
        ('extra.', 'stratum', convert_int),
        ('extra.', 'tc', convert_int),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'clock', validate_to_none),
        ('extra.', 'error', validate_to_none),
        ('extra.', 'mintc', validate_to_none),
        ('extra.', 'noise', validate_to_none),
        ('extra.', 'phase', validate_to_none),
        ('extra.', 'processor', validate_to_none),
        ('extra.', 'refid', validate_to_none),
        ('extra.', 'reftime', validate_to_none),
        ('extra.', 'stability', validate_to_none),
        ('extra.', 'state', validate_to_none),
        ('extra.', 'system', validate_to_none),
        ('extra.', 'tai', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.identifier': 'ntp-version',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'ntp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/ntp-monitor-report/
scan_ntpmonitor = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'packets', convert_int),
        ('extra.', 'size', convert_int),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.identifier': 'ntp-monitor',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'ntp',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Portmapper
scan_portmapper = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'programs', validate_to_none),
        ('extra.', 'mountd_port', validate_to_none),
        ('extra.', 'exports', validate_to_none),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'portmapper',
        'classification.identifier': 'open-portmapper',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-postgresql-server-report/
scan_postgres = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'startup_error_line', convert_int),
        ('extra.', 'client_ssl', convert_bool),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'supported_protocols', validate_to_none),
        ('extra.', 'protocol_error_code', validate_to_none),
        ('extra.', 'protocol_error_file', validate_to_none),
        ('extra.', 'protocol_error_line', validate_to_none),
        ('extra.', 'protocol_error_message', validate_to_none),
        ('extra.', 'protocol_error_routine', validate_to_none),
        ('extra.', 'protocol_error_severity', validate_to_none),
        ('extra.', 'protocol_error_severity_v', validate_to_none),
        ('extra.', 'startup_error_code', validate_to_none),
        ('extra.', 'startup_error_file', validate_to_none),
        ('extra.', 'startup_error_message', validate_to_none),
        ('extra.', 'startup_error_routine', validate_to_none),
        ('extra.', 'startup_error_severity', validate_to_none),
        ('extra.', 'startup_error_severity_v', validate_to_none),
        ('extra.', 'handshake', validate_to_none),
        ('extra.', 'cipher_suite', validate_to_none),
        ('extra.', 'cert_length', convert_int),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'ssl_version', convert_int),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'subject_organization_name', validate_to_none),
        ('extra.', 'subject_organization_unit_name', validate_to_none),
        ('extra.', 'subject_country', validate_to_none),
        ('extra.', 'subject_state_or_province_name', validate_to_none),
        ('extra.', 'subject_locality_name', validate_to_none),
        ('extra.', 'subject_street_address', validate_to_none),
        ('extra.', 'subject_postal_code', validate_to_none),
        ('extra.', 'subject_surname', validate_to_none),
        ('extra.', 'subject_given_name', validate_to_none),
        ('extra.', 'subject_email_address', validate_to_none),
        ('extra.', 'subject_business_category', validate_to_none),
        ('extra.', 'subject_serial_number', validate_to_none),
        ('extra.', 'issuer_organization_name', validate_to_none),
        ('extra.', 'issuer_organization_unit_name', validate_to_none),
        ('extra.', 'issuer_country', validate_to_none),
        ('extra.', 'issuer_state_or_province_name', validate_to_none),
        ('extra.', 'issuer_locality_name', validate_to_none),
        ('extra.', 'issuer_street_address', validate_to_none),
        ('extra.', 'issuer_postal_code', validate_to_none),
        ('extra.', 'issuer_surname', validate_to_none),
        ('extra.', 'issuer_given_name', validate_to_none),
        ('extra.', 'issuer_email_address', validate_to_none),
        ('extra.', 'issuer_business_category', validate_to_none),
        ('extra.', 'issuer_serial_number', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'cert_valid', convert_bool),
        ('extra.', 'self_signed', convert_bool),
        ('extra.', 'cert_expired', convert_bool),
        ('extra.', 'validation_level', validate_to_none),
        ('extra.', 'browser_trusted', convert_bool),
        ('extra.', 'browser_error', validate_to_none),
        ('extra.', 'raw_cert', validate_to_none),
        ('extra.', 'raw_cert_chain', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'protocol.application': 'postgres',
        'classification.identifier': 'open-postgres',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-QOTD
scan_qotd = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'quote', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'qotd',
        'classification.identifier': 'open-qotd',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-quic-report/
scan_quic = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.', 'version_field_1', validate_to_none),
        ('extra.', 'version_field_2', validate_to_none),
        ('extra.', 'version_field_3', validate_to_none),
        ('extra.', 'version_field_4', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'classification.identifier': 'open-quic',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-radmin-report/
scan_radmin = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-radmin',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-rdp-report/
scan_rdp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'cve20190708_vulnerable', convert_bool),
        ('extra.', 'bluekeep_vulnerable', convert_bool),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'handshake', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'rdp_protocol', validate_to_none),
        ('extra.', 'cert_length', convert_int),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'ssl_version', convert_int),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'tlsv13_support', validate_to_none),
        ('extra.', 'tlsv13_cipher', validate_to_none),
        ('extra.', 'jarm', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'rdp',
        'protocol.transport': 'tcp',
        'classification.identifier': 'open-rdp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-ms-rdpeudp/
scan_rdpeudp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sessionid', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-msrdpeudp',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-Redis
scan_redis = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'git_sha1', validate_to_none),
        ('extra.', 'git_dirty_flag', validate_to_none),
        ('extra.', 'build_id', validate_to_none),
        ('extra.', 'mode', validate_to_none),
        ('extra.os.name', 'os', validate_to_none),
        ('extra.', 'architecture', validate_to_none),
        ('extra.', 'multiplexing_api', validate_to_none),
        ('extra.', 'gcc_version', validate_to_none),
        ('extra.', 'process_id', validate_to_none),
        ('extra.', 'run_id', validate_to_none),
        ('extra.', 'uptime', convert_int),
        ('extra.', 'connected_clients', validate_to_none),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'redis',
        'classification.identifier': 'open-redis',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-rsync-report/
scan_rsync = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'module', validate_to_none),
        ('extra.', 'motd', validate_to_none),
        ('extra.', 'has_password', validate_to_none),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-rsync',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'rsync',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-slp-service-report/
scan_slp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'function', validate_to_none),
        ('extra.', 'function_text', validate_to_none),
        ('extra.', 'flags', validate_to_none),
        ('extra.', 'next_extension_offset', validate_to_none),
        ('extra.', 'xid', validate_to_none),
        ('extra.', 'language_tag_length', validate_to_none),
        ('extra.', 'language_tag', validate_to_none),
        ('extra.', 'error_code', validate_to_none),
        ('extra.', 'error_code_text', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'raw_response', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'slp',
        'classification.identifier': 'open-slp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-smb-report/
scan_smb = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'smb_implant', convert_bool),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'arch', validate_to_none),
        ('extra.', 'key', validate_to_none),
        ('extra.', 'smbv1_support', validate_to_none),
        ('extra.', 'smb_major_number', validate_to_none),
        ('extra.', 'smb_minor_number', validate_to_none),
        ('extra.', 'smb_revision', validate_to_none),
        ('extra.', 'smb_version_string', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'smb',
        'protocol.transport': 'tcp',
        'classification.identifier': 'open-smb',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-smtp-report/
scan_smtp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.', 'banner', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'protocol.application': 'smtp',
        'classification.identifier': 'open-smtp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/vulnerable-smtp-report/
scan_smtp_vulnerable = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'banner', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'smtp',
        'classification.identifier': 'vulnerable-smtp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-snmp-report/
scan_snmp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'sysdesc', validate_to_none),
        ('extra.', 'sysname', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('extra.', 'device_version', validate_to_none),
        ('extra.', 'device_sector', validate_to_none),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'community', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'snmp',
        'classification.identifier': 'open-snmp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-socks4-5-proxy-report/
scan_socks = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.application', 'tag'),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'classification.identifier': 'open-socks',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-SSDP
scan_ssdp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'header', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'systime', validate_to_none),
        ('extra.', 'cache_control', validate_to_none),
        ('extra.', 'location', validate_to_none),
        ('extra.', 'server', validate_to_none),
        ('extra.', 'search_target', validate_to_none),
        ('extra.', 'unique_service_name', validate_to_none),
        ('extra.', 'host', validate_to_none),
        ('extra.', 'nts', validate_to_none),
        ('extra.', 'nt', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'server_port', validate_to_none),
        ('extra.', 'instance', validate_to_none),
        ('extra.', 'version', validate_to_none),
        ('extra.', 'updated_at', validate_to_none),
        ('extra.', 'resource_identifier', validate_to_none),
        ('extra.', 'amplification', convert_float),
        ('extra.', 'response_size', convert_int),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'ssdp',
        'classification.identifier': 'open-ssdp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-ssh-report/
scan_ssh = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.', 'serverid_raw', validate_to_none),
        ('extra.', 'serverid_version', validate_to_none),
        ('extra.', 'serverid_software', validate_to_none),
        ('extra.', 'serverid_comment', validate_to_none),
        ('extra.', 'server_cookie', validate_to_none),
        ('extra.', 'available_kex', validate_to_none),
        ('extra.', 'available_ciphers', validate_to_none),
        ('extra.', 'available_mac', validate_to_none),
        ('extra.', 'available_compression', validate_to_none),
        ('extra.', 'selected_kex', validate_to_none),
        ('extra.', 'algorithm', validate_to_none),
        ('extra.', 'selected_cipher', validate_to_none),
        ('extra.', 'selected_mac', validate_to_none),
        ('extra.', 'selected_compression', validate_to_none),
        ('extra.', 'server_signature_value', validate_to_none),
        ('extra.', 'server_signature_raw', validate_to_none),
        ('extra.', 'server_host_key', validate_to_none),
        ('extra.', 'server_host_key_sha256', validate_to_none),
        ('extra.', 'rsa_prime', validate_to_none),
        ('extra.', 'rsa_prime_length', validate_to_none),
        ('extra.', 'rsa_generator', validate_to_none),
        ('extra.', 'rsa_generator_length', validate_to_none),
        ('extra.', 'rsa_public_key', validate_to_none),
        ('extra.', 'rsa_public_key_length', validate_to_none),
        ('extra.', 'rsa_exponent', validate_to_none),
        ('extra.', 'rsa_modulus', validate_to_none),
        ('extra.', 'rsa_length', validate_to_none),
        ('extra.', 'dss_prime', validate_to_none),
        ('extra.', 'dss_prime_length', validate_to_none),
        ('extra.', 'dss_generator', validate_to_none),
        ('extra.', 'dss_generator_length', validate_to_none),
        ('extra.', 'dss_public_key', validate_to_none),
        ('extra.', 'dss_public_key_length', validate_to_none),
        ('extra.', 'dss_dsa_public_g', validate_to_none),
        ('extra.', 'dss_dsa_public_p', validate_to_none),
        ('extra.', 'dss_dsa_public_q', validate_to_none),
        ('extra.', 'dss_dsa_public_y', validate_to_none),
        ('extra.', 'ecdsa_curve25519', validate_to_none),
        ('extra.', 'ecdsa_curve', validate_to_none),
        ('extra.', 'ecdsa_public_key_length', validate_to_none),
        ('extra.', 'ecdsa_public_key_b', validate_to_none),
        ('extra.', 'ecdsa_public_key_gx', validate_to_none),
        ('extra.', 'ecdsa_public_key_gy', validate_to_none),
        ('extra.', 'ecdsa_public_key_n', validate_to_none),
        ('extra.', 'ecdsa_public_key_p', validate_to_none),
        ('extra.', 'ecdsa_public_key_x', validate_to_none),
        ('extra.', 'ecdsa_public_key_y', validate_to_none),
        ('extra.', 'ed25519_curve25519', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_nonce', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_bytes', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_raw', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_sha256', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_serial', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_type_id', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_type_name', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_keyid', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_principles', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_valid_after', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_valid_before', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_duration', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_sigkey_bytes', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_sigkey_raw', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_sigkey_sha256', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_sigkey_value', validate_to_none),
        ('extra.', 'ed25519_cert_public_key_sig_raw', validate_to_none),
        ('extra.', 'banner', validate_to_none),
        ('extra.', 'userauth_methods', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('extra.', 'device_version', validate_to_none),
        ('extra.', 'device_sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'classification.identifier': 'open-ssh',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-ssl-report/
scan_ssl = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'handshake', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'cipher_suite', validate_to_none),
        ('extra.', 'ssl_poodle', convert_bool),
        ('extra.', 'cert_length', convert_int),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'ssl_version', convert_int),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'subject_organization_name', validate_to_none),
        ('extra.', 'subject_organization_unit_name', validate_to_none),
        ('extra.', 'subject_country', validate_to_none),
        ('extra.', 'subject_state_or_province_name', validate_to_none),
        ('extra.', 'subject_locality_name', validate_to_none),
        ('extra.', 'subject_street_address', validate_to_none),
        ('extra.', 'subject_postal_code', validate_to_none),
        ('extra.', 'subject_surname', validate_to_none),
        ('extra.', 'subject_given_name', validate_to_none),
        ('extra.', 'subject_email_address', validate_to_none),
        ('extra.', 'subject_business_category', validate_to_none),
        ('extra.', 'subject_serial_number', validate_to_none),
        ('extra.', 'issuer_organization_name', validate_to_none),
        ('extra.', 'issuer_organization_unit_name', validate_to_none),
        ('extra.', 'issuer_country', validate_to_none),
        ('extra.', 'issuer_state_or_province_name', validate_to_none),
        ('extra.', 'issuer_locality_name', validate_to_none),
        ('extra.', 'issuer_street_address', validate_to_none),
        ('extra.', 'issuer_postal_code', validate_to_none),
        ('extra.', 'issuer_surname', validate_to_none),
        ('extra.', 'issuer_given_name', validate_to_none),
        ('extra.', 'issuer_email_address', validate_to_none),
        ('extra.', 'issuer_business_category', validate_to_none),
        ('extra.', 'issuer_serial_number', validate_to_none),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.', 'freak_vulnerable', convert_bool),
        ('extra.', 'freak_cipher_suite', validate_to_none),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'http_response_type', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'http_connection', validate_to_none),
        ('extra.', 'www_authenticate', validate_to_none),
        ('extra.', 'set_cookie', validate_to_none),
        ('extra.', 'server_type', validate_to_none),
        ('extra.', 'content_length', convert_int),
        ('extra.', 'transfer_encoding', validate_to_none),
        ('extra.', 'http_date', convert_date),
        ('extra.', 'cert_valid', convert_bool),
        ('extra.', 'self_signed', convert_bool),
        ('extra.', 'cert_expired', convert_bool),
        ('extra.', 'browser_trusted', convert_bool),
        ('extra.', 'validation_level', validate_to_none),
        ('extra.', 'browser_error', validate_to_none),
        ('extra.', 'tlsv13_support', validate_to_none),
        ('extra.', 'tlsv13_cipher', validate_to_none),
        ('extra.', 'jarm', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'protocol.application': 'https',
        'classification.identifier': 'open-ssl',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Ssl-Freak-Scan
scan_ssl_freak = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'handshake', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'cipher_suite', validate_to_none),
        ('extra.', 'cert_length', convert_int),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'subject_organization_name', validate_to_none),
        ('extra.', 'subject_organization_unit_name', validate_to_none),
        ('extra.', 'subject_country', validate_to_none),
        ('extra.', 'subject_state_or_province_name', validate_to_none),
        ('extra.', 'subject_locality_name', validate_to_none),
        ('extra.', 'subject_street_address', validate_to_none),
        ('extra.', 'subject_postal_code', validate_to_none),
        ('extra.', 'subject_surname', validate_to_none),
        ('extra.', 'subject_given_name', validate_to_none),
        ('extra.', 'subject_email_address', validate_to_none),
        ('extra.', 'subject_business_category', validate_to_none),
        ('extra.', 'subject_serial_number', validate_to_none),
        ('extra.', 'issuer_organization_name', validate_to_none),
        ('extra.', 'issuer_organization_unit_name', validate_to_none),
        ('extra.', 'issuer_country', validate_to_none),
        ('extra.', 'issuer_state_or_province_name', validate_to_none),
        ('extra.', 'issuer_locality_name', validate_to_none),
        ('extra.', 'issuer_street_address', validate_to_none),
        ('extra.', 'issuer_postal_code', validate_to_none),
        ('extra.', 'issuer_surname', validate_to_none),
        ('extra.', 'issuer_given_name', validate_to_none),
        ('extra.', 'issuer_email_address', validate_to_none),
        ('extra.', 'issuer_business_category', validate_to_none),
        ('extra.', 'issuer_serial_number', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'freak_vulnerable', convert_bool),
        ('extra.', 'freak_cipher_suite', validate_to_none),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'http_response_type', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'http_connection', validate_to_none),
        ('extra.', 'www_authenticate', validate_to_none),
        ('extra.', 'set_cookie', validate_to_none),
        ('extra.', 'server_type', validate_to_none),
        ('extra.', 'content_length', convert_int),
        ('extra.', 'transfer_encoding', validate_to_none),
        ('extra.', 'http_date', convert_date),
        ('extra.', 'cert_valid', convert_bool),
        ('extra.', 'self_signed', convert_bool),
        ('extra.', 'cert_expired', convert_bool),
        ('extra.', 'browser_trusted', convert_bool),
        ('extra.', 'validation_level', validate_to_none),
        ('extra.', 'browser_error', validate_to_none),
        ('extra.', 'tlsv13_support', validate_to_none),
        ('extra.', 'tlsv13_cipher', validate_to_none),
        ('extra.', 'raw_cert', validate_to_none),
        ('extra.', 'raw_cert_chain', validate_to_none),
        ('extra.', 'jarm', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('extra.', 'device_version', validate_to_none),
        ('extra.', 'device_sector', validate_to_none),
        ('extra.', 'page_sha256fp', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'https',
        'classification.identifier': 'ssl-freak',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Ssl-Scan
scan_ssl_poodle = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('extra.', 'handshake', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'cipher_suite', validate_to_none),
        ('extra.', 'ssl_poodle', convert_bool),
        ('extra.', 'cert_length', convert_int),
        ('extra.', 'subject_common_name', validate_to_none),
        ('extra.', 'issuer_common_name', validate_to_none),
        ('extra.', 'cert_issue_date', validate_to_none),
        ('extra.', 'cert_expiration_date', validate_to_none),
        ('extra.', 'sha1_fingerprint', validate_to_none),
        ('extra.', 'cert_serial_number', validate_to_none),
        ('extra.', 'ssl_version', convert_int),
        ('extra.', 'signature_algorithm', validate_to_none),
        ('extra.', 'key_algorithm', validate_to_none),
        ('extra.', 'subject_organization_name', validate_to_none),
        ('extra.', 'subject_organization_unit_name', validate_to_none),
        ('extra.', 'subject_country', validate_to_none),
        ('extra.', 'subject_state_or_province_name', validate_to_none),
        ('extra.', 'subject_locality_name', validate_to_none),
        ('extra.', 'subject_street_address', validate_to_none),
        ('extra.', 'subject_postal_code', validate_to_none),
        ('extra.', 'subject_surname', validate_to_none),
        ('extra.', 'subject_given_name', validate_to_none),
        ('extra.', 'subject_email_address', validate_to_none),
        ('extra.', 'subject_business_category', validate_to_none),
        ('extra.', 'subject_serial_number', validate_to_none),
        ('extra.', 'issuer_organization_name', validate_to_none),
        ('extra.', 'issuer_organization_unit_name', validate_to_none),
        ('extra.', 'issuer_country', validate_to_none),
        ('extra.', 'issuer_state_or_province_name', validate_to_none),
        ('extra.', 'issuer_locality_name', validate_to_none),
        ('extra.', 'issuer_street_address', validate_to_none),
        ('extra.', 'issuer_postal_code', validate_to_none),
        ('extra.', 'issuer_surname', validate_to_none),
        ('extra.', 'issuer_given_name', validate_to_none),
        ('extra.', 'issuer_email_address', validate_to_none),
        ('extra.', 'issuer_business_category', validate_to_none),
        ('extra.', 'issuer_serial_number', validate_to_none),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'sha256_fingerprint', validate_to_none),
        ('extra.', 'sha512_fingerprint', validate_to_none),
        ('extra.', 'md5_fingerprint', validate_to_none),
        ('extra.', 'http_response_type', validate_to_none),
        ('extra.', 'http_code', convert_int),
        ('extra.', 'http_reason', validate_to_none),
        ('extra.', 'content_type', validate_to_none),
        ('extra.', 'http_connection', validate_to_none),
        ('extra.', 'www_authenticate', validate_to_none),
        ('extra.', 'set_cookie', validate_to_none),
        ('extra.', 'server_type', validate_to_none),
        ('extra.', 'content_length', convert_int),
        ('extra.', 'transfer_encoding', validate_to_none),
        ('extra.', 'http_date', convert_date),
        ('extra.', 'cert_valid', convert_bool),
        ('extra.', 'self_signed', convert_bool),
        ('extra.', 'cert_expired', convert_bool),
        ('extra.', 'browser_trusted', convert_bool),
        ('extra.', 'validation_level', validate_to_none),
        ('extra.', 'browser_error', validate_to_none),
        ('extra.', 'tlsv13_support', validate_to_none),
        ('extra.', 'tlsv13_cipher', validate_to_none),
        ('extra.', 'raw_cert', validate_to_none),
        ('extra.', 'raw_cert_chain', validate_to_none),
        ('extra.', 'jarm', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
        ('extra.', 'device_type', validate_to_none),
        ('extra.', 'device_model', validate_to_none),
        ('extra.', 'device_version', validate_to_none),
        ('extra.', 'device_sector', validate_to_none),
        ('extra.', 'page_sha256fp', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'https',
        'classification.identifier': 'ssl-poodle',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-stun-service-report/
scan_stun = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'mapped_port', convert_int),
        ('extra.', 'xor_mapped_port', convert_int),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'transaction_id', validate_to_none),
        ('extra.', 'magic_cookie', validate_to_none),
        ('extra.', 'message_length', convert_int),
        ('extra.', 'message_type', validate_to_none),
        ('extra.', 'mapped_family', validate_to_none),
        ('extra.', 'mapped_address', validate_to_none),
        ('extra.', 'xor_mapped_family', validate_to_none),
        ('extra.', 'xor_mapped_address', validate_to_none),
        ('extra.', 'software', validate_to_none),
        ('extra.', 'fingerprint', validate_to_none),
        ('extra.', 'amplification', convert_float),
        ('extra.', 'response_size', convert_int),
    ],
    'constant_fields': {
        'classification.taxonomy': 'other',
        'classification.type': 'other',
        'protocol.application': 'Session Traversal Utilities for NAT',
        'classification.identifier': 'open-stun',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/synful-scan-report/
scan_synfulknock = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.', 'ack_number', convert_int),
        ('extra.', 'window_size', convert_int),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.', 'sequence_number', validate_to_none),
        ('extra.', 'urgent_pointer', validate_to_none),
        ('extra.', 'tcp_flags', validate_to_none),
        ('extra.', 'raw_packet', validate_to_none),
        ('extra.source.sector', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'classification.identifier': 'open-synfulknock',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-telnet-report/
scan_telnet = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'banner', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'telnet',
        'classification.identifier': 'open-telnet',
    },
}

# https://www.shadowserver.org/wiki/pmwiki.php/Services/Open-TFTP
scan_tftp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'opcode', validate_to_none),
        ('extra.', 'errorcode', validate_to_none),
        ('extra.', 'error', validate_to_none),
        ('extra.', 'errormessage', validate_to_none),
        ('extra.', 'size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'tftp',
        'classification.identifier': 'open-tftp',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/open-ubiquiti-report/
scan_ubiquiti = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('extra.mac_address', 'mac', validate_to_none),
        ('extra.radio_name', 'radioname', validate_to_none),
        ('extra.model', 'modelshort', validate_to_none),
        ('extra.model_full', 'modelfull', validate_to_none),
        ('extra.firmwarerev', 'firmware', validate_to_none),
        ('extra.response_size', 'size', convert_int),
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'essid', validate_to_none),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.identifier': 'accessible-ubiquiti-discovery-service',
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-vnc-report/
scan_vnc = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('source.reverse_dns', 'hostname'),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'product', validate_to_none),
        ('extra.', 'banner', validate_to_none),
        ('extra.', 'sector', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'vnc',
        'protocol.transport': 'tcp',
        'classification.identifier': 'open-vnc',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-ws-discovery-service-report/
scan_ws_discovery = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sic', 'sic', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('extra.', 'response_size', convert_int),
        ('extra.', 'amplification', convert_float),
        ('extra.', 'error', validate_to_none),
        ('extra.', 'raw_response', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'ws-discovery',
        'classification.identifier': 'open-ws-discovery',
    },
}

# https://www.shadowserver.org/what-we-do/network-reporting/accessible-xdmcp-service-report/
scan_xdmcp = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.reverse_dns', 'hostname'),
        ('extra.', 'tag', validate_to_none),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sic', invalidate_zero),
        ('extra.', 'opcode', validate_to_none),
        ('extra.', 'reported_hostname', validate_to_none),
        ('extra.', 'status', validate_to_none),
        ('extra.', 'size', convert_int),
        ('extra.', 'amplification', convert_float),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'protocol.application': 'xdmcp',
        'classification.identifier': 'open-xdmcp',
    },
}

# http://www.shadowserver.org/wiki/pmwiki.php/Services/Spam-URL
spam_url = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
    ],
    'optional_fields': [
        ('source.url', 'url', convert_http_host_and_url, True),
        ('source.fqdn', 'http_host', validate_fqdn),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('extra.', 'naics', invalidate_zero),
        ('extra.', 'sector', validate_to_none),
        ('extra.', 'source', validate_to_none),
        ('extra.', 'sender', validate_to_none),
        ('extra.', 'subject', validate_to_none),
        ('source.ip', 'src_ip', validate_ip),
        ('source.asn', 'src_asn', invalidate_zero),
        ('source.geolocation.cc', 'src_geo'),
        ('source.geolocation.region', 'src_region'),
        ('source.geolocation.city', 'src_city'),
        ('extra.source.naics', 'src_naics', invalidate_zero),
        ('extra.source.sector', 'src_sector', validate_to_none),
        ('malware.hash.md5', 'md5', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'abusive-content',
        'classification.type': 'spam',
        'classification.identifier': 'spam-url',
    },
}

special = {
    'required_fields': [
        ('time.source', 'timestamp', add_UTC_to_timestamp),
        ('source.ip', 'ip', validate_ip),
        ('source.port', 'port', convert_int),
    ],
    'optional_fields': [
        ('protocol.transport', 'protocol'),
        ('source.asn', 'asn', invalidate_zero),
        ('source.geolocation.cc', 'geo'),
        ('source.geolocation.region', 'region'),
        ('source.geolocation.city', 'city'),
        ('source.reverse_dns', 'hostname'),
        ('extra.source.naics', 'naics', invalidate_zero),
        ('extra.source.sector', 'sector', validate_to_none),
        ('malware.name', 'tag'),
        ('extra.', 'public_source', validate_to_none),
        ('extra.', 'status', validate_to_none),
        ('extra.', 'detail', validate_to_none),
        ('extra.', 'method', validate_to_none),
        ('extra.', 'device_vendor', validate_to_none),
    ],
    'constant_fields': {
        'classification.taxonomy': 'vulnerable',
        'classification.type': 'vulnerable-system',
        'classification.identifier': 'special',
    },
}

mapping = (
    # feed name, file name, function
    ('Blocklist', 'blocklist', blocklist),
    ('Compromised-Website', 'compromised_website', compromised_website),
    ('Device-Identification IPv4', 'device_id', device_id),
    ('Device-Identification IPv6', 'device_id6', device_id),
    ('DDoS-Participant', 'event4_ddos_participant', event_ddos_participant),
    ('Honeypot-Brute-Force-Events', 'event4_honeypot_brute_force', event_honeypot_brute_force),
    ('Honeypot-Darknet', 'event4_honeypot_darknet', event_honeypot_darknet),
    ('Honeypot-DDoS', 'event4_honeypot_ddos', event_honeypot_ddos),
    ('Honeypot-Amplification-DDoS-Events', 'event4_honeypot_ddos_amp', event_honeypot_ddos_amp),
    ('Honeypot-DDoS-Target', 'event4_honeypot_ddos_target', event_honeypot_ddos_target),
    ('Honeypot-HTTP-Scan', 'event4_honeypot_http_scan', event_honeypot_http_scan),
    ('Honeypot-ICS-Scanner', 'event4_honeypot_ics_scan', event_honeypot_ics_scan),
    ('IP-Spoofer-Events', 'event4_ip_spoofer', event_ip_spoofer),
    ('Microsoft-Sinkhole-Events IPv4', 'event4_microsoft_sinkhole', event_sinkhole),
    ('Microsoft-Sinkhole-Events-HTTP IPv4', 'event4_microsoft_sinkhole_http', event_sinkhole_http),
    ('Sinkhole-Events IPv4', 'event4_sinkhole', event_sinkhole),
    ('Sinkhole-DNS', 'event4_sinkhole_dns', event_sinkhole_dns),
    ('Sinkhole-Events-HTTP IPv4', 'event4_sinkhole_http', event_sinkhole_http),
    ('Sinkhole-Events-HTTP-Referer IPv4', 'event4_sinkhole_http_referer', event_sinkhole_http_referer),
    ('Sinkhole-Events IPv6', 'event6_sinkhole', event_sinkhole),
    ('Sinkhole-Events-HTTP IPv6', 'event6_sinkhole_http', event_sinkhole_http),
    ('Sinkhole-Events-HTTP-Referer IPv6', 'event6_sinkhole_http_referer', event_sinkhole_http_referer),
    ('Malware-URL', 'malware_url', malware_url),
    ('Phish-URL', 'phish_url', phish_url),
    ('Accessible-HTTP-proxy', 'population_http_proxy', population_http_proxy),
    ('Sandbox-Connections', 'sandbox_conn', sandbox_conn),
    ('Sandbox-DNS', 'sandbox_dns', sandbox_dns),
    ('Sandbox-URL', 'sandbox_url', sandbox_url),
    ('IPv6-Accessible-CWMP', 'scan6_cwmp', scan_cwmp),
    ('IPv6-DNS-Open-Resolvers', 'scan6_dns', scan_dns),
    ('IPv6-Vulnerable-Exchange', 'scan6_exchange', scan_exchange),
    ('IPv6-Accessible-FTP', 'scan6_ftp', scan_ftp),
    ('IPv6-Accessible-HTTP', 'scan6_http', scan_http),
    ('IPv6-Vulnerable-HTTP', 'scan6_http_vulnerable', scan_http_vulnerable),
    ('IPv6-Open-IPP', 'scan6_ipp', scan_ipp),
    ('IPv6-Open-LDAP-TCP', 'scan6_ldap_tcp', scan_ldap_tcp),
    ('IPv6-Open-MQTT', 'scan6_mqtt', scan_mqtt),
    ('IPv6-Open-Anonymous-MQTT', 'scan6_mqtt_anon', scan_mqtt_anon),
    ('IPv6-Accessible-MySQL', 'scan6_mysql', scan_mysql),
    ('IPv6-NTP-Version', 'scan6_ntp', scan_ntp),
    ('IPv6-NTP-Monitor', 'scan6_ntpmonitor', scan_ntpmonitor),
    ('IPv6-Accessible-PostgreSQL', 'scan6_postgres', scan_postgres),
    ('IPv6-Accessible-RDP', 'scan6_rdp', scan_rdp),
    ('IPv6-Accessible-SLP', 'scan6_slp', scan_slp),
    ('IPv6-Accessible-SMB', 'scan6_smb', scan_smb),
    ('IPv6-Accessible-SMTP', 'scan6_smtp', scan_smtp),
    ('IPv6-Vulnerable-SMTP', 'scan6_smtp_vulnerable', scan_smtp_vulnerable),
    ('IPv6-Open-SNMP', 'scan6_snmp', scan_snmp),
    ('IPv6-Accessible-SSH', 'scan6_ssh', scan_ssh),
    ('IPv6-Accessible-SSL', 'scan6_ssl', scan_ssl),
    ('SSL-FREAK-Vulnerable-Servers IPv6', 'scan6_ssl_freak', scan_ssl_freak),
    ('SSL-POODLE-Vulnerable-Servers IPv6', 'scan6_ssl_poodle', scan_ssl_poodle),
    ('IPv6-Accessible-Session-Traversal-Utilities-for-NAT', 'scan6_stun', scan_stun),
    ('IPv6-Accessible-Telnet', 'scan6_telnet', scan_telnet),
    ('IPv6-Accessible-VNC', 'scan6_vnc', scan_vnc),
    ('Accessible-ADB', 'scan_adb', scan_adb),
    ('Accessible-AFP', 'scan_afp', scan_afp),
    ('Accessible-AMQP', 'scan_amqp', scan_amqp),
    ('Accessible-ARD', 'scan_ard', scan_ard),
    ('Open-Chargen', 'scan_chargen', scan_chargen),
    ('Accessible-Cisco-Smart-Install', 'scan_cisco_smart_install', scan_cisco_smart_install),
    ('Accessible-CoAP', 'scan_coap', scan_coap),
    ('Accessible-CouchDB', 'scan_couchdb', scan_couchdb),
    ('Accessible-CWMP', 'scan_cwmp', scan_cwmp),
    ('Open-DB2-Discovery-Service', 'scan_db2', scan_db2),
    ('Vulnerable-DDoS-Middlebox', 'scan_ddos_middlebox', scan_ddos_middlebox),
    ('DNS-Open-Resolvers', 'scan_dns', scan_dns),
    ('Accessible-Docker', 'scan_docker', scan_docker),
    ('Accessible-DVR-DHCPDiscover', 'scan_dvr_dhcpdiscover', scan_dvr_dhcpdiscover),
    ('Open-Elasticsearch', 'scan_elasticsearch', scan_elasticsearch),
    ('Accessible-Erlang-Port-Mapper-Daemon', 'scan_epmd', scan_epmd),
    ('Vulnerable-Exchange-Server', 'scan_exchange', scan_exchange),
    ('Accessible-FTP', 'scan_ftp', scan_ftp),
    ('Accessible-Hadoop', 'scan_hadoop', scan_hadoop),
    ('Accessible-HTTP', 'scan_http', scan_http),
    ('Open-HTTP-proxy', 'scan_http_proxy', scan_http_proxy),
    ('Vulnerable-HTTP', 'scan_http_vulnerable', scan_http_vulnerable),
    ('Accessible-ICS', 'scan_ics', scan_ics),
    ('Open-IPMI', 'scan_ipmi', scan_ipmi),
    ('Open-IPP', 'scan_ipp', scan_ipp),
    ('Vulnerable-ISAKMP', 'scan_isakmp', scan_isakmp),
    ('Accessible-Kubernetes-API', 'scan_kubernetes', scan_kubernetes),
    ('Open-LDAP-TCP', 'scan_ldap_tcp', scan_ldap_tcp),
    ('Open-LDAP', 'scan_ldap_udp', scan_ldap_udp),
    ('Open-mDNS', 'scan_mdns', scan_mdns),
    ('Open-Memcached', 'scan_memcached', scan_memcached),
    ('Open-MongoDB', 'scan_mongodb', scan_mongodb),
    ('Open-MQTT', 'scan_mqtt', scan_mqtt),
    ('Open-Anonymous-MQTT', 'scan_mqtt_anon', scan_mqtt_anon),
    ('Open-MSSQL', 'scan_mssql', scan_mssql),
    ('Accessible-MySQL', 'scan_mysql', scan_mysql),
    ('Open-NATPMP', 'scan_nat_pmp', scan_nat_pmp),
    ('Open-NetBIOS-Nameservice', 'scan_netbios', scan_netbios),
    ('Open-Netis', 'scan_netis_router', scan_netis_router),
    ('NTP-Version', 'scan_ntp', scan_ntp),
    ('NTP-Monitor', 'scan_ntpmonitor', scan_ntpmonitor),
    ('Open-Portmapper', 'scan_portmapper', scan_portmapper),
    ('Accessible-PostgreSQL', 'scan_postgres', scan_postgres),
    ('Open-QOTD', 'scan_qotd', scan_qotd),
    ('Accessible-QUIC', 'scan_quic', scan_quic),
    ('Accessible-Radmin', 'scan_radmin', scan_radmin),
    ('Accessible-RDP', 'scan_rdp', scan_rdp),
    ('Accessible-MS-RDPEUDP', 'scan_rdpeudp', scan_rdpeudp),
    ('Open-Redis', 'scan_redis', scan_redis),
    ('Accessible-Rsync', 'scan_rsync', scan_rsync),
    ('Accessible-SLP', 'scan_slp', scan_slp),
    ('Accessible-SMB', 'scan_smb', scan_smb),
    ('Accessible-SMTP', 'scan_smtp', scan_smtp),
    ('Vulnerable-SMTP', 'scan_smtp_vulnerable', scan_smtp_vulnerable),
    ('Open-SNMP', 'scan_snmp', scan_snmp),
    ('Accessible-SOCKS4/5-Proxy', 'scan_socks', scan_socks),
    ('Open-SSDP', 'scan_ssdp', scan_ssdp),
    ('Accessible-SSH', 'scan_ssh', scan_ssh),
    ('Accessible-SSL', 'scan_ssl', scan_ssl),
    ('SSL-FREAK-Vulnerable-Servers', 'scan_ssl_freak', scan_ssl_freak),
    ('SSL-POODLE-Vulnerable-Servers IPv4', 'scan_ssl_poodle', scan_ssl_poodle),
    ('Accessible-Session-Traversal-Utilities-for-NAT', 'scan_stun', scan_stun),
    ('SYNful-Knock', 'scan_synfulknock', scan_synfulknock),
    ('Accessible-Telnet', 'scan_telnet', scan_telnet),
    ('Open-TFTP', 'scan_tftp', scan_tftp),
    ('Accessible-Ubiquiti-Discovery-Service', 'scan_ubiquiti', scan_ubiquiti),
    ('Accessible-VNC', 'scan_vnc', scan_vnc),
    ('Accessible-WS-Discovery-Service', 'scan_ws_discovery', scan_ws_discovery),
    ('Open-XDMCP', 'scan_xdmcp', scan_xdmcp),
    ('Spam-URL', 'spam_url', spam_url),
    ('Special', 'special', special),
    ('Accessible-RDPEUDP', 'scan_rdpeudp', scan_rdpeudp),
    ('Sinkhole-Events', 'event4_sinkhole', event_sinkhole),
    ('Sinkhole-Events-HTTP', 'event4_sinkhole_http', event_sinkhole_http),
    ('Sinkhole-Events-HTTP-Referer', 'event4_sinkhole_http_referer', event_sinkhole_http_referer),
)
# END CONFGEN

feedname_mapping = {feedname: function for feedname, filename, function in mapping}
filename_mapping = {filename: (feedname, function) for feedname, filename, function in mapping}
