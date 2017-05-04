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
 - Events of the matter "avalanche" are sent to three different types of receivers
   They are aggregated by ASN, Country-Code or IP-Network
 - Events of the matter Ebury or Mumblehard and from the Feedprovider Shadowserver
   are sent to only one type of receiver, they are always aggregated by ASN

"""

from intelmq.bots.experts.certbund_contact.rulesupport import \
    Directive, most_specific_matches

CTS_TO_WORK_WITH = ['botnet drone']

# A set which is containing information about already logged
# errors to prevent log-flooding
LOGGING_SET = set()

def determine_directives(context):
    context.logger.debug("============= 31ct_botnet-drone.py ===========")

    feed_provider = context.get("feed.provider")
    feed_name = context.get("feed.name")
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

    # Handle the datasets first, which shall only be sent to one group
    # We have two options to deal with the shadowserver datasets.
    #  1. Try to match them because of the feed_name
    #  2. Try to match them becaus of the feed_provider
    # Well take Opt.2 here for demonstration purposes,
    # but you can always switch to the other path

    if feed_provider in ["Shadowserver", "shadowserver"] \
            or feed_name in ["ebury", "mumblehard"]:
        # handle the malware matter.
        add_directives_to_context(context, msm, "malware")
        return True

    elif feed_name == "avalanche":
        # handle the avalanche matter.
        add_directives_to_context(context, msm, "avalanche")
        return True

    else:
        # We don't want to handle this data. Something may not be correct
        # Check if this was already logged to prevent log-flooding:
        if "FPFN-NS_"+feed_provider+"_"+feed_name not in LOGGING_SET:
            LOGGING_SET.add("FPFN-NS_"+feed_provider+"_"+feed_name)
            context.logger.info("Currently there is no rule to generate "
                                "directives for Feed.Provider %s, "
                                "Feed.Name %s",
                                feed_provider, feed_name)

    return


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

        # Based on the assumptions we've made earlier,
        # we use two different paths to generate
        # directives based upon the matter of the event
        if matter == "malware":
            add_malware_directives_to_context(context, match)

        elif matter == "avalanche":
            add_avalanche_directives_to_context(context, match)

        else:
            # Check if this was already logged to prevent log-flooding:
            if "Matter-NS_" + matter not in LOGGING_SET:
                LOGGING_SET.add("Matter-NS_" + matter)
                context.logger.info("Cannot generate directive for matter: %s",
                                    matter)


def add_avalanche_directives_to_context(context, match):
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
                d = create_directive(notification_format="avalanche",
                                     target_group="constituency",
                                     interval=86400,
                                     data_format="avalanche_csv_attachment")
                directive.update(d)
                directive.aggregate_key["cidr"] = match.address
                context.add_directive(directive)

            elif is_government:
                d = create_directive(notification_format="avalanche",
                                     target_group="constituency",
                                     interval=86400,
                                     data_format="avalanche_csv_attachment")
                directive.update(d)
                directive.aggregate_key["cidr"] = match.address
                context.add_directive(directive)

            elif match.field == "geolocation.cc":
                # We know the National CERT that is responsible in this case
                d = create_directive(notification_format="avalanche",
                                     target_group="certs",
                                     interval=0,
                                     data_format="avalanche_csv_attachment")
                directive.update(d)
                # Aggregate by Geolocation.
                directive.aggregate_by_field(context.section + ".geolocation.cc")
                context.add_directive(directive)

            else:
                d = create_directive(notification_format="avalanche",
                                     target_group="provider",
                                     interval=86400,
                                     data_format="avalanche_csv_inline")
                directive.update(d)
                directive.aggregate_by_field(context.section + ".asn")
                context.add_directive(directive)


def add_malware_directives_to_context(context, match):
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
                # dir = create_directive(notification_format="malware-infection",
                #                        target_group="constituency",
                #                       interval=86400,
                #                       data_format="malware-infection_csv_attachment")
                # directive.update(dir)
                # directive.aggregate_key["cidr"] = match.address
                # context.add_directive(directive)

            elif is_government:
                pass  # Right now we are not generating Notifications for this group
                # dir = create_directive(notification_format="malware-infection",
                #                       target_group="constituency",
                #                       interval=86400,
                #                       data_format="malware-infection_csv_attachment")
                # directive.update(dir)
                # directive.aggregate_key["cidr"] = match.address
                # context.add_directive(directive)

            elif match.field == "geolocation.cc":
                pass  # Right now we are not generating Notifications for this group
                # We know the National CERT that is responsible in this case
                # dir = create_directive(notification_format="malware-infection",
                #                       target_group="certs",
                #                       interval=0,
                #                       data_format="malware-infection_csv_attachment")
                # directive.update(dir)
                # Aggregate by Geolocation.
                # directive.aggregate_by_field(context.section + ".geolocation.cc")
                # context.add_directive(directive)

            else:
                d = create_directive(notification_format="malware-infection",
                                     target_group="provider",
                                     interval=86400,
                                     data_format="malware-infection_csv_inline")
                directive.update(d)
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
    return Directive(template_name=notification_format+"_"+target_group,
                     notification_format=notification_format,
                     event_data_format=data_format,
                     notification_interval=interval)
