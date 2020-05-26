# -*- coding: utf-8 -*-
""" IntelMQ parser for Bambenek DGA, Domain, and IP feeds """

from intelmq.lib.bot import ParserBot


class BambenekParserBot(ParserBot):
    """ Single parser for Bambenek feeds """

    IPMASTERLIST = {
        'http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt',
        'https://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt',
        'https://faf.bambenekconsulting.com/feeds/dga/c2-ipmasterlist.txt',
    }
    DOMMASTERLIST = {
        'http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt',
        'https://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt',
        'https://faf.bambenekconsulting.com/feeds/dga/c2-dommasterlist.txt',
    }
    DGA_FEED = {
        'http://osint.bambenekconsulting.com/feeds/dga-feed.txt',
        'https://osint.bambenekconsulting.com/feeds/dga-feed.txt',
        'https://faf.bambenekconsulting.com/feeds/dga-feed.txt',
    }

    MALWARE_NAME_MAP = {
        "cl": "cryptolocker",
        "p2pgoz": "p2p goz",
        "ptgoz": "pt goz",
        "volatile": "volatile cedar",
    }

    def parse_line(self, line, report):
        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)

        else:
            value = line.split(',')
            event = self.new_event(report)

            event.add('event_description.text', value[1])
            event.add('event_description.url', value[3])
            event.add('raw', line)

            # last column is a url with malware named txt file link
            malware_name = value[-1].split('/')[-1].split('.')[0]
            event.add('malware.name', self.MALWARE_NAME_MAP.get(malware_name, malware_name))

            if report['feed.url'] in BambenekParserBot.IPMASTERLIST:
                event.add('source.ip', value[0])
                event.add('time.source', value[2] + ' UTC')
                event.add('classification.type', 'c2server')
                event.add('status', 'online')

            elif report['feed.url'] in BambenekParserBot.DOMMASTERLIST:
                event.add('source.fqdn', value[0])
                event.add('time.source', value[2] + ' UTC')
                event.add('classification.type', 'c2server')
                event.add('status', 'online')

            elif report['feed.url'] in BambenekParserBot.DGA_FEED:
                event.add('source.fqdn', value[0])
                event.add('time.source', value[2] + ' 00:00 UTC')
                event.add('classification.type', 'dga domain')

            else:
                raise ValueError('Unknown data feed %s.' % report['feed.url'])

            yield event


BOT = BambenekParserBot
