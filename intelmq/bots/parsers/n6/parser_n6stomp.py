# -*- coding: utf-8 -*-
"""
The source provides a JSON file with a dictionary. The keys of this dict are
identifiers and the values are lists of domains.
"""
from __future__ import unicode_literals

import json
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

__all__ = ['N6StompParserBot']
# FIXME: setting the identifier could be done in the modify.conf file.
# However, it was easier here. TBD.
mapping = dict()
mapping['amplifier']    = {"taxonomy": "Vulnerable",
                           "type": "vulnerable service",
                           "identifier": "amplifier"}
mapping['bots']         = {"taxonomy": "Malicious Code",
                           "type": "botnet drone"}
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
mapping['malware-action']={"taxonomy": "Malicious Code",
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
mapping['server-exploit']={"taxonomy": "Malicious Code",
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
                           "type": "other", "identifier": "unknown"}


class N6StompParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        peek = utils.base64_decode(report.value("raw"))
        self.logger.debug("Peeking at event '%s'." % peek)
        if "TEST MESSAGE" in peek:
            self.logger.debug("Ignoring test message/event.")
            self.acknowledge_message()
            return

        # try to parse a JSON object
        event = Event(report)
        dict_report = json.loads(peek)

        event.add("raw", report.value("raw"))
        event.add("extra", "{ \"_comment\": \"JSON dict for extra info\"")
        if ("time" in dict_report):
            event.add("time.source", dict_report["time"], sanitize=True)
        if ("dip" in dict_report):
            event.add("destination.ip", dict_report["dip"], sanitize=True)
        if ("dport" in dict_report):
            event.add("destination.port", dict_report["dport"],
                      sanitize=True)
        if ("md5" in dict_report):
            event.add("malware.hash", dict_report["md5"], sanitize=True)
        if ("sha1" in dict_report):
            event.add("malware.hash.sha1", dict_report["sha1"],
                      sanitize=True)
        if ("fqdn" in dict_report):
            event.add("source.fqdn", dict_report["fqdn"], sanitize=True)
        if ("id" in dict_report):
            # XXX FIXME: we need some discussion here if this should be a list,
            # JSON dict etc.? Maybe use append() ?
            event.add("extra", event.value("extra") + ', { "feed_id": "' + dict_report["id"] + '" }',
                      sanitize=True, force=True)
        if ("adip" in dict_report):
            event.add("extra", event.value("extra") + ', { "adip": ' + dict_report["adip"] +'" }',
                      sanitize=True, force=True)
        if ("proto" in dict_report):
            event.add("source.transport", dict_report["proto"],
                      sanitize=True)
        if ("source" in dict_report):
            event.add("feed.name", 'n6.' + dict_report["source"],
                      sanitize=True)
        if ("sport" in dict_report):
            event.add("source.port", dict_report["sport"], sanitize=True)
        if ("url" in dict_report):
            event.add("source.url", dict_report["url"], sanitize=True)
        if ("category" in dict_report and "name" in dict_report and
                dict_report["category"] == 'bots'):
            event.add("malware.name", dict_report["name"], sanitize=True)

        mapping['bots']['identifier'] = dict_report["name"]

        if dict_report["category"] is not None:
            event.add("classification.taxonomy",
                      mapping[dict_report["category"]]["taxonomy"],
                      sanitize=True)
            event.add("classification.type",
                      mapping[dict_report["category"]]["type"],
                      sanitize=True)
            event.add("classification.identifier",
                      mapping[dict_report["category"]]["identifier"],
                      sanitize=True)

        # address is an array of JSON objects -> split the event
        for addr in dict_report['address']:
            ev = Event(event)
            ev.add("source.ip", addr["ip"], sanitize=True)
            ev.add("source.asn", addr["asn"], sanitize=True)
            ev.add("source.reverse_dns", addr["rdns"], sanitize=True)
            # XXX ignore for now, only relevant for flows
            # ev.add("source.dir", addr["dir"], sanitize=True)
            ev.add("source.geolocation.cc", addr["cc"], sanitize=True)
            self.send_message(ev)

        self.acknowledge_message()


if __name__ == "__main__":
    bot = N6StompParserBot(sys.argv[1])
    bot.start()
