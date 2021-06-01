# SPDX-FileCopyrightText: 2018 Karel
#
# SPDX-License-Identifier: AGPL-3.0-or-later

r"""

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
import re
import pkg_resources

from typing import Optional, Iterable

from intelmq.lib.bot import Bot, utils
from intelmq.lib.exceptions import InvalidArgument
from intelmq.lib.harmonization import ClassificationType
from intelmq.lib.exceptions import MissingDependencyError

try:
    from url_normalize import url_normalize
except ImportError:
    url_normalize = None

try:
    import tld.exceptions
    from tld import get_tld
    from tld.utils import update_tld_names
except ImportError:
    get_tld = None
    update_tld_names = None


class TwitterParserBot(Bot):
    """Parse tweets and extract IoC data. Currently only URLs are supported, a whitelist of safe domains can be provided"""
    default_scheme: Optional[str] = None
    domain_whitelist: str = 't.co'
    _domain_whitelist: Iterable[str] = []
    substitutions: str = ".net;[.]net"
    _substitutions: Iterable[str] = []
    classification_type: str = "blacklist"

    def init(self):
        if url_normalize is None:
            raise MissingDependencyError("url-normalize")
        url_version = pkg_resources.get_distribution("url-normalize").version
        if tuple(int(v) for v in url_version.split('.')) < (1, 4, 1) and self.default_scheme is not None:
            raise ValueError("Parameter 'default_scheme' given but 'url-normalize' version %r does not support it. "
                             "Get at least version '1.4.1'." % url_version)
        if get_tld is None:
            raise MissingDependencyError("tld")
        try:
            update_tld_names()
        except tld.exceptions.TldIOError:
            self.logger.info("Could not update TLD names cache.")
        if self.domain_whitelist != '':
            self._domain_whitelist.extend(self.domain_whitelist.split(','))
        if self.substitutions != '':
            temp = self.substitutions.split(';')
            if len(temp) % 2 != 0:
                raise InvalidArgument(
                    'substitutions',
                    got=self.substitutions,
                    expected="even number of ; separated strings")
            for i in range(int(len(temp) / 2)):
                self._substitutions.append([temp[2 * i], temp[2 * i + 1]])
        if not ClassificationType.is_valid(self.classification_type):
            self.classification_type = 'unknown'

        if self.default_scheme is not None:
            self.url_kwargs = {'default_scheme': self.default_scheme}
        else:
            self.url_kwargs = {}

    def get_domain(self, address):
        try:
            dom = re.search(r'(//|^)([a-z0-9.-]*[a-z]\.[a-z][a-z-]*?(?:[/:].*|$))', address).group(2)
            if not self.in_whitelist(dom):
                if get_tld(url_normalize(dom, **self.url_kwargs), fail_silently=True):
                    return url_normalize(dom, **self.url_kwargs)
            return None
        except AttributeError:
            return None
        except UnicodeError:  # url_normalize's error, happens when something weird matches regex
            self.logger.info("Caught UnicodeError on %r.", address)
            return None

    def in_whitelist(self, domain: str) -> bool:
        for dom_clean in self._domain_whitelist:
            if re.search(dom_clean, domain):
                return True
        return False

    def get_data_from_text(self, text) -> list:
        data = []
        for sub in self._substitutions:  # allows for custom matches
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
