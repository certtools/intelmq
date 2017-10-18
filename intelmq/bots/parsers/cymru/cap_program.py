# -*- coding: utf-8 -*-
from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class CymruCAPProgramParserBot(ParserBot):

    def parse(self, report):
        lines = utils.base64_decode(report.get("raw")).splitlines()

        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                self.tempdata.append(line)
            else:
                yield line

    def parse_line(self, line, report):
        report, ip, asn, timestamp, comments, asn_name = line.split('|')
        comment = comments.split(' ')
        event = self.new_event(report)

        event.add('source.ip', ip)
        event.add('sorce.asn', asn)
        event.add('time.source', timestamp)
        event.add('source.as_name', asn_name)
        event.add('classification.type', 'blacklist')
        event.add('raw', self.recover_line(line))
        if report == 'beagle':  # TODO: verify
            # beagle|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[<GET REQUEST>] [srcport <PORT>]|ASNAME
            event.add('classification.type', 'malicious code')
            event.add('malware.name', 'beagle')
            event.add('destination.url', comment[0])
        elif report in ['blaster', 'dameware', 'dipnet', 'mydoom', 'nachi', 'phatbot',
                        'sinit', 'slammer']:
            # blaster|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS||ASNAME
            # dameware|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS||ASNAME
            # dipnet|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS||ASNAME
            # mydoom|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS||ASNAME
            # nachi|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS||ASNAME
            # phatbot|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS||ASNAME
            # sinit|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS||ASNAME
            # slammer|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS||ASNAME
            event.add('classification.type', 'malicious code')
            event.add('classification.identifier', report)
            event.add('malware.name', report)
        elif report == 'bots':
            # bots|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[srcport <PORT>] [mwtype <TYPE>] [destaddr <IPADDR>]|ASNAME
            event.add('classification.type', 'botnet drone')
            event['extra.source_port'] = comment[1]
            event['classification.identifier'] = event['malware.name'] = comment[3]
            event['destination.ip'] = comment[5]
        elif report == 'bruteforce':
            # bruteforce|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<PROTOCOL>|ASNAME
            event.add('classification.type', 'brute-force')
            event.add('classification.identifier', comments)
            event.add('protocol.application', comments)
        elif report == 'ddosreport':  # TODO: verify
            # ddosreport|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[<PROTOCOL> <PORT>] [category: <CATEGORY>] [servpass: <PASSWORD>] [SSL] [url: <URL>]|ASNAME
            event['classification.type'] = 'c&c'
            event['protocol.application'] = comment[0]
            event['source.port'] = comment[1]
            # TODO: category? password? ssl?
            event['source.url'] = comment[-1]
            raise NotImplementedError
        elif report == 'defacement':  # TODO: verify
            # defacement|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<URL> [<ZONE-H ID>]|ASNAME
            event['classification.type'] = 'compromised'
            event['classification.identifier'] = report
            event['source.url'] = comment[0]
            event['extra.zoneh.id'] = comment[1]
        elif report == 'fastflux':  # TODO: verify
            # fastflux|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[<DOMAIN>]|ASNAME
            event['classification.type'] = 'compromised'
            event['classification.identifier'] = report
            if comments:
                event['source.reverse_dns'] = comments
        elif report == 'malwareurl':  # TODO: verify
            # malwareurl|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<URL> <SCAN-ID>|ASNAME
            # TODO: classification
            event['source.url'] = comment[0]
            raise NotImplementedError
        elif report == 'openresolvers':
            # openresolvers|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS||ASNAME
            event['classification.type'] = 'vulnerable service'
            event['classification.identifier'] = 'dns-open-resolver'
            event['protocol.application'] = 'dns'
        elif report == 'phishing':  # TODO: verify
            # phishing|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<URL>|ASNAME
            event['classification.type'] = 'phishing'
            event['source.url'] = comments
        elif report == 'proxy':
            # proxy|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<PROXY PORT>|ASNAME
            event['classification.type'] = 'proxy'
            event['extra.request'] = comments
        elif report == 'routers':  # TODO: verify
            # routers|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[<DEVICE TYPE>]|ASNAME
            event['classification.type'] = 'compromised'
            if comments:
                event['classification.identifier'] = comments
        elif report == 'scanners':  # TODO: verify
            # scanners|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<PORTS>|ASNAME
            event['classification.type'] = 'scanner'
            # TODO: How are ports splitted?
            raise NotImplementedError
        elif report == 'spam':  # TODO: verify
            # spam|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<SOURCE>|ASNAME
            event['classification.type'] = 'spam'
            # TODO: what is the comment?
            raise NotImplementedError
        elif report == 'spreaders':  # TODO: verify
            # spreaders|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<URL> [<MD5>]|ASNAME
            # TODO: classification
            raise NotImplementedError
        elif report == 'stormworm':  # TODO: verify
            # stormworm|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|confidence:<NUMBER> [legacy|crypto] [srcport <SOURCE PORT>]|ASNAME
            if 'feed.accuracy' not in event:
                event['feed.accuracy'] = 100
            event['feed.accuracy'] *= int(comment[0].lstrip('confidence:'))/5
            raise NotImplementedError
        elif report == 'toxbot':  # TODO: verify
            # toxbot|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|srcport <SOURCE PORT>|ASNAME
            event.add('classification.type', 'botnet drone')
            event.add('classification.identifier', report)
            event.add('malware.name', report)
            event['extra.source_port'] = comment[1]
        else:
            raise ValueError('Unknown report %r', report)
        yield event


BOT = CymruCAPProgramParserBot
