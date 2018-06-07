"""Helper functions for JSON data stored in the event.


Copyright (C) 2016, 2017 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH

This program is Free Software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/agpl.html>.

Author(s):
    Bernhard Herzog <bernhard.herzog@intevation.de>
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
    event.add("extra", extra, overwrite=True)


def del_certbund_field(event, key):
    extra = get_parsed_extra_field(event)
    certbund = extra.get("certbund")
    if certbund is not None and key in certbund:
        del certbund[key]
    event.add("extra", extra, force=True)


def get_certbund_field(event):
    return get_parsed_extra_field(event).get("certbund", {})


def set_certbund_contacts(event, section, contacts):
    set_certbund_field(event, contacts_key(section), contacts)


def get_certbund_contacts(event, section):
    """Return the contact data associated with the event for a section.
    The section should be either 'destination' or 'source'. If the event
    does not have contact information for the section, this function
    returns empty contact information.
    """
    return get_certbund_field(event).get(contacts_key(section),
                                         {"matches": [], "organisations": []})


def del_certbund_contacts(event, section):
    del_certbund_field(event, contacts_key(section))


def set_certbund_directives(event, section, directives):
    set_certbund_field(event, directives_key(section), directives)


def get_certbund_directives(event, section):
    return get_certbund_field(event).get(directives_key(section), [])
