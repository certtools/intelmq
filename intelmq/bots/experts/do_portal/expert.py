# -*- coding: utf-8 -*-
try:
    import requests
except ImportError:
    requests = None

from intelmq.lib.bot import Bot


class DoPortalExpertBot(Bot):
    def init(self):
        if requests is None:
            raise ValueError("Library 'requests' could not be loaded. Please install it.")

        self.set_request_parameters()

        self.url = self.parameters.portal_url + '/api/1.0/ripe/contact?cidr=%s'
        self.http_header.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "API-Authorization": self.parameters.portal_api_key
        })
        self.mode = self.parameters.mode

    def process(self):
        event = self.receive_message()
        if "source.ip" in event:
            req = requests.get(self.url % event['source.ip'],
                               headers=self.http_header,
                               auth=self.auth,
                               proxies=self.proxy,
                               verify=self.http_verify_cert,
                               cert=self.ssl_client_cert,
                               timeout=self.http_timeout_sec)
            if req.status_code == 404 and req.json()['message'].startswith("('no such cidr'"):
                result = []
            else:
                req.raise_for_status()
                result = req.json()['abusecs']

            if self.mode == 'append':
                existing = event.get("source.abuse_contact", '').split(',')
                combined = ','.join(existing + result).strip(',')
                event.add("source.abuse_contact", combined, overwrite=True)
            else:
                event.add("source.abuse_contact", ','.join(result), overwrite=True)

        self.send_message(event)
        self.acknowledge_message()


BOT = DoPortalExpertBot
