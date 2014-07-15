import sys
import socket
import dateutil.parser as dateparser
import datetime
import sys
from intelmq.lib.utils import *


# Find all domain names values in ip fields
# and move them to domain names fields

def sanitize_ip(event, *items):
    for ip_key, domain_name_key in items:
        value = event.value(ip_key)
        if value:
            if not is_ip(value):
                event.discard(ip_key, value)
                event.add(domain_name_key, value)
    return event


# Find all ip values in domain names fields
# and move them to ip fields

def sanitize_domain_name(event, *items):
    for domain_name_key, ip_key in items:
        value = event.value(domain_name_key)
        if value:
            if is_ip(value):
                event.discard(domain_name_key, value)
                event.add(ip_key, value)
    return event


def sanitize_time(event, key):
    if not event.contains(key):
        value = datetime.datetime.utcnow().isoformat()
        event.add(key, value)
        return event
        
    value = event.value(key)
    new_value = dateparser.parse(value).isoformat()
    event.discard(key, value)
    event.add(key, new_value)
    return event
