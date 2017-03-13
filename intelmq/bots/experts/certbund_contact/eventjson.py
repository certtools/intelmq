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


def directives_key(section):
    return section + "_directives"


def set_certbund_field(event, key, value):
    extra = get_parsed_extra_field(event)
    certbund = extra.setdefault("certbund", {})
    certbund[key] = value
    event.add("extra", extra, force=True)


def get_certbund_field(event):
    return get_parsed_extra_field(event).get("certbund", {})


def set_certbund_contacts(event, section, contacts):
    set_certbund_field(event, contacts_key(section), contacts)


def get_certbund_contacts(event, section):
    return get_certbund_field(event).get(contacts_key(section), [])


def set_certbund_directives(event, section, directives):
    set_certbund_field(event, directives_key(section), directives)


def get_certbund_directives(event, section):
    return get_certbund_field(event).get(directives_key(section), [])
