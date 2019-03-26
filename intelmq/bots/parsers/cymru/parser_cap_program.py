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
        event = self.new_event(report)

        event.add('source.ip', ip)
        if asn != '0':
            event.add('source.asn', asn)
        event.add('time.source', timestamp + ' GMT')
        event.add('source.as_name', asn_name)
        event.add('raw', self.recover_line(line))
        if report_type == 'beagle':  # TODO: verify
            # beagle|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[<GET REQUEST>] [srcport <PORT>]|ASNAME
            event.add('classification.type', 'malware')
            event.add('classification.identifier', 'beagle')
            event.add('malware.name', 'beagle')
            if len(comments):
                # TODO: what is the comment? One sample does not have a comment at all
                raise NotImplementedError("Can't properly parse report %r, not know how to parse comment."
                                          "" % report_type)
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
            event.add('classification.type', 'malware')
            event.add('classification.identifier', report_type)
            event.add('malware.name', report_type)
        elif report_type == 'bots':
            # bots|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[srcport <PORT>] [mwtype <TYPE>] [destaddr <IPADDR>] [comment]|ASNAME
            # TYPE can contain spaces -.-
            event.add('classification.type', 'infected system')
            comment_results = {}
            comment_key = None
            comment_value = []
            event_comment = []
            for part in comment_split + [None]:  # iterate once more at end
                if part in ['srcport', 'mwtype', 'destaddr', None]:
                    if comment_key and comment_value:
                        comment_results[comment_key] = ' '.join(comment_value)
                    comment_key = part
                    comment_value.clear()
                else:
                    if comment_key == 'destaddr' and len(comment_value) == 1:
                        # line 9 in test case ('Avalanche Botnet' comment)
                        event_comment.append(part)
                    else:
                        comment_value.append(part)
            for kind, value in comment_results.items():
                if kind == 'srcport':
                    event['extra.source_port'] = int(value)
                elif kind == 'mwtype':
                    event['classification.identifier'] = event['malware.name'] = value.lower()
                elif kind == 'destaddr':
                    event['destination.ip'] = value
                else:
                    raise ValueError('Unknown value in comment %r for report %r.' % (kind, report_type))
            if event_comment:
                event.add('event_description.text', ' '.join(event_comment))
        elif report_type == 'bruteforce':
            # bruteforce|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<PROTOCOL>|ASNAME
            event.add('classification.type', 'brute-force')
            event.add('classification.identifier', comments)
            event.add('protocol.application', comments)
        elif report_type == 'ddosreport':  # TODO: verify
            # ddosreport|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[<PROTOCOL> <PORT>] [category: <CATEGORY>]
            # [servpass: <PASSWORD>] [SSL] [url: <URL>]|ASNAME
            raise NotImplementedError('Report %r not implemented, format is unknown.' % report_type)
            event['classification.type'] = 'c&c'
            event['protocol.application'] = comment_split[0]
            event['source.port'] = comment_split[1]
            # TODO: category? password? ssl?
            event['source.url'] = comment_split[-1]
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
            event['source.url'] = comment_split[0]
            event.add('classification.type', 'malware')
            event.add('classification.identifier', 'malwareurl')
        elif report_type == 'openresolvers':
            # openresolvers|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS||ASNAME
            event['classification.type'] = 'vulnerable service'
            event['classification.identifier'] = 'dns-open-resolver'
            event['protocol.application'] = 'dns'
        elif report_type == 'phishing':
            # phishing|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<URL>|ASNAME
            event['classification.type'] = 'phishing'
            event['classification.identifier'] = 'phishing'
            event['source.url'] = comments
        elif report_type == 'proxy':
            # proxy|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<PROXY PORT>|ASNAME
            # Data in comment is not a port but e.g. HTTP CONNECT (8080)
            event['classification.type'] = 'proxy'
            event['classification.identifier'] = 'openproxy'
            event['extra.request'] = comments
        elif report_type == 'routers':  # TODO: verify
            # routers|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|[<DEVICE TYPE>]|ASNAME
            event['classification.type'] = 'compromised'
            if comments:
                event['classification.identifier'] = comments
        elif report_type == 'scanners':  # TODO: verify
            # scanners|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<PORTS>|ASNAME
            event['classification.type'] = 'scanner'
            event['classification.identifier'] = 'scanner'
            port = None
            try:
                port = int(comments)
            except ValueError:
                # TODO: How are ports splitted?
                raise NotImplementedError("Can't properly parse report %r, format for multiple ports is unknown."
                                          "" % report_type)
            else:
                event['source.port'] = port
        elif report_type == 'spam':
            # spam|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<SOURCE>|ASNAME
            event['classification.type'] = 'spam'
            event['classification.identifier'] = 'spam'
            if len(comments):
                # TODO: what is the comment? One sample does not have a comment at all
                raise NotImplementedError("Can't properly parse report %r, not know how to parse comment."
                                          "" % report_type)
        elif report_type == 'spreaders':  # TODO: verify
            # spreaders|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|<URL> [<MD5>]|ASNAME
            event.add('source.url', comment_split[0])
            if len(comment_split == 2):
                event.add('malware.hash.md5', comment_split[1])
            event.add('classification.type', 'malware')
            event.add('classification.identifier', 'spreader')
        elif report_type == 'stormworm':  # TODO: verify
            # stormworm|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|confidence:<NUMBER> [legacy|crypto] [srcport <SOURCE PORT>]|ASNAME
            if 'feed.accuracy' not in event:
                event['feed.accuracy'] = 100
            for i in range(len(comment_split)):
                if comment_split[i].startswith('confidence:'):
                    event['feed.accuracy'] *= int(comment_split[i].lstrip('confidence:')) / 5
                elif comment_split[i] in ['legacy', 'crypto']:
                    event['malware.version'] = comment_split[i]
                elif comment_split[i] == 'srcport':
                    event['extra.source_port'] = int(comment_split[i + 1])
                    break
        elif report_type == 'toxbot':  # TODO: verify
            # toxbot|192.0.2.1|ASN|YYYY-MM-DD HH:MM:SS|srcport <SOURCE PORT>|ASNAME
            event.add('classification.type', 'infected system')
            event.add('classification.identifier', report_type)
            event.add('malware.name', report_type)
            event['extra.source_port'] = int(comment_split[1])
        else:
            raise ValueError('Unknown report %r.', report_type)
        yield event


BOT = CymruCAPProgramParserBot
