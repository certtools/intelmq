# -*- coding: utf-8 -*-
"""
There are two different Formats: Breaches and Pastes
For Breaches, there are again two different Variants:
    * Callback Test: has field 'Email', Breach is a list of dictionaries
    * Real: has NO field 'Email', Breach is a dictionary
"""
import json

from intelmq.lib.bot import ParserBot
from intelmq.lib.utils import base64_decode


class HIBPCallbackParserBot(ParserBot):
    def recover_line(self, line):
        return json.dumps(line, sort_keys=True)

    def parse(self, report):
        return [json.loads(base64_decode(report["raw"]))]

    def parse_line(self, request, report):
        event = self.new_event(report)
        event['raw'] = self.recover_line(request)

        event["source.fqdn"] = request["Domain"]
        event["extra.domain_emails"] = request["DomainEmails"]
        try:
            event["extra.breach"] = request["Breach"]
            event['classification.identifier'] = 'breach'
            try:
                # for real
                event["time.source"] = request["Breach"]["AddedDate"]
            except TypeError:
                # for callback test, has multiple breaches
                pass
        except KeyError:
            pass
        try:
            event["extra.paste"] = request["Paste"]
            event['classification.identifier'] = 'paste'
        except KeyError:
            pass

        event['classification.taxonomy'] = 'information content security'
        event['classification.type'] = 'leak'

        for email in sorted(filter(bool, set([request.get('Email')] + request["DomainEmails"]))):
            if not email:
                continue
            event.add('source.account', email, overwrite=True)
            yield event.copy()


BOT = HIBPCallbackParserBot
