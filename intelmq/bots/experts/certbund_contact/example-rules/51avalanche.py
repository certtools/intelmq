"""Sample notification rules for the avalanche feed

"""

from intelmq.bots.experts.certbund_contact.rulesupport import \
    Directive, most_specific_matches


def determine_directives(context):
    context.logger.debug("============= 51avalanche.py ===========")

    feedname = context.get("feed.name")
    context.logger.debug("Context Matches: %r", context.matches)
    context.logger.debug("Most Specific Matches: %r",
                         most_specific_matches(context))

    if feedname != "avalanche":
        # This script shall only handle avalanche data.
        return

    if context.section == "destination":
        # We are not interested in notifiying the Destination for this event.
        return

    else:
        # Have a look at the Bots logging output. You may notice a
        # difference: (If you are using the 20prioritize_contacts.py
        # script, there should not be one)
        context.logger.debug("Context Matches: %r", context.matches)
        # This line Logs all existing matches for an event, whilst
        context.logger.debug("Most Specific Matches: %r",
                             most_specific_matches(context))
        # This line will log only those matches which are considered as
        # "most_specific" The SourceCode of
        # intelmq.bots.experts.certbund_contact.rulesupport can tell you
        # more details how this is evaluated. In short: FQDN is more
        # specific than IP than ASN than geolocation.cc (indicating a
        # nat. cert) So we will use the Output of the helper method
        # most_specific_matches to continue:

        msm = most_specific_matches(context)

        # Now we need to determine, who is going to be notified in which way.
        # Remember, this has to be evaluated by mailgen, you need to create some
        # configuration there, too!

        for match in msm:
            # Iterate the matches...
            # Matches tell us the organisations and their contacts that
            # could be determined for a property of the event, such as
            # IP-Address, ASN, CC.

            # do not take care of automatic matches for the moment.
            # TODO Check if you want to do this in production
            # In our Test-Case the skript 06testbetrieb.py should make
            # this piece of code unnecessary. But we want to be sure...
            if match.managed == "automatic":
                context.logger.debug("Skipping automatic match")
                continue

            # Now get the annotations ("Tags") for the match
            # Those annotations belong to the IP, ASN, FQDN or CC entry
            match_annotations = match.annotations

            # Most likely we are not going to need them in this script.
            # For demonstration-purposes we are going to log them anyway:
            context.logger.debug("Annotations for this Match %r",
                                 match_annotations)

            # Also organisations can carry these annotations ("Tags").
            # We don't know them yet, as we'll need to iterate over the
            # orgs to get them.

            # Let's start actually doing things.
            # I moved the decisionsmaking to the function "evaluate_match"
            # As we are in a Loop, this function is called for every match.
            evaluate_match(context, match)

        # After this function has run, there should be some directives
        # in the context
        context.logger.debug("Directives %r", context.directives)

        # End Processing and do not evaluate other directive-scripts
        return True


def evaluate_match(context, match):
    # For demonstration purposes, log some of the information available
    # for decisions here

    # 1) If a match for a FQDN exists,
    if match.field == "fqdn":
        context.logger.debug("Specific FQDN-Match: %r", match)

    # 2) If a match for an IP exist.
    # If an IP-Match exists, the Networks Address is written into
    # the match as "address"
    if match.field == "ip":
        context.logger.debug("Specific IP-Match: %r for Network %s",
                             match, match.address)

    # 3) If a match for an ASN exist,
    if match.field == "asn":
        context.logger.debug("Specific ASN-Match: %r", match)

    # 4) If a match for a CountryCode exists (indicating a national cert),
    if match.field == "geolocation.cc":
        context.logger.debug("Specific Geolocation-Match: %r", match)

    # You could also check how the match was managed here:
    # for instance: if match.managed == "automatic"

    # Let's have a look at the Organisations associated to this match:
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
                directive.update(constituency_contact_directive())
                directive.aggregate_key["cidr"] = match.address
                context.add_directive(directive)

            elif is_government:
                directive.update(constituency_contact_directive())
                directive.aggregate_key["cidr"] = match.address
                context.add_directive(directive)

            elif match.field == "geolocation.cc":
                # We know the National CERT that is responsible in this case
                directive.update(cert_contact_directive())
                # Aggregate by Geolocation.
                directive.aggregate_by_field(context.section + ".geolocation.cc")
                context.add_directive(directive)

            else:
                directive.update(provider_contact_directive())
                directive.aggregate_by_field(context.section + ".asn")
                context.add_directive(directive)


def cert_contact_directive(notification_format="avalanche",
                           data_format="avalanche_csv_attachment", interval=0):
    # Some maybe reasonable defaults
    # CSV Attachment, for testing 0 = immediately is a good choice.
    # In production, daily = 86400 will be better.
    return Directive(template_name="avalanche_certs.txt",
                     notification_format=notification_format,
                     event_data_format=data_format,
                     notification_interval=interval)


def constituency_contact_directive(notification_format="avalanche",
                                   data_format="avalanche_csv_inline",
                                   interval=86400):
    # Some maybe reasonable defaults
    # CSV Attachment, for testing 0 = immediately is a good choice.
    # In production, daily = 86400 will be better.
    return Directive(template_name="avalanche_constituency.txt",
                     notification_format=notification_format,
                     event_data_format=data_format,
                     notification_interval=interval)


def provider_contact_directive(notification_format="avalanche",
                               data_format="avalanche_csv_inline", interval=0):
    # Some maybe reasonable defaults
    # Interval: for testing 0 = immediately is a good choice.
    # In production, daily = 86400 will be better.
    return Directive(template_name="avalanche_provider.txt",
                     notification_format=notification_format,
                     event_data_format=data_format,
                     notification_interval=interval)

