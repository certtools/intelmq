from collections import defaultdict

from intelmq.bots.experts.certbund_contact.eventjson import \
     get_certbund_contacts, set_certbund_directives
import intelmq.bots.experts.certbund_contact.annotations as annotations


class Contact:

    def __init__(self, automation, email, organisation, sector=None,
                 matched_fields=(), annotations=()):
        self.email = email
        self.organisation = organisation
        self.sector = sector
        self.matched_fields = matched_fields
        self.automation = automation
        self.annotations = annotations

    def __repr__(self):
        return ("Contact(automation=%r, email=%r, organisation=%r)"
                % (self.automation, self.email, self.organisation))

    @classmethod
    def from_json(cls, jsondict):
        return cls(automation=jsondict["automation"],
                   email=jsondict["email"],
                   organisation=jsondict["organisation"],
                   sector=jsondict["sector"],
                   matched_fields=jsondict["matched_fields"],
                   annotations=map(annotations.from_json,
                                   jsondict["annotations"]))



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


class Context:

    def __init__(self, event, section):
        self._event = event
        self.section = section
        self.contacts = [Contact.from_json(j)
                         for j in get_certbund_contacts(event, section)]
        self._directives = []

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



def most_specific_contacts(contacts):
    by_source = defaultdict(lambda : {"manual": set(), "automatic": set()})

    for contact in contacts:
        for field in contact.matched_fields:
            by_source[field][contact.automation].add(contact)

    def get_preferred_by_source(key):
        if key not in by_source:
            return set()
        else:
            by_automation = by_source[key]
            return by_automation["manual"] or by_automation["automatic"]

    return list(get_preferred_by_source("fqdn")
                | (get_preferred_by_source("ip")
                   or get_preferred_by_source("asn")))


def notification_inhibited(context):
    """Return whether any inhibition annotation in the contacts matches event.
    """
    return any(annotation.matches(context)
               for contact in context.contacts
               for annotation in contact.annotations
               if isinstance(annotation, annotations.Inhibition))
