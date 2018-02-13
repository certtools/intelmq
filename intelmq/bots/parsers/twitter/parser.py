"""

Parser of text intended to obtain IOCs from tweets.
First substitutions are performed and then words in the text are compared with
'(/|^)([a-z0-9.-]+\.[a-z0-9]+?)([/:]|$)'
In the case of a match it is checked whether this can be a valid domain using get_tld
There is also a whitelist for filtering out good domains.


Parameters:
    domain_whitelist : domains that will be ignored in parsing

    substitutions : semicolon separated list of pairs
                    substitutions that will be made in the text,
                    for example " .com,.com" enables parsing of one fuzzy format
                                "[.];." enables the parsing of another fuzzy format

    classification_type : string with a valid classificationtype
"""

from intelmq.lib.bot import ParserBot
from intelmq.lib.bot import utils
from intelmq.lib.exceptions import InvalidArgument
from intelmq.lib.harmonization import ClassificationType
import re

try:
    from url_normalize import url_normalize
except ImportError:
    url_normalize = None

try:
    from tld import get_tld
    from tld.utils import update_tld_names
except ImportError:
    get_tld = None
    update_tld_names = None


class TwitterParserBot(ParserBot):
    def init(self):
        update_tld_names()
        self.domain_whitelist = []
        if getattr(self.parameters, "domain_whitelist", '') != '':
            self.domain_whitelist.extend(self.parameters.domain_whitelist.split(','))
        self.substitutions = []
        if getattr(self.parameters, "substitutions", '') != '':
            temp = self.parameters.substitutions.split(';')
            if len(temp) % 2 != 0:
                raise InvalidArgument(
                    'substitutions',
                    got=self.parameters.substitutions,
                    expected="even number of ; separeted strings")
            for i in range(int(len(temp) / 2)):
                self.substitutions.append([temp[2 * i], temp[2 * i + 1]])
        self.classification_type = getattr(self.parameters, "classification_type", "unknown")
        if not ClassificationType.is_valid(self.classification_type):
            self.classification_type = 'unknown'

    def get_domain(self, address):
        try:
            dom = re.search('(//|^)([a-z0-9.-]*[a-z]\.[a-z]+?(?:[/:].*|$))', address).group(2)
            if not self.in_whitelist(dom):
                if get_tld(url_normalize(dom), fail_silently=True):
                    return url_normalize(dom)
            return None
        except AttributeError:
            return None
        except UnicodeError:  # url_normalize's error, happens when something weird matches regex
            self.logger.info("Caught UnicodeError on %r.", address)
            return None

    def in_whitelist(self, domain: str) -> bool:
        for dom_clean in self.domain_whitelist:
            if re.match(dom_clean, domain):
                return True
        return False

    def get_data_from_text(self, text) -> list:
        data = []
        for sub in self.substitutions:  # allows for custom matches
            text = text.replace(sub[0], sub[1])
        tweet_text = text.split()
        tweet_text = [x.strip().lower() for x in tweet_text]
        for part in tweet_text:
            domain = self.get_domain(part)
            if domain:
                data.append(domain)
        return data

    def process(self):
        report = self.receive_message()
        text = utils.base64_decode(report["raw"])
        data = self.get_data_from_text(text)
        for url in data:
            event = self.new_event(report)
            event.add('raw', text)
            event.add('source.url', url)
            event.add('classification.type', self.classification_type)
            self.send_message(event)
        self.acknowledge_message()


BOT = TwitterParserBot
