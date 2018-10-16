# -*- coding: utf-8 -*-
"""
CERT.at geolocate the national CERT abuse service
https://contacts.cert.at/cgi-bin/abuse-nationalcert.pl

HTTP GET: https://contacts.cert.at/cgi-bin/abuse-nationalcert.pl?ip=1.2.3.4
HTTP POST: https://contacts.cert.at/cgi-bin/abuse-nationalcert.pl

Options:
&bShowNationalCERT=on	Show national CERT contact info
&bShowHeader=on	Display a CSV header
&bVerbose=on	Display the source of the data, and other information
&bFilter=off	Act as a filter: only show lines which geolocate to "AT"
&bKeepLoglines=off	Keep original log lines (separated by "#")
&sep={TAB, comma, semicolon, pipe}  	Separator for the (output) CSV format
"""

from intelmq.lib.bot import Bot

try:
    import requests
except ImportError:
    requests = None


URL = 'https://contacts.cert.at/cgi-bin/abuse-nationalcert.pl'


class NationalCERTContactCertATExpertBot(Bot):
    def init(self):
        if requests is None:
            raise ValueError('Could not import requests. Please install it.')

        self.set_request_parameters()

    def process(self):
        event = self.receive_message()

        for section, key, abuse in \
            [('source', 'source.ip', 'source.abuse_contact'),
             ('destination', 'destination.ip', 'destination.abuse_contact'),
             ]:
            if key in event:
                parameters = {
                    'ip': event[key],
                    'bFilter': 'on' if self.parameters.filter else 'off',
                    'bShowNationalCERT': 'on',
                    'sep': 'semicolon',
                }
                req = requests.get(URL, params=parameters,
                                   proxies=self.proxy, headers=self.http_header,
                                   verify=self.http_verify_cert,
                                   timeout=self.http_timeout_sec
                                   )
                response = req.text.strip().split(';')

                ccfield = '{}.geolocation.cc'.format(section)
                if self.parameters.overwrite_cc or ccfield not in event:
                    event.add(ccfield, response[1])

                if abuse in event:
                    old_abuse = event[abuse]
                    event.change(abuse, old_abuse + ',' + response[3])
                else:
                    event.add(abuse, response[3])

        self.send_message(event)
        self.acknowledge_message()


BOT = NationalCERTContactCertATExpertBot
