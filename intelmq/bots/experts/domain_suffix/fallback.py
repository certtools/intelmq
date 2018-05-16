# -*- coding: utf-8 -*-
"""
A custom public suffix implementation
Only works with punycode, not unicode, as intelmq only uses
the first representation.
"""


class PublicSuffixList(object):
    def __init__(self, source, only_icann=None):
        self.suffixes = {}
        icann_section = False
        for line in source.readlines():
            line = line.strip()
            if line == '// ===BEGIN ICANN DOMAINS===':
                icann_section = True
            if line == '// ===END ICANN DOMAINS===':
                icann_section = False
            if not line or line.startswith('//') or not icann_section:
                continue
            line_split = line.split('.')
            suffixes = self.suffixes
            for level, suffix in enumerate(line_split[::-1]):
                if suffix in suffixes:
                    suffixes = suffixes[suffix]
                else:
                    suffixes[suffix] = {}
                    suffixes = suffixes[suffix]

    def publicsuffix(self, domain):
        if not domain:
            return
        suffixes = self.suffixes
        suffix_path = []
        # we are converting here from punycode to unicode because it is easier with the !exceptions
        for level, suffix in enumerate(domain.encode().decode('idna').split('.')[::-1]):
            if suffix in suffixes:
                suffixes = suffixes[suffix]
                suffix_path.append(suffix)
            elif '*' in suffixes and not '!%s' % suffix in suffixes:
                suffix_path.append(suffix)
                suffixes = suffixes['*']
            else:
                break

        if suffix_path:
            return '.'.join(suffix_path[::-1]).encode('idna')
