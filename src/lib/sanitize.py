import sys
import socket
import dateutil.parser as dateparser
import datetime
import sys
from lib.utils import *


# Find all domain names values in ip fields
# and move them to domain names fields

def sanitize_ip(event, *items):
    for ip_key, domain_name_key in items:
        if event.contains(ip_key):
            for value in event.values(ip_key):
                if not is_ip(value):
                    event.discard(ip_key, value)
                    event.add(domain_name_key, value)
    return event


# Find all ip values in domain names fields
# and move them to ip fields

def sanitize_domain_name(event, *items):
    for domain_name_key, ip_key in items:
        if event.contains(domain_name_key):
            for value in event.values(domain_name_key):
                if is_ip(value):
                    event.discard(domain_name_key, value)
                    event.add(ip_key, value)
    return event


def sanitize_time(event, key):
    if not event.contains(key):
        value = datetime.datetime.utcnow().isoformat()
        event.add(key, value)
        return event
        
    for value in event.values(key):
        new_value = parser.parse(value).isoformat()
        event.discard(key, value)
        event.add(key, new_value)
    
    return event


# Create multiple events per 'split_keys' because
# for each event their can be only one value per 'split_keys'
# Example: one event can just have one ip address.

def split_event_by_keys(event, split_keys):
    events = list()
    for split_key in split_keys:
        if event.contains(split_key):
            values = event.values(split_key)
            if values:
                for value in values:
                    event.clear(split_key)  # Need Improvement
                    event.add(split_key, value)
                    events.append(event)
    return events
