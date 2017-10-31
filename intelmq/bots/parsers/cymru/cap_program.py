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
        report_type, ip, asn, timestamp, comments, asn_name = line.split('|')
        comment_split = comments.split(' ')
        comment_zip = zip(comment_split[::2], comment_split[1::2])
        event = self.new_event(report)

        event.add('source.ip', ip)
        event.add('source.asn', asn)
        event.add('time.source', timestamp + ' GMT')
        event.add('source.as_name', asn_name)
        event.add('raw', self.recover_line(line))
        if report_type == 'beagle':  # TODO: verify
            # beagle|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[<GET REQUEST>] [srcport <PORT>]|ASNAME
            event.add('classification.type', 'malicious code')
            event.add('malware.name', 'beagle')
            event.add('destination.url', comment_split[0])
        elif report_type in ['blaster', 'dameware', 'dipnet', 'mydoom', 'nachi', 'phatbot',
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
            event.add('classification.identifier', report_type)
            event.add('malware.name', report_type)
        elif report_type == 'bots':
            # bots|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[srcport <PORT>] [mwtype <TYPE>] [destaddr <IPADDR>]|ASNAME
            event.add('classification.type', 'botnet drone')
            for kind, value in comment_zip:
                if kind == 'srcport':
                    event['extra.source_port'] = value
                elif kind == 'mwtype':
                    event['classification.identifier'] = event['malware.name'] = value.lower()
                elif kind == 'destaddr':
                    event['destination.ip'] = value
                else:
                    raise ValueError('Unknown value in comment %r.' % kind)
        elif report_type == 'bruteforce':
            # bruteforce|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<PROTOCOL>|ASNAME
            event.add('classification.type', 'brute-force')
            event.add('classification.identifier', comments)
            event.add('protocol.application', comments)
        elif report_type == 'ddosreport':  # TODO: verify
            # ddosreport|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[<PROTOCOL> <PORT>] [category: <CATEGORY>] [servpass: <PASSWORD>] [SSL] [url: <URL>]|ASNAME
            event['classification.type'] = 'c&c'
            event['protocol.application'] = comment_split[0]
            event['source.port'] = comment_split[1]
            # TODO: category? password? ssl?
            event['source.url'] = comment_split[-1]
            raise NotImplementedError('Report %r not implemented.' % report_type)
        elif report_type == 'defacement':  # TODO: verify
            # defacement|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<URL> [<ZONE-H ID>]|ASNAME
            event['classification.type'] = 'compromised'
            event['classification.identifier'] = report_type
            event['source.url'] = comment_split[0]
            event['extra.zoneh.id'] = comment_split[1]
        elif report_type == 'fastflux':  # TODO: verify
            # fastflux|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[<DOMAIN>]|ASNAME
            event['classification.type'] = 'compromised'
            event['classification.identifier'] = report_type
            if comments:
                event['source.reverse_dns'] = comments
        elif report_type == 'malwareurl':  # TODO: verify
            # malwareurl|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<URL> <SCAN-ID>|ASNAME
            # TODO: classification
            event['source.url'] = comment_split[0]
            raise NotImplementedError('Report %r not implemented.' % report_type)
        elif report_type == 'openresolvers':
            # openresolvers|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS||ASNAME
            event['classification.type'] = 'vulnerable service'
            event['classification.identifier'] = 'dns-open-resolver'
            event['protocol.application'] = 'dns'
        elif report_type == 'phishing':
            # phishing|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<URL>|ASNAME
            event['classification.type'] = 'phishing'
            event['source.url'] = comments
        elif report_type == 'proxy':
            # proxy|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<PROXY PORT>|ASNAME
            event['classification.type'] = 'proxy'
            event['extra.request'] = comments
        elif report_type == 'routers':  # TODO: verify
            # routers|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[<DEVICE TYPE>]|ASNAME
            event['classification.type'] = 'compromised'
            if comments:
                event['classification.identifier'] = comments
        elif report_type == 'scanners':  # TODO: verify
            # scanners|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<PORTS>|ASNAME
            event['classification.type'] = 'scanner'
            # TODO: How are ports splitted?
            raise NotImplementedError('Report %r not implemented.' % report_type)
        elif report_type == 'spam':
            # spam|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<SOURCE>|ASNAME
            event['classification.type'] = 'spam'
            # TODO: what is the comment? One sample does not have a comment at all
        elif report_type == 'spreaders':  # TODO: verify
            # spreaders|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<URL> [<MD5>]|ASNAME
            # TODO: classification
            raise NotImplementedError('Report %r not implemented.' % report_type)
        elif report_type == 'stormworm':  # TODO: verify
            # stormworm|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|confidence:<NUMBER> [legacy|crypto] [srcport <SOURCE PORT>]|ASNAME
            if 'feed.accuracy' not in event:
                event['feed.accuracy'] = 100
            event['feed.accuracy'] *= int(comment_split[0].lstrip('confidence:'))/5
            raise NotImplementedError('Report %r not implemented.' % report_type)
        elif report_type == 'toxbot':  # TODO: verify
            # toxbot|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|srcport <SOURCE PORT>|ASNAME
            event.add('classification.type', 'botnet drone')
            event.add('classification.identifier', report_type)
            event.add('malware.name', report_type)
            event['extra.source_port'] = comment_split[1]
        else:
            raise ValueError('Unknown report %r', report_type)
        yield event


BOT = CymruCAPProgramParserBot
