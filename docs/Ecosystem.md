# IntelMQ Ecosystem

With the name "IntelMQ" one can mean the core library itself, or the bundle with IntelMQ Manager or even all related software.
This document provides an overview of the ecosystem and all related tools.

## IntelMQ Core

This is IntelMQ itself, as it is available at https://github.com/certtools/intelmq.

It includes all the bots, the harmonization, etc.

## IntelMQ Manager

The Manager is the most known software and can be seen as the face of IntelMQ.
This software provides a graphical user interface to the management tool `intelmqctl`.

https://github.com/certtools/intelmq-manager/

## EventDB

This is not a software itself but listed here because the term it is often mentioned.

The EventDB is a (usually PostgreSQL) database with data from intelmq.

For some related scripts see the [contrib/eventdb](../contrib/eventdb) directory and the [eventdb-stats](https://github.com/wagner-certat/eventdb-stats) repository for simple statistics generation.

## intelmq-webinput-csv

A web-based interface to inject CSV data into IntelMQ with on-line validation and live feedback.

http://github.com/certat/intelmq-webinput-csv/

## intelmq-mailgen

A solution to send grouped notifications to network owners using SMTP/OTRS.

https://github.com/Intevation/intelmq-mailgen

## IntelMQ Fody + Backend

Fody is an interface for intelmq-mailgen's contact database, it's OTRS and the EventDB.
The certbund-contact expert fetches the information from this contact database and provides scripts to import RIPE data into the contact database.

https://github.com/Intevation/intelmq-fody/
https://github.com/Intevation/intelmq-fody-backend/
https://github.com/Intevation/intelmq-certbund-contact/

## do-portal

A contact portal with organizational hierarchies, role functionality and network objects based on RIPE, allows self-administration by the contacts.
Can be queried from IntelMQ and integrates the stats-portal.

https://github.com/certat/do-portal/

## stats-portal

A Grafana-based statistics portal for the EventDB. Integrated in do-portal.

https://github.com/certtools/stats-portal/

## Malware Name Mapping

A mapping for malware names of different feeds with different namings to a common family name.

https://github.com/certtools/malware_name_mapping
