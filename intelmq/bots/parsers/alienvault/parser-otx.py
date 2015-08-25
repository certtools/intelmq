# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import json

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Event

HASHES = {
    'FileHash-SHA256' : 'SHA-256',
    'FileHash-SHA1' : 'SHA-1',
    'FileHash-MD5' : 'MD5'
}


class AlienVaultOTXParserBot(Bot):

    def process(self):
        report = self.receive_message()
        if (report is None or not report.contains("raw") or
                len(report.value("raw").strip()) == 0):
            self.acknowledge_message()
            return
        
        time_observation = DateTime().generate_datetime_now()
        raw_report = utils.base64_decode(report.value("raw"))

        for pulse in json.loads(raw_report):
            comment = "author: " + pulse['author_name'] + "; name: " + pulse['name'] + "; description: " + pulse['description']
            for indicator in pulse["indicators"]:
                event = Event()
                #hashes don't work - invalid keys
                #if indicator["type"] in ['FileHash-SHA256', 'FileHash-SHA1', 'FileHash-MD5']:
                #    event.add('source.artifact_hash', indicator["indicator"])
                #    event.add('source.artifact_hash_type', HASHES[indicator["type"]], sanitize = True)
                #fqdn
                if indicator["type"] in ['hostname', 'domain']:
                    event.add('source.fqdn', indicator["indicator"], sanitize = True)
                # IP addresses
                elif indicator["type"] in ['IPv4', 'IPv6']:
                    event.add('source.ip', indicator["indicator"], sanitize = True)
                #emails
                elif indicator["type"] == 'email':
                    event.add('source.email_address', indicator["indicator"], sanitize = True)
                #URLs
                elif indicator["type"] in ['URL', 'URI']:
                    event.add('source.url', indicator["indicator"], sanitize = True)
                #CIDR, FilePath, Mutex, CVE
                else:
                    continue

                event.add('comment', comment)
                event.add('classification.type', 'blacklist', sanitize = True)
                event.add('time.observation', time_observation, sanitize=True)
                event.add('feed.name', report.value("feed.name"))
                event.add("raw", json.dumps(indicator), sanitize=True)
                self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = AlienVaultOTXParserBot(sys.argv[1])
    bot.start()
