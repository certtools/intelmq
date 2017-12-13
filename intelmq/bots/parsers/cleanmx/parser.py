from xml.etree import ElementTree

from collections import OrderedDict

from intelmq.lib import utils
from intelmq.lib.bot import Bot

PHISHING = OrderedDict([
    ("line", "__IGNORE__"),
    ("id", "extra"),
    ("first", "__IGNORE__"),
    ("firsttime", "time.source"),
    ("last", "__IGNORE__"),
    ("lasttime", "__IGNORE__"),
    ("phishtank", "extra"),
    ("target", "event_description.target"),
    ("url", "source.url"),
    ("recent", "status"),  # can be 'down', 'toggle' or 'up'
    ("response", "extra"),
    ("ip", "source.ip"),
    ("review", "extra"),
    ("domain", "source.fqdn"),
    ("country", "source.geolocation.cc"),
    ("source", "source.registry"),
    ("email", "source.abuse_contact"),
    ("inetnum", "extra"),  # network range, probably source.network
    ("netname", "extra"),
    ("descr", "extra"),
    ("ns1", "extra"),
    ("ns2", "extra"),
    ("ns3", "extra"),
    ("ns4", "extra"),
    ("ns5", "extra"),
])
VIRUS = OrderedDict([
    ("line", "__IGNORE__"),
    ("id", "extra"),
    ("sub", "extra"),
    ("first", "__IGNORE__"),
    ("firsttime", "time.source"),
    ("last", "__IGNORE__"),
    ("lasttime", "__IGNORE__"),
    ("scanner", "extra"),
    ("virusname", "malware.name"),
    ("url", "source.url"),
    ("recent", "status"),
    ("response", "extra"),
    ("ip", "source.ip"),
    ("as", "source.asn"),
    ("review", "extra"),
    ("domain", "source.fqdn"),
    ("country", "source.geolocation.cc"),
    ("source", "extra"),
    ("email", "source.abuse_contact"),
    ("inetnum", "extra"),
    ("netname", "extra"),
    ("descr", "extra"),
    ("ns1", "extra"),
    ("ns2", "extra"),
    ("ns3", "extra"),
    ("ns4", "extra"),
    ("ns5", "extra"),
    ("md5", "malware.hash.md5"),
    ("virustotal", "extra"),
    ("vt_score", "extra"),
    ("vt_info", "extra"),
])


class CleanMXParserBot(Bot):

    def get_mapping_and_type(self, url):
        if 'xmlphishing' in url:
            return PHISHING, 'phishing'
        elif 'xmlviruses' in url:
            return VIRUS, 'malware'
        else:
            raise ValueError('Unknown report.')

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get('raw'))

        mapping, ctype = self.get_mapping_and_type(report.get('feed.url'))

        document = ElementTree.fromstring(raw_report)

        for entry in document.iter(tag='entry'):

            entry_bytes = ElementTree.tostring(entry, encoding='utf-8', method='xml')
            entry_str = entry_bytes.decode("utf-8")

            event = self.new_event(report)
            extra = {}

            for item in entry:
                key = item.tag
                value = item.text

                if not value:
                    continue

                if value == 'undef':
                    continue

                if key is None:
                    self.logger.warning('Value without key found, skipping the'
                                        ' value: %r', value)
                    continue

                key_orig = key
                key = mapping[key]

                if key == "__IGNORE__":
                    continue

                if key == "source.fqdn" and event.is_valid('source.ip', value):
                    continue

                if key == "time.source":
                    value = value + " UTC"

                if key == "source.asn":
                    if value.upper().startswith("ASNA"):
                        continue
                    for asn in value.upper().split(','):
                        if asn.startswith("AS"):
                            value = asn.split("AS")[1]
                            break

                if key == "status":
                    if value == 'down':
                        value = 'offline'
                    elif value == 'up':
                        value = 'online'

                if key == 'extra':
                    extra[key_orig] = value
                    continue

                event.add(key, value)

            if extra:
                event.add('extra', extra)

            event.add('classification.type', ctype)
            event.add("raw", entry_str)
            self.send_message(event)

        self.acknowledge_message()


BOT = CleanMXParserBot
