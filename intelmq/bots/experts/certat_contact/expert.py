# -*- coding: utf-8 -*-
"""
CERT.at geolocate the national CERT abuse service
https://contacts.cert.at/cgi-bin/abuse-nationalcert.pl

HTTP GET: https://contacts.cert.at/cgi-bin/abuse-nationalcert.pl?ip=1.2.3.4
HTTP POST: https://contacts.cert.at/cgi-bin/abuse-nationalcert.pl

Options:
&bShowNationalCERT=on	Show national CERT contact info
&bShowHeader=on	Display a CSV header
&bVerbose=on	Display the source of the data, and other infos
&bFilter=off	Act as a filter: only show lines which geolocate to "AT"
&bKeepLoglines=off	Keep original log lines (separated by "#")
&sep={TAB, comma, semicolon, pipe}  	Separator for the (output) CSV format
"""
import sys

import requests

from intelmq.lib.bot import Bot

URL = 'https://contacts.cert.at/cgi-bin/abuse-nationalcert.pl'


class CERTatContactExpertBot(Bot):

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
                                   verify=self.parameters.http_verify_cert,
                                   )
                response = req.text.strip().split(';')

                ccfield = '{}.geolocation.cc'.format(section)
                if self.parameters.overwrite_cc or ccfield not in event:
                    event.add(ccfield, response[1])

                if abuse in event:
                    old_abuse = event[abuse]
                    event.update(abuse, old_abuse + ',' + response[3])
                else:
                    event.add(abuse, response[3])

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = CERTatContactExpertBot(sys.argv[1])
    bot.start()
