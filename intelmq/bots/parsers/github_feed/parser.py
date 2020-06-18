"""
Github IOC feeds' parser
"""
import ipaddress
import json

try:
    import validators
    from validators.hashes import md5 as valid_md5, sha1 as valid_sha1, sha256 as valid_sha256
    from validators.domain import domain as valid_domain
    from validators.url import url as valid_url
except ImportError:
    validators = None

from intelmq.lib.bot import Bot
from intelmq.lib.utils import base64_decode
from intelmq.lib.exceptions import MissingDependencyError

HASH_VALIDATORS = {
    'sha1': lambda x: valid_sha1(x),
    'sha256': lambda x: valid_sha256(x),
    'md5': lambda x: valid_md5(x)
}


class GithubFeedParserBot(Bot):

    def init(self):
        if validators is None:
            raise MissingDependencyError('validators')
        self.__supported_feeds = {
            'StrangerealIntel/DailyIOC': lambda logger: self.StrangerealIntelDailyIOC(logger)
        }

    def process(self):
        report = self.receive_message()
        try:
            decoded_content = json.loads(base64_decode(report['raw']).replace("'", '"'))
        except json.JSONDecodeError as e:
            self.logger.error("Invalid report['raw']: {}".format(e))
            self.acknowledge_message()
            return

        for event in self.parse(report, decoded_content):
            self.send_message(event)
        self.acknowledge_message()

    def parse(self, report, json_content: dict):
        event = self.new_event(report)

        # add extra metadata from report (when coming from Github API collector)
        if 'extra.file_metadata' in report.keys():
            for k, v in report.get('extra.file_metadata').items():
                event.add('extra.file_metadata.' + k, v)

        for knonw_feed, feed_parser in self.__supported_feeds.items():
            if knonw_feed in report.get('feed.url'):
                return feed_parser(self.logger).parse(event, json_content)
        raise ValueError("Unknown feed '{}'.".format(report.get('feed.url')))

    class StrangerealIntelDailyIOC:
        def __init__(self, logger):
            self.logger = logger

        def parse(self, event, json_content: dict):
            """
            Parse the specific feed to sufficient fields

            :param event: output event object
            :param json_content: IOC(s) in JSON format
            """

            class Next(Exception):
                pass

            clean_event = event

            for ioc in json_content:
                event = clean_event.copy()
                event.add('raw', str(ioc))
                event.add('classification.type', 'unknown')
                event.add('classification.taxonomy', 'other')
                event.add('event_description.text', ioc['Description'])

                ioc_indicator = ioc['Indicator']

                try:
                    for hash_type, validate_hash_func in HASH_VALIDATORS.items():
                        if validate_hash_func(ioc_indicator):
                            yield parse_hash_indicator(event, ioc_indicator, hash_type)
                            raise Next
                except Next:
                    continue

                if valid_domain(ioc_indicator):
                    yield parse_domain_indicator(event, ioc_indicator)
                    continue

                try:
                    ipaddress.ip_address(ioc_indicator)
                    yield parse_ip_indicator(event, ioc_indicator)
                    continue
                except ValueError:
                    pass

                if valid_url(ioc_indicator):
                    yield parse_url_indicator(event, ioc_indicator)
                    continue

                # on default drop the event
                self.logger.warning("IOC '{}' not in expected format.".format(ioc_indicator.replace('.', '[.]')))


def parse_url_indicator(event, ioc_indicator: str):
    event.add('source.url', ioc_indicator)
    return event


def parse_ip_indicator(event, ioc_indicator: str):
    event.add('source.ip', ioc_indicator)
    return event


def parse_domain_indicator(event, ioc_indicator: str):
    event.add('source.fqdn', ioc_indicator)
    return event


def parse_hash_indicator(event, ioc_indicator: str, hash_type: str):
    event.add('malware.hash.{}'.format(hash_type), ioc_indicator)
    event.change('classification.taxonomy', 'malicious code')
    event.change('classification.type', 'malware')
    return event


BOT = GithubFeedParserBot
