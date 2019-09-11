#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 17:03:33 2019

@author: sebastian
"""
import json

from intelmq.lib.bot import ParserBot
from intelmq.lib.utils import base64_decode


class HIBPCallbackParserBot(ParserBot):
    def recover_line(self, line):
        return json.dumps(line)

    def parse(self, report):
        return [json.loads(base64_decode(report["raw"]))]

    def parse_line(self, request, report):
        event = self.new_event(report)
        event['raw'] = self.recover_line(request)

        event['source.account'] = request['Email']
        event["source.fqdn"] = request["Domain"]
        event["extra.domain_emails"] = request["DomainEmails"]
        event["extra.breach"] = request["Breach"]
        event["extra.paste"] = request["Paste"]

        event['classification.taxonomy'] = 'information content security'
        event['classification.type'] = 'leak'
        yield event
