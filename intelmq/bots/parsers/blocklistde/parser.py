# -*- coding: utf-8 -*-
import posixpath
import sys
from urllib.parse import urlparse

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

MAPPING = {
    "all.txt": {
        "classification.type": "blacklist",
    },
    "ssh.txt": {
        "classification.type": "ids alert",
        "protocol.application": "ssh",
        "event_description.text": "IP reported as having run attacks on the "
                                  "service SSH",
    },
    "mail.txt": {
        "classification.type": "ids alert",
        "protocol.application": "smtp",
        "event_description.text": "IP reported as having run attacks on the "
                                  "service Mail, Postfix",
    },
    "apache.txt": {
        "classification.type": "ids alert",
        "protocol.application": "http",
        "event_description.text": "IP reported as having run attacks on the "
                                  "service Apache, Apache-DDoS, RFI-Attacks",
    },
    "imap.txt": {
        "classification.type": "ids alert",
        "protocol.application": "imap",
        "event_description.text": "IP reported as having run attacks on the "
        "service IMAP, SASL, POP3",
    },
    "ftp.txt": {
        "classification.type": "ids alert",
        "protocol.application": "ftp",
        "event_description.text": "IP reported as having run attacks on the "
                                  "service FTP",
    },
    "sip.txt": {
        "classification.type": "ids alert",
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
        "classification.type": "botnet drone",
        "protocol.application": "irc",
    },
    "bruteforcelogin.txt": {
        "classification.type": "brute-force",
        "event_description.text": "IP reported as having run attacks on "
                                  "Joomlas, Wordpress and other Web-Logins "
                                  "with Brute-Force Logins",
    }
}


class BlockListDEParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))
        raw_report = raw_report.strip()

        url = report.get('feed.url')
        path = urlparse(url).path
        filename = posixpath.basename(path)

        for row in raw_report.splitlines():
            event = Event(report)

            event.add('source.ip', row.strip())
            if filename in MAPPING:
                for key, value in MAPPING[filename].items():
                    event.add(key, value)
            else:
                event.add('classification.type', 'blacklist')

            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = BlockListDEParserBot(sys.argv[1])
    bot.start()
