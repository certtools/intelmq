# -*- coding: utf-8 -*-
"""
The source provides a JSON file with a dictionary. The keys of this dict are
identifiers and the values are lists of domains.
"""

import json

from intelmq.lib import utils
from intelmq.lib.bot import Bot

__all__ = ['N6StompParserBot']
mapping = dict()
mapping['amplifier']    = {"taxonomy": "Vulnerable",
                           "type": "vulnerable service",
                           "identifier": "amplifier"}
mapping['bots']         = {"taxonomy": "Malicious Code",
                           "type": "botnet drone", "identifier": "generic-n6-drone"}
mapping['backdoor']     = {"taxonomy": "Intrusions",
                           "type": "backdoor", "identifier": "hacked server"}
mapping['cnc']          = {"taxonomy": "Malicious Code",
                           "type": "c&c", "identifier": "c&c server"}
mapping['dns-query']    = {"taxonomy": "Other",
                           "type": "other", "identifier": "ignore me"}
mapping['dos-attacker'] = {"taxonomy": "Availability",
                           "type": "ddos", "identifier": "dos-attacker"}
mapping['dos-victim']   = {"taxonomy": "Availability",
                           "type": "ddos", "identifier": "dos-victim"}
mapping['flow']         = {"taxonomy": "Other", "type": "other",
                           "identifier": "flow"}
mapping['flow-anomaly'] = {"taxonomy": "Other",
                           "type": "other", "identifier": "flow-anomaly"}
mapping['fraud']        = {"taxonomy": "Fraud",
                           "type": "account numbers", "identifier": "fraud"}
mapping['leak']         = {"taxonomy": "Information Content Security",
                           "type": "leak", "identifier": "leak"}
mapping['malurl']       = {"taxonomy": "Malicious Code",
                           "type": "exploit", "identifier": "malurl"}
mapping['malware-action'] = {"taxonomy": "Malicious Code",
                             "type": "malware configuration",
                             "identifier": "malware configuration"}
mapping['phish']        = {"taxonomy": "Fraud",
                           "type": "phishing", "identifier": "phishing"}
mapping['proxy']        = {"taxonomy": "Vulnerable",
                           "type": "proxy", "identifier": "open proxy"}
mapping['sandbox-url']  = {"taxonomy": "ignore",
                           "type": "ignore", "identifier": "ignore me"}
mapping['scanning']     = {"taxonomy": "Information Gathering",
                           "type": "scanner", "identifier": "scanning"}
mapping['server-exploit'] = {"taxonomy": "Malicious Code",
                             "type": "exploit", "identifier": "server-exploit"}
mapping['spam']         = {"taxonomy": "Abusive Content",
                           "type": "spam", "identifier": "spam"}
mapping['spam-url']     = {"taxonomy": "Abusive Content",
                           "type": "spam", "identifier": "spam-url"}
mapping['tor']          = {"taxonomy": "Other",
                           "type": "tor", "identifier": "tor exit node"}
mapping['webinject']    = {"taxonomy": "Malicious Code",
                           "type": "malware", "identifier": "malware"}
mapping['vulnerable']   = {"taxonomy": "Vulnerable",
                           "type": "other", "identifier": "vulnerable"}
mapping['other']        = {"taxonomy": "Vulnerable",
                           "type": "unknown", "identifier": "unknown"}


class N6StompParserBot(Bot):

    def process(self):
        report = self.receive_message()

        peek = utils.base64_decode(report.get("raw"))
        self.logger.debug("Peeking at event '%s'." % peek)
        if "TEST MESSAGE" in peek:
            self.logger.debug("Ignoring test message/event.")
            self.acknowledge_message()
            return

        # try to parse a JSON object
        event = self.new_event(report)
        dict_report = json.loads(peek)

        event.add("raw", report.get("raw"), sanitize=False)
        extra = {}
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
            extra['feed_id'] = dict_report["id"]
        if "adip" in dict_report:
            extra["adip"] = dict_report["adip"]
        if "proto" in dict_report:
            event.add("protocol.transport", dict_report["proto"])
        if "sport" in dict_report:
            event.add("source.port", dict_report["sport"])
        if "url" in dict_report:
            event.add("source.url", dict_report["url"])
        if ("category" in dict_report and "name" in dict_report and
                dict_report["category"] == 'bots'):
            event.add("malware.name", dict_report["name"])

        if ("name" in dict_report):
            mapping['bots']['identifier'] = dict_report["name"]
        else:
            mapping['bots']['identifier'] = "generic-n6-drone"

        if dict_report["category"] is not None:
            event.add("classification.taxonomy",
                      mapping[dict_report["category"]]["taxonomy"],
                      overwrite=True)
            event.add("classification.type",
                      mapping[dict_report["category"]]["type"],
                      overwrite=True)
            event.add("classification.identifier",
                      mapping[dict_report["category"]]["identifier"],
                      overwrite=True)

        if extra:
            event.add("extra", extra)

        # address is an array of JSON objects -> split the event
        if (not ("address" in dict_report or "fqdn" in dict_report)):
            # neither of them present -> currently we can't handle those
            self.logger.warn("ignoring event that we can't handle: "
                             "neither an address nor an fqdn given")
        elif ("fqdn" in dict_report):
            # need to handle domain based data later (for example via gethostbyname bot)
            ev = self.new_event(event)
            self.send_message(ev)
        else:
            # split up the event into multiple ones, one for each address
            for addr in dict_report['address']:
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

        self.acknowledge_message()


BOT = N6StompParserBot
