# -*- coding: utf-8 -*-
"""
'Mumblehard' is a malware for Linux/BSD operating systems.
The malware installs a backdoor providing the malicious actors with
full access to the infected system and allows for execution of
arbitrary code. The malware also includes a general-purpose proxy
module and a module for sending huge amounts of spam messages.

A detailed analysis of Mumblehard is available at:
<http://www.welivesecurity.com/wp-content/uploads/2015/04/mumblehard.pdf>

Technical indicators of compromise (IoCs) are available at:
<https://github.com/eset/malware-ioc/tree/master/mumblehard>

The malware installs a cronjob for connecting to a command-and-control
server every 15 minutes. Domain names and IP addresses used for
this purpose have been redirected to a so-called sinkhole logging
the requests.

Please find below a list of IP addresses hosted in your country that
tried to connect to a command-and-control server for Mumblehard.
This is a string indicator hosts on those IP addresses are infected
with the malware.

We would like to ask you to notify the owners of the affected hosts
and/or the responsible hosting providers of the infections.

Format:
ASN | IP | Country | Last seen (UTC) | ASN Desc

EX: [ 59939 | 185.43.220.195 | CZ | 2017-07-12 23:45:00 | WIBO-AS, NL]

"""
from intelmq.lib.bot import ParserBot
import dateutil.parser
import pytz


class BundMumblehardParserBot(ParserBot):

    parse = ParserBot.parse_csv
    recover_line = ParserBot.recover_line_csv

    def parse_line(self, line, report):
        event = self.new_event(report)
        event.add("source.asn", line[0])
        event.add("source.ip", line[1])
        event.add('source.geolocation.cc', line[2])
        event.add('time.source', pytz.utc.localize(dateutil.parser.parse(line[3])).isoformat())
        event.add('classification.type', 'malware')
        event.add('malware.name', 'Mumblehard')
        event.add('comment', "ASN Desc: " + line[4])
        yield event


BOT = BundMumblehardParserBot
