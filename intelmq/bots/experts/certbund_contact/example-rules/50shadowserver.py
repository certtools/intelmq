"""Sample notification rules for shadowserver feeds.

The notitification directives are determined based on the feed.name
attribute of the event.
"""

from intelmq.bots.experts.certbund_contact.rulesupport import Directive


def determine_directives(context):
    if context.section == "destination":
        return

    # Find out which Shadowserver configuaration shall be used.
    # Usually the feed.name is set by the parser of the shadowserver data.
    shadowserver_params = shadowserver_mapping.get(context.get("feed.name"))

    if shadowserver_params is not None:
        # This Script does only handle the feeds, that can be determined by the
        # configuration in the shadowserver_mapping dict below.

        # Have a look at the much more sophisticated 51avalanche.py
        # to find out more about different kinds of configuration possibilities,
        # such as annotations, or "matches".

        # TODO This way of generating directives is most likely underdesigned,
        # as a more sophisticated way, like in 51avalanche.py is usually required
        for contact in context.all_contacts():
            directive = Directive.from_contact(contact)
            directive.update(shadowserver_params)
            directive.aggregate_by_field(context.section + ".asn")
            context.add_directive(directive)
        return True

    return


def shadowserver_csv_entry(basename):
    return Directive(template_name="shadowserver_csv_" + basename,
                     notification_format="shadowserver",
                     event_data_format="csv_" + basename,
                     notification_interval=86400)


# map shadowserver feed.name to settings
shadowserver_mapping = {
    "DNS-open-resolvers": shadowserver_csv_entry("DNS-open-resolvers"),
    "Open-Portmapper": shadowserver_csv_entry("Open-Portmapper"),
    "Open-SNMP": shadowserver_csv_entry("Open-SNMP"),
    "Open-MSSQL": shadowserver_csv_entry("Open-MSSQL"),
    "Open-MongoDB": shadowserver_csv_entry("Open-MongoDB"),
    "Open-Chargen": shadowserver_csv_entry("Open-Chargen"),
    "Open-IPMI": shadowserver_csv_entry("Open-IPMI"),
    "Open-NetBIOS": shadowserver_csv_entry("Open-NetBIOS"),
    "NTP-Monitor": shadowserver_csv_entry("NTP-Monitor"),
    "Open-Elasticsearch": shadowserver_csv_entry("Open-Elasticsearch"),
    "Open-mDNS": shadowserver_csv_entry("Open-mDNS"),
    "Open-Memcached": shadowserver_csv_entry("Open-Memcached"),
    "Open-Redis": shadowserver_csv_entry("Open-Redis"),
    "Open-SSDP": shadowserver_csv_entry("Open-SSDP"),
    "Ssl-Freak-Scan": shadowserver_csv_entry("Ssl-Freak-Scan"),
    "Ssl-Scan": shadowserver_csv_entry("Ssl-Scan"),
}
