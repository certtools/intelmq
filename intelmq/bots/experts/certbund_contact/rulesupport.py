from contextlib import contextmanager
from collections import defaultdict
from itertools import chain

from intelmq.bots.experts.certbund_contact.eventjson import \
     get_certbund_contacts, set_certbund_directives
import intelmq.bots.experts.certbund_contact.annotations as annotations


class Organisation:

    """An organisation

    Attributes:
        orgid (int): ID that is used to refer to the organisation from
            the matches and potentially other places.
        name (str): Name of the organisation
        managed (str): Either 'manual' or 'automatic' indicating how the
            contact database entry is managed.
        sector (str): The sector of the organisation (e.g. 'IT',
            'Energe' or similar)
        contacts (list of Contact): The contacts associated with the
            organisation. Notifications related to the organisation
            should be sent to one or more of these.
        annotations (list of Annotation): The annotations associated
            with organisation.
    """



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

    """Contact details.

    Attributes:
        email (str): email address
        is_primary_contact (bool): Whether the contact is the primary
            contact of the organisation with which it is associated.
        managed (str): Either 'manual' or 'automatic' indicating how the
            contact database entry is managed.
        role (str): The role of the contact within the organisation,
            e.g. 'abuse-c'

    """

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

    """A reason why an event matched an entry in the contact database.

    Attributes:

        field (str): The name of the event field that matched

        managed (str): Either 'manual' or 'automatic' indicating how the
            contact database entry is managed.

        organisations (list of int): The IDs of the organisations
            associated with the matching entry

        annotations (list of Annotation): The annotations associated
            with the database match entry. These annotations are the
            ones directly associated with the matching entry in the DB,
            e.g. the ASN entry if the field refers to an ASN. Other
            matches may contain other annotations.

        address (str or None): the network address that matched if the
            field is either 'source.ip' or 'destination.ip'. None
            otherwise.
    """

    def __init__(self, field, managed, organisations, annotations,
                 address=None):
        self.field = field
        self.managed = managed
        self.organisations = organisations
        self.annotations = annotations
        self.address = address

    def __repr__(self):
        return ("Match(field=%r, managed=%r, organisations=%r, annotations=%r,"
                " address=%r)"
                % (self.field, self.managed, self.organisations,
                   self.annotations, self.address))

    def __eq__(self, other):
        return (self.field == other.field
                and self.managed == other.managed
                and self.organisations == other.organisations
                and self.annotations == other.annotations
                and self.address == other.address)

    def __hash__(self):
        return hash((self.field, self.managed, tuple(self.organisations),
                     tuple(self.annotations), self.address))

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
                   annotations=[annotations.from_json(a)
                                for a in jsondict["annotations"]],
                   address=address)




class Directive:

    """Notification directive

    A notification directive indicates to other components, e.g.
    intelmq-mailgen, which notifications should be sent where based on
    the event the directive is associated with.

    Attributes:
        medium (str): The transport medium for the notification.
            So far, only "email" is implemented. More will likely come, such
            as "xmpp"
        recipient_address (str): medium-specific address.
            For email, the email address, obviously.
        aggregate_fields (set of str): Set of event field names that are
            to be part of the aggregate identifier. See aggregation,
            below.
        aggregate_key (dict): Key/value pairs to be part of the
            aggregate identifier. See aggregation, below.
        template_name (str): The name of the template to use. Its meaning
            depends on the notification format
        event_data_format (str): The format to use for event data
            included in the notification. Its meaning depends on the
            notification format.
        notification_interval (int): Interval between notifications for
            similar events. Two events are considered similar in this
            sense if they have equal aggregate identifiers.

    Aggregation
    -----------

    Multiple notification directives may be aggregated into a single
    notification. Directives may only be aggregated when they are
    sufficiently similar. Not only do they have to be sent to the same
    recipient using the same medium and format, often they must also be
    similar enough in other respects, e.g. by being related to the same
    ASN.

    This similarity is defined with the aggregation identifier which is
    conceptually a set of key/value pairs (set in the sense that each
    key must occur only once). Directives with equal aggregation
    identifiers may be aggregated because they are considered to
    sufficiently similar. Some parts of it are implicit, such as a the
    parameters for the more physical aspects of the notification (e.g.
    medium, address, etc.). The other parts have to be handled
    explicitly. In this class this is done with the two attributes
    aggregate_key and aggregate_fields. The former is a dict whose
    contents are simply treated as part of the aggregation identifier.
    The latter is a set of event field names and these names together
    with the corresponding values from the event are also treated as
    part of the aggregation identifier. The aggregate_fields attribute
    is mainly meant for convenience so that one does not have to copy
    the actual attributes explicitly.


    JSON-Representation
    -------------------

    When converted to JSON, a directive is a JSON-Object whose keys and
    values are the public attributes of the Directive instance with the
    exception of aggregate_fields and aggregate_key, which are combined
    into a single dictionary in the obvious way and included in the JSON
    object under the key "aggregate_identifier".
    """

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
        """Create a new directive from a email contact.
        The new directive will define "email" as medium and use the
        contact's email attribute as the recipient_address.
        """
        return cls(recipient_address=contact.email, medium="email", **kw)

    def as_dict_for_event(self, event):
        """Return a dictionary that can be attached to the given event.
        Args:
            event: The event from which to take the values indicated by
                aggregate_fields

        Returns:
            A dict that can be included in the e.g. the event's extra
            dictionary and serialized to JSON in the way described in
            the class doc-string.
        """
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
        """Indicate that aggregation should consider the given event field.
        Args:
            fieldname (str): The name of the event field whose value
                must be equal in two directives if they are to be
                aggregated.

        The fieldname is added to the aggregate_fields attribute.
        """
        self.aggregate_fields.add(fieldname)

    def update(self, directive):
        """Update self with the attributes of another directive.

        Most attributes are simply copied if their value is not None,
        however, for aggregate_fields and aggregate_key the other
        directive's values are added to self's values with the
        respective update method.

        This is useful when writing scripts where one wants to combine
        attributes that depend mainly on the event's contents, e.g.
        which feed it came from or the event's classification, and
        attributes taken from the contact information. For example::

            def determine_directives(context):
                feed_directive = directive_from_feed(context.get("feed.name"))
                if feed_directive is not None:
                    for contact in context.all_contacts():
                        directive = Directive.from_contact(contact)
                        directive.update(feed_directive)
                        context.add_directive(directive)
                return True
        """
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

    """Context given to rule scripts

    The context object provides access to various pieces of information
    the scripts need and collects the directives created by the scripts.
    It's a single object so that it's easy to add more information. We
    only need to add a new attribute to the context instead of add a new
    parameter to all scripts.

    Attributes:
        section (str): Either 'source' when the script is called due to
            matches in the source attributes (source.ip, source.asn,
            ...) or 'destination' when called for matches in the
            destination attributes.
        logger: A logger object that can be used for log output.
        matches: The entries in the contact DB that matched the event
        organisations: The organisation associated with the matches
    """

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
        """Return an iterator over all annotations."""
        for item in chain(self.organisations, self.matches):
            for annotation in item.annotations:
                yield annotation

    def lookup_organisation(self, orgid):
        """Return the organisation with the given ID"""
        return self._organisation_map[orgid]

    def all_contacts(self):
        """Return an iterator over all contacts."""
        for org in self.organisations:
            for contact in org.contacts:
                yield contact

    @property
    def directives(self):
        """Return the directives that have been added to the context"""
        return self._directives

    def __getitem__(self, key):
        """Return the event's value for the key."""
        return self._event[key]

    def get(self, key):
        """Return the event's value for the key if it exists, None otherwise.
        """
        return self._event.get(key)

    def add_directive(self, directive):
        """Add the directive to the context."""
        self._directives.append(directive)

    def get_updated_event(self):
        """Return the event of the context with the directives added"""
        set_certbund_directives(self._event, self.section,
                                [d.as_dict_for_event(self._event)
                                 for d in self._directives])
        return self._event



def most_specific_matches(context):
    """Return the most specific matches from the context"""
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
    """Modify context by removing all but the most specific matches.
    The most specific matches are determined with most_specific_matches.
    All other matches are removed.
    """
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
