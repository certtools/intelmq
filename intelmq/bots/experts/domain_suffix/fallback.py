# -*- coding: utf-8 -*-
"""
A custom
"""


class PublicSuffixList(object):
    def __init__(self, source):
        self.suffixes = {}
        for line in source.readlines():
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

    def publicsuffix(self, domain):
        suffixes = self.suffixes
        suffix_path = []
        # we are converting here from punycode to unicode because it is easier with the !exceptions
        for level, suffix in enumerate(domain.encode().decode('idna').split('.')[::-1]):
            if suffix in suffixes:
                suffixes = suffixes[suffix]
                suffix_path.append(suffix)
            elif '*' in suffixes and not '!%s' % suffix in suffixes:
                suffix_path.append(suffix)
            else:
                break

        if suffix_path:
            return '.'.join(suffix_path[::-1])
