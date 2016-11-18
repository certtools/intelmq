from intelmq.bots.experts.certbund_contact.eventjson import \
     get_certbund_contacts, set_certbund_directives


class Contact:

    def __init__(self, automation, email, organisation, sector=None,
                 matched_fields=()):
        self.email = email
        self.organisation = organisation
        self.sector = sector
        self.matched_fields = matched_fields
        self.automation = automation

    def __repr__(self):
        return ("Contact(automation=%r, email=%r, organisation=%r)"
                % (self.automation, self.email, self.organisation))

    @classmethod
    def from_json(cls, jsondict):
        return cls(automation=jsondict["automation"],
                   email=jsondict["email"],
                   organisation=jsondict["organisation"],
                   sector=jsondict["sector"],
                   matched_fields=jsondict["matched_fields"])


class Directive:

    def __init__(self, medium=None, recipient_address=None, template_name=None,
                 event_data_format=None, notification_interval=None):
        self.medium = medium
        self.recipient_address = recipient_address
        self.template_name = template_name
        self.event_data_format = event_data_format
        self.notification_interval = notification_interval

    def __repr__(self):
        return ("Directive(medium={medium},"
                " recipient_address={recipient_address},"
                " template_name={template_name},"
                " event_data_format={event_data_format},"
                " notification_interval={notification_interval}"
                .format(**self.__dict__))

    @classmethod
    def from_contact(cls, contact, **kw):
        return cls(recipient_address=contact.email, medium="email", **kw)

    def as_dict_for_event(self, event):
        return dict(medium=self.medium,
                    recipient_address=self.recipient_address,
                    template_name=self.template_name,
                    event_data_format=self.event_data_format,
                    notification_interval=self.notification_interval)


    def update(self, directive):
        for attr in ["medium", "recipient_address", "template_name",
                     "event_data_format", "notification_interval"]:
            new = getattr(directive, attr)
            if new is not None:
                setattr(self, attr, new)


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
