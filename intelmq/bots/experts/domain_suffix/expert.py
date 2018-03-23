# -*- coding: utf-8 -*-
"""
"""
import codecs

from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import InvalidArgument


ALLOWED_FIELDS = ['fqdn', 'reverse_dns']


class DomainSuffixExpertBot(Bot):
    suffixes = {}

    def init(self):
        self.field = self.parameters.field
        if self.field not in ALLOWED_FIELDS:
            raise InvalidArgument('key', got=self.field, expected=self.field)
        with codecs.open(self.parameters.suffix_file, encoding='UTF-8') as file_handle:
            for line in file_handle.readlines():
                line = line.strip()
                if line == '// ===END ICANN DOMAINS===':
                    break
                if not line or line.startswith('//'):
                    continue
                line_split = line.split('.')
                suffixes = self.suffixes
                for level, suffix in enumerate(line_split[::-1]):
                    if suffix in suffixes:
                        suffixes = suffixes[suffix]
                    else:
                        suffixes[suffix] = {}
                        suffixes = suffixes[suffix]
            else:
                raise ValueError('Could not detect end of ICANN Domain list. Please fix the list or report a bug.')

    def process(self):
        event = self.receive_message()
        for space in ('source', 'destination'):
            key = '.'.join((space, self.field))
            if key not in event:
                continue
            suffixes = self.suffixes
            suffix_path = []
            # we are converting here from punycode to unicode because it is easier with the exceptions
            for level, suffix in enumerate(event[key].encode().decode('idna').split('.')[::-1]):
                if suffix in suffixes:
                    suffixes = suffixes[suffix]
                    suffix_path.append(suffix)
                elif '*' in suffixes and not '!%s' % suffix in suffixes:
                    suffix_path.append(suffix)
                else:
                    break

            if suffix_path:
                event['.'.join((space, 'domain_suffix'))] = '.'.join(suffix_path[::-1])

        self.send_message(event)
        self.acknowledge_message()


BOT = DomainSuffixExpertBot
