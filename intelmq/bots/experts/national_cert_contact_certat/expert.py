# SPDX-FileCopyrightText: 2017 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
from intelmq.lib.utils import create_request_session
from intelmq.lib.exceptions import MissingDependencyError

try:
    import requests
except ImportError:
    requests = None


URL = 'https://contacts.cert.at/cgi-bin/abuse-nationalcert.pl'


class NationalCERTContactCertATExpertBot(Bot):
    """Add country and abuse contact information from the CERT.at national CERT Contact Database. Set filter to true if you want to filter out events for Austria. Set overwrite_cc to true if you want to overwrite an existing country code value"""
    filter: bool = False
    http_verify_cert: bool = True
    overwrite_cc: bool = False

    def init(self):
        if requests is None:
            raise MissingDependencyError("requests")

        self.set_request_parameters()
        self.session = create_request_session(self)

    def process(self):
        event = self.receive_message()

        for section, key, abuse in \
            [('source', 'source.ip', 'source.abuse_contact'),
             ('destination', 'destination.ip', 'destination.abuse_contact'),
             ]:
            if key in event:
                parameters = {
                    'ip': event[key],
                    'bFilter': 'on' if self.filter else 'off',
                    'bShowNationalCERT': 'on',
                    'sep': 'semicolon',
                }
                req = self.session.get(URL, params=parameters)
                self.session.close()
                if not req.text:
                    # empty response
                    continue
                response = req.text.strip().split(';')

                ccfield = '{}.geolocation.cc'.format(section)
                if self.overwrite_cc or ccfield not in event:
                    event.add(ccfield, response[1])

                if abuse in event:
                    old_abuse = event[abuse]
                    event.change(abuse, old_abuse + ',' + response[3])
                else:
                    event.add(abuse, response[3])

        self.send_message(event)
        self.acknowledge_message()


BOT = NationalCERTContactCertATExpertBot
