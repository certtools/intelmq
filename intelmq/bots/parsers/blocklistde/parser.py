# -*- coding: utf-8 -*-
import posixpath
from urllib.parse import urlparse

from intelmq.lib.bot import ParserBot

MAPPING = {
    "all.txt": {
        "classification.type": "blacklist",
    },
    "ssh.txt": {
        "classification.type": "ids-alert",
        "protocol.application": "ssh",
        "event_description.text": "IP reported as having run attacks on the "
                                  "service SSH",
    },
    "mail.txt": {
        "classification.type": "ids-alert",
        "protocol.application": "smtp",
        "event_description.text": "IP reported as having run attacks on the "
                                  "service Mail, Postfix",
    },
    "apache.txt": {
        "classification.type": "ids-alert",
        "protocol.application": "http",
        "event_description.text": "IP reported as having run attacks on the "
                                  "service Apache, Apache-DDoS, RFI-Attacks",
    },
    "imap.txt": {
        "classification.type": "ids-alert",
        "protocol.application": "imap",
        "event_description.text": "IP reported as having run attacks on the "
        "service IMAP, SASL, POP3",
    },
    "ftp.txt": {
        "classification.type": "ids-alert",
        "protocol.application": "ftp",
        "event_description.text": "IP reported as having run attacks on the "
                                  "service FTP",
    },
    "sip.txt": {
        "classification.type": "ids-alert",
        "protocol.application": "sip",
        "event_description.text": "IP reported as having run attacks on the "
                                  "service SIP, VOIP, Asterisk",
    },
    "bots.txt": {
        "classification.type": "spam",
        "event_description.text": "IP reported as having spammed on IRC, open "
                                  "forums, wikis or registration forms.",
    },
    "strongips.txt": {
        "classification.type": "blacklist",
        "event_description.text": "IP reported as having run attacks in last "
                                  "2 months",
    },
    "ircbot.txt": {
        "classification.type": "infected-system",
        "protocol.application": "irc",
    },
    "bruteforcelogin.txt": {
        "classification.type": "brute-force",
        "event_description.text": "IP reported as having run attacks on "
                                  "Joomlas, Wordpress and other Web-Logins "
                                  "with Brute-Force Logins",
    }
}


class BlockListDEParserBot(ParserBot):

    def parse_line(self, line, report):
        path = urlparse(report['feed.url']).path
        filename = posixpath.basename(path)

        event = self.new_event(report)
        event.add('source.ip', line)
        if filename in MAPPING:
            for key, value in MAPPING[filename].items():
                event.add(key, value)
        else:
            event.add('classification.type', 'blacklist')

        event.add("raw", line)
        yield event


BOT = BlockListDEParserBot
