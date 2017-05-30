"""Sample Rules to generate directives from Events
which are classified as 'vulnerable'


This script is supposed to handle events from:
 - Shadowserver Open* Feeds
 - Owncloud and Nextcloud data

Assumptions:
 - Events which are part of the "vulnerable service" type
   carry different classification.identifiers, thus the different
   types of vulnerabilities can be distinguished.

"""

from intelmq.bots.experts.certbund_contact.rulesupport import \
    Directive, most_specific_matches

CTS_TO_WORK_WITH = ['vulnerable service']


SUPPORTED_CLASSIFICATION_IDENTIFIERS = ['openportmapper',
                                        'openmemcached',
                                        'openelasticsearch',
                                        'openntp',
                                        'opendns',
                                        'openmssql',
                                        'opensnmp',
                                        'openmongodb',
                                        'openmdns',
                                        # 'openipmi',
                                        # 'openchargen',
                                        'openssdp',
                                        'openredis',
                                        'openldap',
                                        'opennetbios',
                                        # 'nextcloud',
                                        # 'owncloud',
                                        # 'SSL-FREAK',
                                        # 'SSL-Poodle'
                                        ]

# A set which is containing information about already logged
# errors to prevent log-flooding
LOGGING_SET = set()


def determine_directives(context):
    context.logger.debug("============= 32ct_vulnerable-service.py ===========")

    classification_identifier = context.get("classification.identifier")
    classification_type = context.get("classification.type")

    if classification_type not in CTS_TO_WORK_WITH:
        context.logger.debug("This CT is not supported by 32ct_vulnerable-service.py: %s",
                             classification_type)
        return

    if context.section == "destination":
        # We are not interested in notifying the contact for the destination of this event.
        return

    # write the most specific matches into a variable. See
    # 51avalanche.py for a more detailled description.
    msm = most_specific_matches(context)

    # Debugging Output about the Context.
    context.logger.debug("Context Matches: %r", context.matches)
    context.logger.debug("Most Specific Matches: %r",
                         most_specific_matches(context))

    if not msm:
        context.logger.debug("There are no matches I'm willing to process.")
        return

    if classification_identifier not in SUPPORTED_CLASSIFICATION_IDENTIFIERS:
        # We don't want to handle this data. Something may not be correct
        # Check if this was already logged to prevent log-flooding:
        if classification_identifier is None:
            classification_identifier = "NONE-TYPE"

        if "CI-NS_"+classification_identifier not in LOGGING_SET:
            LOGGING_SET.add("CI-NS_"+classification_identifier)
            context.logger.info("The Classification Identifier %s "
                                "might not be supported, yet.",
                                classification_identifier)
        return

    # Always convert the classification.identifier to lowercase from now
    # on. This makes dealing with templates much easier.
    # Also: Make sure the CI does not contain underscores.
    new_ci = classification_identifier.lower().replace("_", "-")
    add_directives_to_context(context, msm, new_ci)
    return True


def add_directives_to_context(context, matches, matter):
    # Generate Directives from the matches

    context.logger.debug(matches)
    for match in matches:
        # Iterate the matches...
        # Matches tell us the organisations and their contacts that
        # could be determined for a property of the event, such as
        # IP-Address, ASN, CC.
        # It can happen that one organisation has multiple matches for
        # the same criterion (for instance IP - address),
        # this happens due to overlapping networks in the
        # contactdb

        # do not take care of automatic matches for the moment.
        # TODO Check if you want to do this in production
        # In our Test-Case the skript 06testbetrieb.py should make
        # this piece of code unnecessary. But we want to be sure...
        if match.managed == "automatic":
            context.logger.debug("Skipping automatic match")
            continue

        add_vulnerable_directives_to_context(context, match, matter)


def add_vulnerable_directives_to_context(context, match, matter):
    # Let's have a look at the Organisations associated to this match:
    context.logger.debug(context.organisations_for_match(match))
    for org in context.organisations_for_match(match):
        # Determine the Annotations for this Org.
        org_annotations = org.annotations
        context.logger.debug("Org Annotations: %r" % org_annotations)

        is_government = False
        is_critical = False

        for annotation in org_annotations:
            if annotation.tag == "government":
                is_government = True
            if annotation.tag == "critical":
                is_critical = True

        # Now create the Directives
        #
        # An organisation may have multiple contacts, so we need to
        # iterate over them. In many cases this will only loop once as
        # many organisations will have only one.
        for contact in org.contacts:
            directive = Directive.from_contact(contact)
            # Doing this defines "email" as medium and uses the
            # contact's email attribute as the recipient_address.
            # One could also do this by hand, see Directive in
            # intelmq.bots.experts.certbund_contact.rulesupport
            # If you like to know more details

            # Now fill in more details of the directive, depending on
            # the annotations of the directive and/or the type of the
            # match

            if is_critical:
                pass  # Right now we are not generating Notifications for this group

            elif is_government:
                pass  # Right now we are not generating Notifications for this group

            elif match.field == "geolocation.cc":
                pass  # Right now we are not generating Notifications for this group

            else:
                d = create_directive(notification_format="vulnerable-service",
                                     matter=matter,
                                     target_group="provider",
                                     interval=86400,
                                     data_format=matter + "_csv_inline")
                directive.update(d)
                directive.aggregate_by_field(context.section + ".asn")
                context.add_directive(directive)


def create_directive(notification_format, matter, target_group, interval, data_format):
    """
    This method creates Directives looking like:
    template_name: openportmapper_provider
    notification_format: vulnerable-service
    notification_interval: 86400
    data_format: openportmapper_csv_inline

    """
    return Directive(template_name=matter+"_"+target_group,
                     notification_format=notification_format,
                     event_data_format=data_format,
                     notification_interval=interval)
