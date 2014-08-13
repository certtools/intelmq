import sys
import socket
import datetime
import dateutil.parser as dateparser
from intelmq.bots.utils import is_ip


# Find all domain names values in ip fields
# and move them to domain names fields

def ip(event, *items):
    for ip_key, domain_name_key in items:
        value = event.value(ip_key)
        if value:
            if not is_ip(value):
                event.discard(ip_key, value)
                event.add(domain_name_key, value)
    return event


# Find all ip values in domain names fields
# and move them to ip fields

def domain_name(event, *items):
    for domain_name_key, ip_key in items:
        value = event.value(domain_name_key)
        if value:
            if is_ip(value):
                event.discard(domain_name_key, value)
                event.add(ip_key, value)
    return event


def source_time(event, key):
    value = event.value(key)
    new_value = dateparser.parse(value).isoformat()
    event.discard(key, value)
    event.add(key, new_value)
    return event
        

def generate_source_time(event, key):        
    value = datetime.datetime.utcnow()
    value = value.replace(hour=0,minute=0,second=0,microsecond=0)
    value = value.isoformat()
    event.add(key, value)
    return event


def generate_observation_time(event, key):        
    value = datetime.datetime.utcnow()
    value = value.replace(microsecond=0)
    value = value.isoformat()
    event.add(key, value)
    return event

