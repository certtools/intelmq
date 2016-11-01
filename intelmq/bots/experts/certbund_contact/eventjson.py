"""Helper functions for JSON data stored in the event.
"""


import json


def get_parsed_extra_field(event):
    """Return the value of the extra field as a python dict.
    """
    if "extra" in event:
        return json.loads(event["extra"])
    return {}


def contacts_key(section):
    return section + "_contacts"


def set_certbund_field(event, key, value):
    extra = get_parsed_extra_field(event)
    certbund = extra.setdefault("certbund", {})
    certbund[key] = value
    event.add("extra", extra, force=True)


def set_certbund_contacts(event, section, contacts):
    set_certbund_field(event, contacts_key(section), contacts)
