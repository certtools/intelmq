IntelMQ - n6 Integration
========================

n6 is an Open Source Tool with very similar aims as IntelMQ, processing and distributing IoC data, developed by CERT.pl.
The covered use-cases differ and both tools have non-overlapping strengths.

Information about n6 can be found here:
- Website: https://n6.cert.pl/en/
- Development: https://github.com/CERT-Polska/n6/

.. figure:: https://n6.cert.pl/n6-schemat2.png
   :alt: n6 schema

Data format
-------------------------------

The internal data representation differs for the systems, so any data exchanged between the systems needs to be converted.
As n6 can save multiple IP addresses per event, which IntelMQ is unable to do, one n6 event results in one or more IntelMQ events.
Thus and because of some other reasons, the conversion is *not* bidirectional.

Data exchange interface
-------------------------------

n6 offers a STOMP interface via the RabbitMQ broker, which can be used for both sending and receiving data.
IntelMQ has both a STOMP collector bot as well as a STOMP output bot.

- :ref:`IntelMQ's Stomp collector bot <stomp collector bot>`
- :ref:`IntelMQ's n6 parser bot <n6 parser bot>`
- :ref:`IntelMQ's Stomp output bot <stomp output bot>`

Data conversion
-------------------------------

IntelMQ can parse n6 data using the n6 parser and n6 can parse IntelMQ data using the Intelmq2n6 parser.

- :ref:`IntelMQ's n6 parser bot <n6 parser bot>`

Webinput CSV
-------------------------------

The IntelMQ Webinput CSV software can also be used together with n6.
The documentation can be found in the software's repository:
https://github.com/certat/intelmq-webinput-csv/blob/master/docs/webinput-n6.md
