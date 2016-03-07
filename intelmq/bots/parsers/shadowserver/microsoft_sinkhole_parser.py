# -*- coding: utf-8 -*-
"""
https://www.shadowserver.org/wiki/pmwiki.php/Services/Microsoft-Sinkhole

timestamp 	Timestamp in UTC+0 the IP accessed the sinkhole system
ip 	IP that accessed the sinkhole
asn 	ASN of the IP
geo 	Country location of the IP
url 	HTTP request   # without hostname
type 	Drone type (if known)
http_agent 	HTTP agent
tor 	If client is a TOR exit node
src_port 	TCP source port
p0f_genre 	First level TCP test of the Operating System
p0f_detail 	Detailed results of the OS test
hostname 	Reverse DNS of the IP
dst_port 	TCP destination port
http_host 	Domain accessed by the IP
http_referer 	HTTP Referer
http_referer_ip [UNDOCUMENTED]
http_referer_asn 	HTTP Referer ASN
http_referer_geo 	HTTP Referer country code
dst_ip 	Sinkhole IP the target accessed (if available)
dst_asn 	Sinkhole ASN the target accessed (if available)
dst_geo 	Sinkhole GEO the target accessed (if available)
naics   [UNDOCUMENTED]
sic [UNDOCUMENTED]
"""
from __future__ import unicode_literals

import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class ShadowServerMicrosoftSinkholeParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report["raw"])
        for row in utils.csv_reader(raw_report, dictreader=True):
            event = Event(report)
            extra = {}
            self.logger.debug(repr(row))

            event.add('time.source', row['timestamp']+' UTC')
            event.add('source.ip', row['ip'])
            event.add('source.asn', row['asn'])
            event.add('source.geolocation.cc', row['geo'])
            if row['http_host'] and row['url']:
                event.add('destination.url', row['http_host']+row['url'])
            elif row['url']:
                extra['url'] = row['url']  # incomplete URL
            event.add('malware.name', row['type'])
            if row['http_agent']:
                extra['http_agent'] = row['http_agent']
            if row['tor']:
                event.add('source.tor_node', row['tor'])
            event.add('source.port', row['src_port'])
            if row['p0f_genre']:
                extra['os.name'] = row['p0f_genre']
            if row['p0f_detail']:
                extra['os.version'] = row['p0f_detail']
            if row['hostname']:
                event.add('source.reverse_dns', row['hostname'])
            event.add('destination.port', row['dst_port'])
            if row['http_host']:
                extra['http_host'] = row['http_host']
            if row['http_referer'] not in ['', 'null']:
                extra['http_referer'] = row['http_referer']
            if row['http_referer_asn']:
                extra['http_referer_asn'] = row['http_referer_asn']
            if row['http_referer_geo']:
                extra['http_referer_geo'] = row['http_referer_geo']
            if row['dst_ip']:
                event.add('destination.ip', row['dst_ip'])
            if row['dst_asn']:
                event.add('destination.asn', row['dst_asn'])
            if row['dst_geo']:
                event.add('destination.geolocation.cc', row['dst_geo'])
            if int(row['naics']):
                extra['naics'] = int(row['naics'])
            if int(row['sic']):
                extra['sic'] = int(row['sic'])

            event.add('raw', '"'+','.join(map(str, row.items()))+'"')
            if extra:
                event.add('extra', extra)
            event.add('classification.type', 'botnet drone')
            event.add('protocol.application', 'http')

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ShadowServerMicrosoftSinkholeParserBot(sys.argv[1])
    bot.start()
