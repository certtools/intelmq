# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import posixpath
import sys
import urlparse

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

MAPPING = {
    "all.txt": {
        "event_classification.type": "blacklist",
    },
    "ssh.txt": {
        "event_classification.type": "ids alert",
        "protocol.application": "ssh",
        "description.text": "IP reported as having run attacks on the "
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
        "classification.type": "botnet drone"  # TODO: description
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

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.value("raw"))
        raw_report = raw_report.strip()

        url = report.value('feed.url')
        path = urlparse.urlparse(url).path
        filename = posixpath.basename(path)

        classification_type = 'blacklist'
        if filename in MAPPING:
            for key, value in MAPPING[filename].items():
                classification_type = value

        for row in raw_report.split('\n'):
            event = Event()

            event.add('source.ip', row.strip(), sanitize=True)
            event.add(key, classification_type, sanitize=True)

            event.add('time.observation', report.value(
                'time.observation'), sanitize=True)
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add("raw", row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = BlockListDEParserBot(sys.argv[1])
    bot.start()
