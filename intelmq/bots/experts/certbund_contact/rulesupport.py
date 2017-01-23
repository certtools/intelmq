from contextlib import contextmanager
from collections import defaultdict

from intelmq.bots.experts.certbund_contact.eventjson import \
     get_certbund_contacts, set_certbund_directives
import intelmq.bots.experts.certbund_contact.annotations as annotations


class Organisation:

    def __init__(self, orgid, name, managed, sector, contacts, annotations):
        self.orgid = orgid
        self.name = name
        self.managed = managed
        self.sector = sector
        self.contacts = contacts
        self.annotations = annotations

    @classmethod
    def from_json(cls, jsondict):
        return cls(orgid=jsondict["id"],
                   name=jsondict["name"],
                   managed=jsondict["managed"],
                   sector=jsondict["sector"],
                   contacts=[Contact.from_json(c)
                             for c in jsondict["contacts"]],
                   annotations=[annotations.from_json(a)
                                for a in jsondict["annotations"]])


class Contact:

    def __init__(self, email, is_primary_contact, managed, role):
        self.email = email
        self.is_primary_contact= is_primary_contact
        self.managed = managed
        self.role = role

    def __repr__(self):
        return ("Contact(email=%r, is_primary_contact=%r, managed=%r, role=%r)"
                % (self.email, self.is_primary_contact, self.managed,
                   self.role))

    @classmethod
    def from_json(cls, jsondict):
        return cls(email=jsondict["email"],
                   is_primary_contact=jsondict["is_primary_contact"],
                   managed=jsondict["managed"],
                   role=jsondict["role"])


class Match:

    def __init__(self, field, managed, organisations, address=None):
        self.field = field
        self.managed = managed
        self.organisations = organisations
        self.address = address

    def __repr__(self):
        return ("Match(field=%r, managed=%r, organisations=%r, address=%r)"
                % (self.field, self.managed, self.organisations, self.address))

    def __eq__(self, other):
        return (self.field == other.field
                and self.managed == other.managed
                and self.organisations == other.organisations
                and self.address == other.address)

    def __hash__(self):
        return hash((self.field, self.managed, tuple(self.organisations),
                     self.address))

    @classmethod
    def from_json(cls, jsondict):
        field = jsondict["field"]
        if field == "ip":
            address = jsondict["address"]
        else:
            address = None
        return cls(field=field,
                   managed=jsondict["managed"],
                   organisations=jsondict["organisations"],
                   address=address)




class Directive:

    def __init__(self, medium=None, recipient_address=None,
                 aggregate_fields=(), aggregate_key=(), template_name=None,
                 event_data_format=None, notification_interval=None):
        self.medium = medium
        self.recipient_address = recipient_address
        self.template_name = template_name
        self.event_data_format = event_data_format
        self.notification_interval = notification_interval
        self.aggregate_fields = set(aggregate_fields)
        self.aggregate_key = dict(aggregate_key)

    def __repr__(self):
        return ("Directive(medium={medium},"
                " recipient_address={recipient_address},"
                " aggregate_fields={aggregate_fields},"
                " aggregate_key={aggregate_key},"
                " template_name={template_name},"
                " event_data_format={event_data_format},"
                " notification_interval={notification_interval}"
                .format(**self.__dict__))

    def __eq__(self, other):
        return (self.medium == other.medium
                and self.recipient_address == other.recipient_address
                and self.aggregate_fields == other.aggregate_fields
                and self.aggregate_key == other.aggregate_key
                and self.template_name == other.template_name
                and self.event_data_format == other.event_data_format
                and self.notification_interval == other.notification_interval)

    def __hash__(self):
        return hash((self.medium,
                     self.recipient_address,
                     self.aggregate_fields,
                     self.aggregate_key,
                     self.template_name,
                     self.event_data_format,
                     self.notification_interval))

    @classmethod
    def from_contact(cls, contact, **kw):
        return cls(recipient_address=contact.email, medium="email", **kw)

    def as_dict_for_event(self, event):
        aggregate_identifier = self.aggregate_key.copy()
        for field in self.aggregate_fields:
            aggregate_identifier[field] = event.get(field)

        return dict(medium=self.medium,
                    recipient_address=self.recipient_address,
                    template_name=self.template_name,
                    event_data_format=self.event_data_format,
                    notification_interval=self.notification_interval,
                    aggregate_identifier=aggregate_identifier)


    def aggregate_by_field(self, fieldname):
        self.aggregate_fields.add(fieldname)

    def update(self, directive):
        for attr in ["medium", "recipient_address", "template_name",
                     "event_data_format", "notification_interval"]:
            new = getattr(directive, attr)
            if new is not None:
                setattr(self, attr, new)
        self.aggregate_fields.update(directive.aggregate_fields)
        self.aggregate_key.update(directive.aggregate_key)


def contact_info_from_json(jsondict):
    return ([Match.from_json(m) for m in jsondict["matches"]],
            [Organisation.from_json(o) for o in jsondict["organisations"]])


class Context:

    def __init__(self, event, section, base_logger):
        self._event = event
        self.section = section
        # base_logger should only be None for testing purposes.
        self.logger = (base_logger.getChild("script") if base_logger is not None
                       else None)
        self.matches, self.organisations = \
              contact_info_from_json(get_certbund_contacts(event, section))
        self._directives = []
        self._organisation_map = {org.orgid: org
                                  for org in self.organisations}

    def all_annotations(self):
        """Return an iterator over all contact annotations."""
        for organisation in self.organisations:
            for annotation in organisation.annotations:
                yield annotation

    def lookup_organisation(self, orgid):
        return self._organisation_map[orgid]

    def all_contacts(self):
        for org in self.organisations:
            for contact in org.contacts:
                yield contact

    @property
    def directives(self):
        return self._directives

    def __getitem__(self, key):
        return self._event[key]

    def get(self, key):
        return self._event.get(key)

    def add_directive(self, directive):
        self._directives.append(directive)

    def get_updated_event(self):
        set_certbund_directives(self._event, self.section,
                                [d.as_dict_for_event(self._event)
                                 for d in self._directives])
        return self._event



def most_specific_matches(context):
    by_field = defaultdict(lambda : {"manual": set(), "automatic": set()})

    for match in context.matches:
        by_field[match.field][match.managed].add(match)

    def get_preferred_by_field(field):
        if field not in by_field:
            return set()
        else:
            by_managed = by_field[field]
            return by_managed["manual"] or by_managed["automatic"]

    return (get_preferred_by_field("fqdn")
            | (get_preferred_by_field("ip") or get_preferred_by_field("asn")))


def keep_most_specific_contacts(context):
    orgids = set()
    matches = most_specific_matches(context)
    for match in matches:
        orgids |= set(match.organisations)
    for organisation in context.organisations:
        if organisation.orgid in orgids:
            primary = []
            other = []
            for contact in organisation.contacts:
                if contact.is_primary_contact:
                    primary.append(contact)
                else:
                    other.append(contact)
            if primary:
                keep = primary
            else:
                keep = other
        else:
            keep = []
        organisation.contacts = keep


def notification_inhibited(context):
    """Return whether any inhibition annotation in the contacts matches event.
    """
    return any(annotation.matches(context)
               for annotation in context.all_annotations()
               if isinstance(annotation, annotations.Inhibition))
