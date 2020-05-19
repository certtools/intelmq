# -*- coding: utf-8 -*-
"""
The source provides a JSON file with a dictionary. The keys of this dict are
identifiers and the values are lists of domains.
"""
import json
import re

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.exceptions import InvalidValue

__all__ = ['N6StompParserBot']
mapping = {}
mapping['amplifier']    = {"taxonomy": "vulnerable",
                           "type": "vulnerable service",
                           "identifier": "amplifier"}
mapping['bots']         = {"taxonomy": "malicious code",
                           "type": "infected-system", "identifier": "malware-generic"}
mapping['backdoor']     = {"taxonomy": "intrusions",
                           "type": "backdoor", "identifier": "hacked server"}
mapping['cnc']          = {"taxonomy": "malicious code",
                           "type": "c2server", "identifier": "c&c server"}
mapping['dns-query']    = {"taxonomy": "other",
                           "type": "other", "identifier": "dns-query"}
mapping['dos-attacker'] = {"taxonomy": "availability",
                           "type": "ddos", "identifier": "dos-attacker"}
mapping['dos-victim']   = {"taxonomy": "availability",
                           "type": "ddos", "identifier": "dos-victim"}
mapping['flow']         = {"taxonomy": "other", "type": "other",
                           "identifier": "flow"}
mapping['flow-anomaly'] = {"taxonomy": "other",
                           "type": "other", "identifier": "flow-anomaly"}
mapping['fraud']        = {"taxonomy": "fraud",
                           "type": "account numbers", "identifier": "fraud"}
mapping['leak']         = {"taxonomy": "information content security",
                           "type": "leak", "identifier": "leak"}
mapping['malurl']       = {"taxonomy": "malicious code",
                           "type": "exploit", "identifier": "malurl"}
mapping['malware-action'] = {"taxonomy": "malicious code",
                             "type": "malware-configuration",
                             "identifier": "malware-configuration"}
mapping['phish']        = {"taxonomy": "fraud",
                           "type": "phishing", "identifier": "phishing"}
mapping['proxy']        = {"taxonomy": "other",
                           "type": "proxy", "identifier": "openproxy"}
mapping['sandbox-url']  = {"taxonomy": "malicious code",
                           "type": "malware", "identifier": "sandboxurl"}
mapping['scanning']     = {"taxonomy": "information gathering",
                           "type": "scanner", "identifier": "scanning"}
mapping['server-exploit'] = {"taxonomy": "malicious code",
                             "type": "exploit", "identifier": "server-exploit"}
mapping['spam']         = {"taxonomy": "abusive content",
                           "type": "spam", "identifier": "spam"}
mapping['spam-url']     = {"taxonomy": "abusive content",
                           "type": "spam", "identifier": "spam-url"}
mapping['tor']          = {"taxonomy": "other",
                           "type": "tor", "identifier": "tor exit node"}
mapping['webinject']    = {"taxonomy": "malicious code",
                           "type": "malware", "identifier": "malware"}
mapping['vulnerable']   = {"taxonomy": "vulnerable",
                           "type": "other", "identifier": "vulnerable"}
mapping['other']        = {"taxonomy": "other",
                           "type": "other", "identifier": "other"}


class N6StompParserBot(Bot):

    def process(self):
        report = self.receive_message()

        peek = utils.base64_decode(report.get("raw"))
        self.logger.debug("Peeking at event %r.", peek)
        if "TEST MESSAGE" in peek:
            self.logger.debug("Ignoring test message/event.")
            self.acknowledge_message()
            return

        # try to parse a JSON object
        event = self.new_event(report)
        dict_report = json.loads(peek)

        event.add("raw", report.get("raw"), sanitize=False)
        if "time" in dict_report:
            event.add("time.source", dict_report["time"])
        if "dip" in dict_report:
            event.add("destination.ip", dict_report["dip"])
        if "dport" in dict_report:
            event.add("destination.port", dict_report["dport"])
        if "md5" in dict_report:
            event.add("malware.hash.md5", dict_report["md5"])
        if "sha1" in dict_report:
            event.add("malware.hash.sha1", dict_report["sha1"])
        if "fqdn" in dict_report:
            if dict_report["fqdn"] == 'unknown':
                del dict_report["fqdn"]
            else:
                event.add("source.fqdn", dict_report["fqdn"])
        if "id" in dict_report:
            event["extra.feed_id"] = dict_report["id"]
        if "adip" in dict_report:
            event["extra.adip"] = dict_report["adip"]
        if "proto" in dict_report:
            event.add("protocol.transport", dict_report["proto"])
        if "sport" in dict_report:
            event.add("source.port", dict_report["sport"])
        if "url" in dict_report:
            event.add("source.url", dict_report["url"])
        if "confidence" in dict_report:
            event.add("extra.confidence", dict_report["confidence"])
        if "expires" in dict_report:
            event.add("extra.expires", DateTime.sanitize(dict_report["expires"]))
        if "source" in dict_report:
            event.add("extra.feed_source", dict_report["source"])
        if "name" in dict_report:
            mapping['bots']['identifier'] = dict_report["name"]
            try:
                event.add("malware.name", dict_report["name"])
            except InvalidValue:
                event.add("malware.name", re.sub("[^ -~]", '', dict_report["name"]))
                event.add("event_description.text", dict_report["name"])
        else:
            mapping['bots']['identifier'] = "malware-generic"

        if dict_report["type"] == "bl-update":
            event.add("classification.taxonomy", "other")
            event.add("classification.type", "blacklist")
        elif dict_report["category"] is not None:
            event.add("classification.taxonomy",
                      mapping[dict_report["category"]]["taxonomy"],
                      overwrite=True)
            event.add("classification.type",
                      mapping[dict_report["category"]]["type"],
                      overwrite=True)
            event.add("classification.identifier",
                      mapping[dict_report["category"]]["identifier"],
                      overwrite=True)

        # split up the event into multiple ones, one for each address
        for addr in dict_report.get('address', []):
            ev = self.new_event(event)
            ev.add("source.ip", addr["ip"])
            if ("asn" in addr):
                ev.add("source.asn", addr["asn"])
            if ("rdns" in addr):
                ev.add("source.reverse_dns", addr["rdns"])
            # XXX ignore for now, only relevant for flows
            # ev.add("source.dir", addr["dir"])
            if ("cc" in addr):
                ev.add("source.geolocation.cc", addr["cc"])
            self.send_message(ev)
        else:  # no address
            self.send_message(event)

        self.acknowledge_message()


BOT = N6StompParserBot
