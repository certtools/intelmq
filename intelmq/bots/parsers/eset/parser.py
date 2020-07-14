import json

from intelmq.lib.bot import ParserBot

message_taxonomy_map = {
    'Host actively distributes high-severity threat in the form of executable code.': 'malware-distribution',
    'Host is known to be distributing low-risk and potentially unwanted content.': 'malware-distribution',
    'Host is known source of phishing or other fraudulent content.': 'phishing',
    'Host is known to be actively distributing adware or other medium-risk software.': 'other',
    'Host is known source of active fraudulent content.': 'other'
}


class ESETParserBot(ParserBot):
    def init(self):
        self.f_map = {
            'ei.urls (json)': self.urls_parse,
            'ei.domains v2 (json)': self.domains_parse
        }

    parse = ParserBot.parse_json

    def parse_line(self, line, report):  # parse a section of the received report
        event = self.new_event(report)

        self.common_parse(event, line)
        event['extra.eset_feed'] = report['extra.eset_feed']
        f = self.f_map.get(report['extra.eset_feed'], None)
        if not f:
            raise ValueError('Unsupported feed %r' % report['extra.eset_feed'])

        f(event, line)

        yield event

    @staticmethod
    def _get_taxonomy(reason):
        tax = message_taxonomy_map.get(reason, None)
        if tax:  # was found in dictionary
            return tax
        elif reason.startswith('Host is used as command and control server'):  # dynamic section after that
            return 'c2server'
        else:
            return 'other'

    @staticmethod
    def domains_parse(event, line):
        event.add('time.source', line['last_seen'])

    @staticmethod
    def urls_parse(event, line):
        event.add('time.source', line['domain_last_seen'])
        event.add('source.url', line['url'])

    def common_parse(self, event, line):
        type = self._get_taxonomy(line['reason'])

        event.add('raw', json.dumps(line, sort_keys=True))
        event.add('event_description.text', line['reason'])
        event.add('classification.type', type)
        event.add('source.fqdn', line['domain'], raise_failure=False)  # IP addresses may be passed in line['domain']

        ip = line['ip']
        if ip and not ip.endswith('_NXDOMAIN'):
            event.add('source.ip', ip)

    recover_line = ParserBot.recover_line_json


BOT = ESETParserBot
