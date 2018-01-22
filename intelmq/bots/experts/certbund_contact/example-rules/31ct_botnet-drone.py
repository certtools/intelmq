"""Sample Rules to generate directives from Events
which are classified as 'botnet drone'

Note: Currently there is no such thing in IntelMQ like a
classification.type 'malware-infected' so 'botnet drone' is
the best way to deal with these datasets for now.

This script is supposed to handle events from:
 - Shadowserver Botnet-Drone-Hadoop, Sinkhole-HTTP-Drone, Microsoft-Sinkhole
 - Ebury
 - Mumblehard
 - Avalanche

Assumptions:
 - Events of the matter "avalanche", "ebury" or "mumblehard" are sent to three different types of receivers
   They are aggregated by ASN, Country-Code or IP-Network. Providers, and Constituencies and CERTs
   are the receivers.
 - Events of more generic matters, like those of the Feedprovider Shadowserver
   are sent to only two types of receivers: Providers, and Constituencies

"""

from intelmq.bots.experts.certbund_contact.rulesupport import \
    Directive, most_specific_matches

CTS_TO_WORK_WITH = ['botnet drone']

GOVERNMENT_ANNOTATION = 'government'
CRITICAL_ANNOTATION = 'critical'

SPECIAL_MATTERS = ['avalanche',
                   'ebury',
                   'mumblehard'
                   ]

# A set which is containing information about already logged
# errors to prevent log-flooding
LOGGING_SET = set()


def determine_directives(context):
    context.logger.debug("============= 31ct_botnet-drone.py ===========")

    feed_name = context.get("feed.name")  # This could also be the classification.identier.
    # It should work the same way.
    classification_type = context.get("classification.type")

    if classification_type not in CTS_TO_WORK_WITH:
        context.logger.debug("This CT is not supported by 31ct_botnet-drone.py: %s",
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

    if feed_name in SPECIAL_MATTERS:
        # handle the ebury matter.
        add_directives_to_context(context, msm, feed_name)
        return True

    else:
        # The Feed-Provider is most likely Shadowserver or
        # the feed carries a less specific information.
        add_directives_to_context(context, msm, "malware-infection")
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

        add_matter_directives_to_context(context, match, matter)


def add_matter_directives_to_context(context, match, matter):
    # This is Copy and Paste from 51avalanche.py, with some
    # minor edits
    # Let's have a look at the Organisations associated to this match:
    for org in context.organisations_for_match(match):

        # Determine the Annotations for this Org.
        org_annotations = org.annotations
        context.logger.debug("Org Annotations: %r" % org_annotations)

        is_government = False
        is_critical = False

        for annotation in org_annotations:
            if annotation.tag == GOVERNMENT_ANNOTATION:
                is_government = True
            if annotation.tag == CRITICAL_ANNOTATION:
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
                d = create_directive(notification_format=matter,
                                     target_group="constituency",
                                     interval=3600,
                                     data_format=matter + "_csv_attachment")
                directive.update(d)
                if matter in SPECIAL_MATTERS:
                    # Add the observation time as an aggregation identifier,
                    # in order to cluster all events from the same report-batch.
                    # But only do so for those Events which have not been associated
                    # to the generic malware-infection matter (see line 78)
                    directive.aggregate_by_field("time.observation")
                # Always aggregate by the network
                directive.aggregate_key["cidr"] = match.address
                context.add_directive(directive)

            elif is_government:
                d = create_directive(notification_format=matter,
                                     target_group="constituency",
                                     interval=3600,
                                     data_format=matter + "_csv_attachment")
                directive.update(d)
                if matter in SPECIAL_MATTERS:
                    # Add the observation time as an aggregation identifier,
                    # in order to cluster all events from the same report-batch.
                    # But only do so for those Events which have not been associated
                    # to the generic malware-infection matter (see line 78)
                    directive.aggregate_by_field("time.observation")
                # Always aggregate by the network
                directive.aggregate_key["cidr"] = match.address
                context.add_directive(directive)

            elif match.field == "geolocation.cc":
                if matter not in SPECIAL_MATTERS:
                    # Do NOT send malware-infection events to CERTs
                    pass

                else:
                    # We know the National CERT that is responsible in this case
                    d = create_directive(notification_format=matter,
                                         target_group="certs",
                                         interval=86400,
                                         data_format=matter + "_csv_attachment")
                    directive.update(d)

                    # Add the observation time as an aggregation identifier,
                    # in order to cluster all events from the same report-batch.
                    directive.aggregate_by_field("time.observation")

                    # Aggregate by Geolocation.
                    directive.aggregate_by_field(context.section + ".geolocation.cc")
                    context.add_directive(directive)

            else:
                d = create_directive(notification_format=matter,
                                     target_group="provider",
                                     interval=86400,
                                     data_format=matter + "_csv_inline")
                directive.update(d)
                if matter in SPECIAL_MATTERS:
                    # Add the observation time as an aggregation identifier,
                    # in order to cluster all events from the same report-batch.
                    # But only do so for those Events which have not been associated
                    # to the generic malware-infection matter (see line 78)
                    directive.aggregate_by_field("time.observation")
                # Always aggregate by ASN
                directive.aggregate_by_field(context.section + ".asn")
                context.add_directive(directive)


def create_directive(notification_format, target_group, interval, data_format):
    """
    This method is NOT designed, to be compatible with the existing configuration
    of mailgen. You MUST can adapt Mailgen-config in order to be capable
    of processing this directive.
    it creates Directives looking like:
    template_name: malware-infection_provider
    notification_format: malware-infection
    notification_interval: 86400
    data_format: malware_csv_inline

    """
    return Directive(template_name=notification_format + "_" + target_group,
                     notification_format=notification_format,
                     event_data_format=data_format,
                     notification_interval=interval)
