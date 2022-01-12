# SPDX-FileCopyrightText: 2021 CysihZ
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Fireeye Parser Bot
Retrieves a base64 encoded JSON-String from raw and converts it into an
event.
"""
import ipaddress

try:
    import xmltodict
except ImportError:
    xmltodict = None

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from intelmq.lib.exceptions import MissingDependencyError


class FireeyeParserBot(ParserBot):

    def init(self):
        if xmltodict is None:
            raise MissingDependencyError("xmltodict")

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get('raw'))
        my_dict = xmltodict.parse(raw_report)
        try:
            event = self.new_event(report)
            for indicator in my_dict['OpenIOC']['criteria']['Indicator']['IndicatorItem']:
                indicatorType = indicator['Context']['@search']
                if indicatorType == 'FileItem/Md5sum':
                    md5sum = indicator['Content']['#text']
                    event.add('malware.hash.md5', md5sum)
                if indicatorType == 'FileItem/Sha256sum':
                    self.logger.debug('FileItem/Sha256sum from UUID %r.', indicator['Content']['#text'])
                    sha256sum = indicator['Content']['#text']
                    event.add('malware.hash.sha256', sha256sum)
                    event.add('classification.type', 'malware')
                    event.add('raw', raw_report)
                    self.send_message(event)
                    data = raw_report.split('<Indicator id')
                    uuidres = data[0].split('"alert_id">')
                    uuid = uuidres[1].split('"')
                    self.logger.debug('My UUID is: %r.', uuid[0])
                    Indicator = data[2]
                    event = self.new_event(report)
                    if "Network" in Indicator:
                        event.add('classification.type', 'malware-distribution')
                        event.add('raw', raw_report)
                        event.add('malware.hash.sha256', sha256sum)
                        event.add('malware.hash.md5', md5sum)
                        fqdn = ""
                        urlpath = ""
                        IndicatorItem = Indicator.split('<IndicatorItem condition')
                        for datainIndicator in IndicatorItem:
                            if "search=" in datainIndicator:
                                search = datainIndicator.split('search="')
                                for searchIndicator in search:
                                    classification = ""
                                    if '"/>' in searchIndicator:
                                        context_search = searchIndicator.split('"/>')
                                        # context inhalt
                                        if context_search[0] == "Network/HTTP/RequestURI":
                                            classification = "destination.urlpath"
                                        if context_search[0] == "Network/HTTP/Host":
                                            classification = "destination.ip"
                                        if context_search[0] == "Network/Connection/RemotePort":
                                            classification = "destination.port"
                                        if context_search[0] == "Network/Connection/Protocol":
                                            classification = "protocol.transport"
                                        if context_search[0] == "Network/DNS":
                                            classification = "destination.fqdn"
                                    if 'Content' in searchIndicator:
                                        Content_search = searchIndicator.split('">')
                                        context = Content_search[1].split('</Content>')
                                        self.logger.debug("Classification: %r Context: %r.", classification, context[0])
                                        if fqdn != "" and urlpath != "":
                                            event.add("destination.url", f"http://{fqdn}{urlpath}")
                                            urlpath = ""
                                        if classification == "destination.ip":
                                            try:
                                                ipaddress.IPv4Network(context[0])
                                                event.add('destination.ip', context[0])
                                                break
                                            except ValueError:
                                                break
                                        elif classification == "destination.fqdn":
                                            fqdn = context[0]
                                            event.add(classification, context[0])
                                        elif classification == "destination.urlpath":
                                            urlpath = context[0]
                                            event.add(classification, context[0])
                                        elif classification == "destination.port":
                                            event.add(classification, int(context[0]))
                        self.send_message(event)
            self.acknowledge_message()
        except KeyError:
            self.logger.info("No IOCs Available.")


BOT = FireeyeParserBot
