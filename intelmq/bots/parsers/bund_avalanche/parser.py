# -*- coding: utf-8 -*-
"""
With an internationally coordinated operation, law enforcement
agencies took down the 'Avalanche' server infrastructure used
for hosting various botnets.
Additional information is available at:
<https://www.bsi-fuer-buerger.de/EN/avalanche>
<http://www.eurojust.europa.eu/press/PressReleases/Pages/2016/
2016-12-01.aspx>

In the course of this operation, domain names used by malware
related to those botnets for contacting command-and-control
servers have been redirected to sinkholes. CERT-Bund is provided
with log data from the sinkholes for notification of responsible
network operators in Germany and national CERTs worldwide.

Please find below a list of affected hosts in your country.
Each record includes the IP address, a timestamp (UTC) and the
name of the corresponding malware family. If available, the records
also include the source port, target IP, target port and target
hostname for the connection.

A value of 'generic' for the malware family means:
a) The affected system connected to a domain name related to the
   Avalanche botnet infrastructure which could not be mapped to
   a particular malware family yet.
or
b) The HTTP request sent by the affected system did not include
   a domain name. Thus, on the sinkhole it could not be decided
   which domain name the affected system resolved to connect to
   the respective IP address.

Most of the malware families reported here include functions for
identity theft (harvesting of usernames and passwords) and/or
online-banking fraud. Further information on the different malware
families as well as additional help for victims is available at:
<https://www.bsi-fuer-buerger.de/EN/avalanche>

Format:
"asn","ip","timestamp","malware","src_port","dst_ip","dst_port","dst_host"

EX: ["6830","88.146.158.126","2017-12-02 23:59:40","tinba","4379","216.218.185.162","80","picapicachu.com"]

"""
from intelmq.lib.bot import ParserBot
import dateutil.parser
import pytz


class BundAvalancheParserBot(ParserBot):

    parse = ParserBot.parse_csv
    recover_line = ParserBot.recover_line_csv

    def parse_line(self, line, report):
        event = self.new_event(report)
        event.add("source.asn", line[0])
        event.add("source.ip", line[1])
        event.add('time.source', pytz.utc.localize(dateutil.parser.parse(line[2])).isoformat())
        event.add('classification.type', 'malware')
        event.add('malware.name', line[3])
        event.add('source.port', line[4])
        event.add('comment', "Destination.ip: " + line[5] + ", Destination.port: " + line[6] + ", Destination.host: " + line[7])
        yield event


BOT = BundAvalancheParserBot
