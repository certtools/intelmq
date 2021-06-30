..
   SPDX-FileCopyrightText: 2021 IntelMQ-Team
   SPDX-License-Identifier: AGPL-3.0-or-later

##############
Abuse contacts
##############

Sources for abuse-contacts
--------------------------

Sources for domain-based abuse-contacts
---------------------------------------
These bots are very suitable for domain-based abuse-contact queries.
* `RDAP <https://www.icann.org/rdap>`_ expert parses rdap data & adds the data to the intelmq event. Like: domain -> abuse_contact.
* `Trusted Introducer <https://www.trusted-introducer.org/directory/teams.json>`_ Lookup expert: lookup of the national CERT by source.fqdn

Sources for IP address-based abuse-contacts
-------------------------------------------
* Abusix expert
* DO Portal expert
* RIPE expert
* `Trusted Introducer <https://www.trusted-introducer.org/directory/teams.json>`_ Lookup Expert: lookup of the national CERT by source.asn

Generic sources for abuse-contacts
----------------------------------

FIXME Just link each

* Generic DB Lookup expert for local data sources, like tables ASN → abuse_contact or Country Code → abuse_contact
* uWhoisd (for fetching whois-data, not extracting abuse-contact information)

Helpful other bots for pre-processing
-------------------------------------

FIXME Just link each

* ASN lookup expert
* Cymru Whois expert
* Domain suffix expert
* Format field expert
* Gethostbyname expert (resolve *.ip from *.fqdn)
* MaxMind GeoIP expert (lookup Geolocation information for *.ip)
* Reverse DNS expert (resolve *.reverse_dns from *.ip)
* RIPE expert (lookup of *.asn and Geolocation information for (*.ip)
* TOR nodes expert (for filtering out TOR nodes)
* Url2FQDN expert (extract *.fqdn/*.ip from *.url)

Combining the lookup approaches
-------------------------------

FIXME link each

* Filter expert: You lookup process may be different for different types of data. E.g. website-related issues may be better addressed at the domain owner and device-related issues may be better addressed to the hoster.
* Modify expert: Allows you to set values based on filter and also format values based on the value of other fields.
* Sieve expert: Very powerful expert which allows filtering, routing (to different subsequent bots) based on if-expressions . It support set-operations (field value is in list) as well as subnet operations for IP address networks in CIDR notation for the expression-part. You can as well set the abuse-contact directly.
