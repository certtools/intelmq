..
   SPDX-FileCopyrightText: 2021 IntelMQ-Team
   SPDX-License-Identifier: AGPL-3.0-or-later

######################
Abuse-contact look-ups
######################

The right decision whom to contact about a specific incident is vital to get the
incident resolved as quick as possible.
Different types of events may required different abuse-contact to be selected.
For example, issues about a device, e.g. a vulnerability in the operating system
or an application, is better sent to the hoster which can inform the server
administrator.
For website-related issues, like defacements or phishing, the domain owner
(maintaining the content of the website) could be the better and more direct
contact.
Additionally, different CERT's have different approaches and different contact
databases.
Multiple information sources have different information, and some sources are
more accurate than others.
IntelMQ can query multiple sources of abuse-contacts and combine them.
Internal databases, like a Constituency Portal (see :doc:`ecosystem`)
provide high-quality and first-hand contact information.
The RIPE document `Sources of Abuse Contact Information for Abuse Handlers <https://www.ripe.net/publications/docs/ripe-658>`_
contains a good summary of the complex of themes.

Sources for abuse-contacts
--------------------------

All these bots add the queried contacts to the IntelMQ events in the field
`source.abuse_contact` if not state otherwise in the documentation.

Sources for domain-based abuse-contacts
---------------------------------------

These bots are suitable for domain-based abuse-contact look-ups.

* :ref:`intelmq.bots.experts.rdap.expert` expert queries private and public RDAP servers for `source.fqdn` and add the contact information to the event as `source.abuse_contact`.
* :ref:`intelmq.bots.experts.trusted_introducer_lookup.expert` expert
  queries a locally cached
  `Trusted Introducer team directory <https://www.trusted-introducer.org/directory/teams.json>`_
  for the TLD or domain (first match) of *source.fqdn*.

Sources for IP address-based abuse-contacts
-------------------------------------------

These bots are suitable for IP address- and ASN-based abuse-contact look-ups.

* :ref:`intelmq.bots.experts.abusix.expert` expert queries the online Abusix service.
* :ref:`intelmq.bots.experts.do_portal.expert` expert queries an instance of the do-portal software (deprecated).
* :ref:`intelmq.bots.experts.tuency.expert` expert queries an instance of the
  *tuency* Constituency Portal for the IP address. The Portal also takes into
  account any notification rules, which are saved additionally in the event.
* :ref:`intelmq.bots.experts.ripe.expert` expert queries the online RIPE database for IP-Address and AS contacts.
* :ref:`intelmq.bots.experts.trusted_introducer_lookup.expert` expert
  queries a locally cached
  `Trusted Introducer team directory <https://www.trusted-introducer.org/directory/teams.json>`_
  for the Autonomous system *source.asn*.

Generic sources for abuse-contacts
----------------------------------

* :ref:`intelmq.bots.experts.generic_db_lookup.expert` expert for local data
  sources, like database tables mapping ASNs to abuse-contact or Country Codes
  to abuse-contact.
* :ref:`intelmq.bots.experts.uwhoisd.expert` expert for fetching whois-data,
  not extracting abuse-contact information

Helpful other bots for pre-processing
-------------------------------------

* :ref:`intelmq.bots.experts.asn_lookup.expert`
* :ref:`intelmq.bots.experts.cymru_whois.expert` to lookup ASN, Geolocation, and BGP prefix for ``*.ip``.
* :ref:`intelmq.bots.experts.domain_suffix.expert` to lookup the public suffix of the domain in ``*.fqdn``.
* :ref:`intelmq.bots.experts.format_field.expert`
* :ref:`intelmq.bots.experts.gethostbyname.expert` resolve ``*.ip`` from ``*.fqdn``.
* :ref:`intelmq.bots.experts.maxmind_geoip.expert` to lookup Geolocation information for ``*.ip``.
* :ref:`intelmq.bots.experts.reverse_dns.expert` to resolve ``*.reverse_dns`` from ``*.ip``.
* :ref:`intelmq.bots.experts.ripe.expert` to lookup ``*.asn`` and Geolocation information for ``*.ip``.
* :ref:`intelmq.bots.experts.tor_nodes.expert` for filtering out TOR nodes.
* :ref:`intelmq.bots.experts.url2fqdn.expert` to extract ``*.fqdn``/``*.ip`` from ``*.url``.

Combining the lookup approaches
-------------------------------

In order to get the best contact, it may be necessary to combine multiple
abuse-contact sources.
IntelMQ's modularity provides methods to arrange and configure the bots as
needed.
Among others, the following bots can help in getting the best result:

* :ref:`intelmq.bots.experts.filter.expert` expert: Your lookup process may be
  different for different types of data. E.g. website-related issues may be
  better addressed at the domain owner and device-related issues may be better
  addressed to the hoster.
* :ref:`intelmq.bots.experts.modify.expert` expert: Allows you to set values
  based on filter and also format values based on the value of other fields.
* :ref:`intelmq.bots.experts.sieve.expert` expert: Very powerful expert which
  allows filtering, routing (to different subsequent bots) based on
  if-expressions . It support set-operations (field value is in list) as well as
  sub-network operations for IP address networks in CIDR notation for the
  expression-part. You can as well set the abuse-contact directly.
