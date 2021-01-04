
"""
Fireeye Parser Bot
Retrieves a base64 encoded JSON-String from raw and converts it into an
event.
""" 
from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from intelmq.lib.message import MessageFactory
from intelmq.lib.utils import base64_decode
import json
import xmltodict


import ipaddress

class FireeyeParserBot(ParserBot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get('raw'))
        my_dict = xmltodict.parse(raw_report)
        try:
            event = self.new_event(report)
            for indicator in my_dict['OpenIOC']['criteria']['Indicator']['IndicatorItem']:
                hashValue = indicator['Content']['#text']
                indicatorType = indicator['Context']['@search']
                if indicatorType == 'FileItem/Md5sum':
                   event.add('malware.hash.md5', indicator['Content']['#text'])
                if indicatorType == 'FileItem/Sha256sum':
                   self.logger.debug('FileItem/Md5sum aus uuid'+ indicator['Content']['#text'])
                   event.add('malware.hash.sha256', indicator['Content']['#text'])
                   self.send_message(event)
                   data = raw_report.split('<Indicator id')
                   uuidres = data[0].split('"alert_id">')
                   uuid = uuidres[1].split('"')
                   self.logger.debug("My UUDI is:  " + uuid[0])
                   data.pop(0)
                   data.pop(0)
                   for Indicator in data:
                      event = self.new_event(report)
                      if "Network" in Indicator:
                         fqdn=""
                         urlpath=""
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
                                             #if context_search[0] == "Network/HTTP/UserAgent":
                                             #   classification = ""
                                          if 'Content' in searchIndicator:
                                             Content_search= searchIndicator.split('">')
                                             context = Content_search[1].split('</Content>')
                                             self.logger.debug(classification   +"   "+context[0])
                                             if fqdn != "" and urlpath!= "":
                                                event.add("destination.url", "http://"+fqdn+urlpath)
                                                fqdn=""
                                                urlpath=""
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
            self.logger.info("no Iocs Available")

BOT = FireeyeParserBot
