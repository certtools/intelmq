import json
from intelmq.lib.utils import base64_encode, base64_decode

message_taxonomy_map = {
  'Host actively distributes high-severity threat in the form of executable code.': 'malware',
  'Host is known to be distributing low-risk and potentially unwanted content.': 'malware',
  'Host is known source of phishing or other fraudulent content.': 'phishing',
  'Host is known to be actively distributing adware or other medium-risk software.': 'other',
  'Host is known source of active fraudulent content.': 'other'
}

from intelmq.lib.bot import ParserBot

class ESETParserBot(ParserBot):
  def parse(self, report): # yield single sections for parse_line to parse
    data = json.loads(base64_decode(report['raw']))
    for section in data:
      yield section

  def parse_line(self, line, report): # parse a section of the received report
    event = self.new_event(report)

    type = self._get_taxonomy(line['reason'])

    event.add('raw', base64_encode(json.dumps(line)))
    event.add('event_description.text', line['reason'])
    event.add('classification.type', type)

    if not line['ip'] in [line['domain'], None]:
      event.add('source.fqdn', line['domain']) # IP addresses are not permitted, only domain names

    event.add('source.ip', line['ip'])

    if 'domain_last_seen' in line:
      event.add('time.source', line['domain_last_seen'])
      event.add('source.url', line['url'])
    else:
      event.add('time.source', line['last_seen'])

    event.add('feed.name', 'ESET Threat Intelligence Service')
    event.add('feed.provider', 'ESET')
    event.add('feed.url', 'https://eti.eset.com/taxiiservice/discovery')
    event.add('feed.documentation', 'https://www.eset.com/int/business/services/threat-intelligence/')

    yield event


  @staticmethod
  def _get_taxonomy(reason):
    tax = message_taxonomy_map.get(reason, None)
    if tax: # was found in dictionary
      return tax
    elif reason.startswith('Host is used as command and control server'): # dynamic section after that
      return 'c2server'
    else:
      return 'other'

BOT = ESETParserBot
