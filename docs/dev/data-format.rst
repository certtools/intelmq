..
   SPDX-FileCopyrightText: 2015 Aaron Kaplan <aaron@lo-res.org>
   SPDX-License-Identifier: AGPL-3.0-or-later

##################
Data Format
##################

.. contents::

Overview
========

In IntelMQ version 3.x+ the internal data format name changed from DHO ( IntelMQ Data Harmonization ) to IDF ( IntelMQ Data Format ).
The python module `intelmq.lib.harmonization` and the configuration file `harmonization.conf` keep the name `harmonization` for now. DHO and IDF have the same meaning.

All messages (reports and events) are Python/JSON dictionaries. The key names and according types are defined by the IntelMQ Data Format.

The purpose of this document is to list and clearly define known **fields** in Abusehelper as well as IntelMQ or similar systems.
A field is a ```key=value``` pair. For a clear and unique definition of a field, we must define the **key** (field-name) as well as the possible **values**.
A field belongs to an **event**. An event is basically a structured log record in the form ```key=value, key=value, key=value, …```.
In the :ref:`List of known fields <data format field list>`, each field is grouped by a **section**. We describe these sections briefly below.
Every event **MUST** contain a timestamp field.

An `IOC <https://en.wikipedia.org/wiki/Indicator_of_compromise>`_ (Indicator of compromise) is a single observation like a log line.

Rules for keys
==============

The keys can be grouped together in sub-fields, e.g. `source.ip` or `source.geolocation.latitude`.

Only the lower-case alphabet, numbers and the underscore are allowed. Further, the field name must not begin with a number.
Thus, keys must match ``^[a-z_][a-z_0-9]+(\.[a-z_0-9]+)*$``.
These rules also apply for the otherwise unregulated ``extra.`` namespace.


Sections
========

As stated above, every field is organized under some section. The following is a description of the sections and what they imply.

Feed
----

Fields listed under this grouping list details about the source feed where information came from.

Time
----

The time section lists all fields related to time information.
This document requires that all the timestamps MUST be normalized to UTC. If the source reports only a date, do not attempt to invent timestamps.

Source Identity
---------------

This section lists all fields related to identification of the source. The source is the identity the IoC is about, as opposed to the destination identity, which is another identity.

For examples see the table below.

The abuse type of an event defines the way these events needs to be interpreted. For example, for a botnet drone they refer to the compromised machine, whereas for a command and control server they refer the server itself.

Source Geolocation Identity
^^^^^^^^^^^^^^^^^^^^^^^^^^^

We recognize that ip geolocation is not an exact science and analysis of the abuse data has shown that different sources attribution sources have different opinions of the geolocation of an ip. This is why we recommend to enrich the data with as many sources as you have available and make the decision which value to use for the cc IOC based on those answers.

Source Local Identity
^^^^^^^^^^^^^^^^^^^^^

Some sources report an internal (NATed) IP address.

Destination Identity
--------------------

The abuse type of an event defines the way these IOCs needs to be interpreted. For a botnet drone they refer to the compromised machine, whereas for a command and control server they refer the server itself.

Destination Geolocation Identity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We recognize that ip geolocation is not an exact science and analysis of the abuse data has shown that different sources attribution sources have different opinions of the geolocation of an ip. This is why we recommend to enrich the data with as many sources as you have available and make the decision which value to use for the cc IOC based on those answers.

Destination Local Identity
^^^^^^^^^^^^^^^^^^^^^^^^^^

Some sources report an internal (NATed) IP address.

Extra values
------------
Data which does not fit in the format can be saved in the 'extra' namespace. All keys must begin with `extra.`, there are no other rules on key names and values. The values can be get/set like all other fields.

.. _data format field list:

Fields List and data types
==========================

A list of allowed fields and data types can be found in :doc:`format-fields`.

.. _data format classification:

Classification
==============

IntelMQ classifies events using three labels: taxonomy, type and identifier. This tuple of three values can be used for deduplication of events and describes what happened.

The taxonomy can be automatically added by the taxonomy expert bot based on the given type. The following classification scheme follows the `Reference Security Incident Taxonomy (RSIT) <https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/>`_:


===============================  ========================================= =============================================
      Taxonomy                   Type                                        Description
===============================  ========================================= =============================================
   abusive-content               harmful-speech                              Discreditation or discrimination of somebody, e.g. cyber stalking, racism or threats against one or more individuals.
   abusive content               spam                                        Or 'Unsolicited Bulk Email', this means that the recipient has not granted verifiable permission for the message to be sent and that the message is sent as part of a larger collection of messages, all having a functionally comparable content.
   abusive-content               violence                                    Child pornography, glorification of violence, etc.
   availability                  ddos                                        Distributed Denial of Service attack, e.g. SYN-Flood or UDP-based reflection/amplification attacks.
   availability                  dos                                         Denial of Service attack, e.g. sending specially crafted requests to a web application which causes the application to crash or slow down.
   availability                  misconfiguration                            Software misconfiguration resulting in service availability issues, e.g. DNS server with outdated DNSSEC Root Zone KSK.
   availability                  outage                                      Outage caused e.g. by air condition failure or natural disaster.
   availability                  sabotage                                    Physical sabotage, e.g cutting wires or malicious arson.
   fraud                         copyright                                   Offering or Installing copies of unlicensed commercial software or other copyright protected materials (Warez).
   fraud                         masquerade                                  Type of attack in which one entity illegitimately impersonates the identity of another in order to benefit from it.
   fraud                         phishing                                    Masquerading as another entity in order to persuade the user to reveal private credentials.
   fraud                         unauthorized-use-of-resources               Using resources for unauthorized purposes including profit-making ventures, e.g. the use of e-mail to participate in illegal profit chain letters or pyramid schemes.
   information-content-security  data-leak                                   Leaked confidential information like credentials or personal data.
   information-content-security  data-loss                                   Loss of data, e.g. caused by harddisk failure or physical theft.
   information-content-security  unauthorised-information-access             Unauthorized access to information, e.g. by abusing stolen login credentials for a system or application, intercepting traffic or gaining access to physical documents.
   information-content-security  unauthorised-information-modification       Unauthorised modification of information, e.g. by an attacker abusing stolen login credentials for a system or application or a ransomware encrypting data.
   information-gathering         scanner                                     Attacks that send requests to a system to discover weaknesses. This also includes testing processes to gather information on hosts, services and accounts. Examples: fingerd, DNS querying, ICMP, SMTP (EXPN, RCPT, ...), port scanning.
   information-gathering         sniffing                                    Observing and recording of network traffic (wiretapping).
   information-gathering         social-engineering                          Gathering information from a human being in a non-technical way (e.g. lies, tricks, bribes, or threats). This IOC refers to a resource, which has been observed to perform brute-force attacks over a given application protocol.
   intrusion-attempts            brute-force                                 Multiple login attempts (Guessing / cracking of passwords, brute force).
   intrusion-attempts            exploit                                     An attack using an unknown exploit.
   intrusion-attempts            ids-alert                                   IOCs based on a sensor network. This is a generic IOC denomination, should it be difficult to reliably denote the exact type of activity involved for example due to an anecdotal nature of the rule that triggered the alert.
   intrusions                    application-compromise                      Compromise of an application by exploiting (un)known software vulnerabilities, e.g. SQL injection.
   intrusions                    burglary                                    Physical intrusion, e.g. into corporate building or data center.
   intrusions                    privileged-account-compromise               Compromise of a system where the attacker gained administrative privileges.
   intrusions                    system-compromise                           Compromise of a system, e.g. unauthorised logins or commands. This includes compromising attempts on honeypot systems.
   intrusions                    unprivileged-account-compromise             Compromise of a system using an unprivileged (user/service) account.
   malicious-code                c2-server                                   This is a command and control server in charge of a given number of botnet drones.
   malicious-code                infected-system                             This is a compromised machine, which has been observed to make a connection to a command and control server.
   malicious-code                malware-configuration                       This is a resource which updates botnet drones with a new configuration.
   malicious-code                malware-distribution                        URI used for malware distribution, e.g. a download URL included in fake invoice malware spam.
   other                         blacklist                                   Some sources provide blacklists, which clearly refer to abusive behavior, such as spamming, but fail to denote the exact reason why a given identity has been blacklisted. The reason may be that the justification is anecdotal or missing entirely. This type should only be used if the typing fits the definition of a blacklist, but an event specific denomination is not possible for one reason or another. Not in RSIT.
   other                         dga-domain                                  DGA Domains are seen various families of malware that are used to periodically generate a large number of domain names that can be used as rendezvous points with their command and control servers. Not in RSIT.
   other                         other                                       All incidents which don't fit in one of the given categories should be put into this class.
   other                         malware                                     An IoC referring to a malware (sample) itself. Not in RSIT.
   other                         proxy                                       This refers to the use of proxies from inside your network. Not in RSIT.
   test                          test                                        Meant for testing. Not in RSIT.
   other                         tor                                         This IOC refers to incidents related to TOR network infrastructure. Not in RSIT.
   other                         undetermined                                The categorisation of the incident is unknown/undetermined.
   vulnerable                    ddos-amplifier                              Publicly accessible services that can be abused for conducting DDoS reflection/amplification attacks, e.g. DNS open-resolvers or NTP servers with monlist enabled.
   vulnerable                    information-disclosure                      Publicly accessible services potentially disclosing sensitive information, e.g. SNMP or Redis.
   vulnerable                    potentially-unwanted-accessible             Potentially unwanted publicly accessible services, e.g. Telnet, RDP or VNC.
   vulnerable                    vulnerable-system                           A system which is vulnerable to certain attacks. Example: misconfigured client proxy settings (example: WPAD), outdated operating system version, etc.
   vulnerable                    weak-crypto                                 Publicly accessible services offering weak crypto, e.g. web servers susceptible to POODLE/FREAK attacks.
===============================  ========================================= =============================================

In the "other" taxonomy, several types are not in the RSIT, but this taxonomy is intentionally extensible.

Meaning of source and destination identities
--------------------------------------------

Meaning of source and destination identities for each classification type and possible ``classification.identifier`` meanings and usages. The identifier is often a normalized malware name, grouping many variants or the affected network protocol.
Examples of the meaning of the *source* and *destination* fields for each classification type and possible identifiers are shown here. Usually the main information is in the *source* fields. The identifier is often a normalized malware name, grouping many variants.

=======================  ================================================  ==========================  ===========================
 Type                     Source                                            Destination                 Possible identifiers
=======================  ================================================  ==========================  ===========================
 blacklist                *blacklisted device*
 brute-force              *attacker*                                        target
 c2-server                *(sinkholed) c&c server*                                                      zeus, palevo, feodo
 ddos                     *attacker*                                        target
 dga-domain               *infected device*
 dropzone                 *server hosting stolen data*
 exploit                  *hosting server*
 ids-alert                *triggering device*
 infected-system          *infected device*                                 *contacted c2c server*
 malware                  *infected device*                                                             zeus, palevo, feodo
 malware configuration    *infected device*
 malware-distribution     *server hosting malware*
 phishing                 *phishing website*
 proxy                    *server allowing policy and security bypass*
 scanner                  *scanning device*                                 scanned device              http,modbus,wordpress
 spam                     *infected device*                                 targeted server
 system-compromise        *server*
 vulnerable-system        *vulnerable device*                                                           heartbleed, openresolver, snmp, wpad
=======================  ================================================  ==========================  ===========================

Field in italics is the interesting one for CERTs.

Example:

If you know of an IP address that connects to a zeus c&c server, it's about the infected device, thus `classification.taxonomy` is *malicious-code*, `classification.type` is *infected-system* and the `classification.identifier` is zeus. If you want to complain about the c&c server, the event's `classification.type` is *c2server*. The `malware.name` can have the full name, eg. `zeus_p2p`.

Minimum recommended requirements for events
===========================================

Below, we have enumerated the minimum recommended requirements for an actionable abuse event. These keys should to be present for the abuse report to make sense for the end recipient. Please note that if you choose to anonymize your sources, you can substitute **feed** with **feed.code** and that only one of the identity keys **ip**, **domain name**, **url**, **email address** must be present. All the rest of the keys are **optional**.

=================  ========================  =================
 Category           Key                        Terminology
=================  ========================  =================
 Feed               feed.name                  Should
 Classification     classification.type        Should
 Classification     classification.taxonomy    Should
 Time               time.source                Should
 Time               time.observation           Should
 Identity           source.ip                  Should*
 Identity           source.fqdn                Should*
 Identity           source.url                 Should*
 Identity           source.account             Should*
=================  ========================  =================

* only one of them

This list of required fields is *not* enforced by IntelMQ.

**NOTE:** This document was copied from `AbuseHelper repository <https://github.com/abusesa/abusehelper/blob/master/docs/Harmonization.md>`_ (now `Arctic Security Public documents <https://github.com/arcticsecurity/public/blob/master/docs/Harmonization.md>`_ and improved.
