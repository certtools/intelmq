# -*- coding: utf-8 -*-

import sys

from intelmq.lib import BlueCoatAPI
from intelmq.lib.bot import Bot

__author__ = 'Christoph Giese <cgi1> <C.Giese@telekom.de>'

class BlueCoatMitigationBot(Bot):

    def init(self):
        self.logger.info("Init of BlueCoat Mitigation Bot started...")
        self.bluecoat_api = BlueCoatAPI.BlueCoatAPI()
        self.logger.info("Init of BlueCoat Mitigation Bot finished!")

    def __get_mititgation_value(self, event):
        """ return the URL/IP/Domain which needs to be mitigated from one of the different event fields

        :param event:
        :return: string value
        """
        return event.get('source.ip', None) or \
               event.get('destination.ip', None) or \
               event.get('source.url', None) or \
               event.get('destination.url', None) or \
               event.get('source.fqdn', None) or \
               event.get('destination.fqdn', None)

    def process(self):
        """ Receives an event which contains a mitigation request (i.e. block at bluecoat proxy)

        :return: Nothing
        """

        event = self.receive_message()
        # Check if mitigation command is set
        if 'control.command' in event:
            self.logger.info("Received command: %s" % (event['control.command']))
            if event['control.command'] == 'mitigate':
                mitigation_value = self.__get_mititgation_value(event)
                response_code = self.bluecoat_api.submit_url(
                    url=mitigation_value,
                    submit_comment=self.parameters.submit_comment,
                    cat1=self.parameters.bc_category1,
                    cat2=self.parameters.bc_category2,
                    email=self.parameters.submitter_mail,
                    customTrackingID=123,
                    confidence=80)
                self.logger.info("Response code from BlueCoat: %s." % response_code)
                if response_code:
                    event.add('control.response_code', response_code)
                else:
                    event.add('control.response_code', 666)
                event.add('control.raw_response', response_code)
                self.send_message(event)
        else:
            self.logger.debug("Received event without control.command.")
        self.acknowledge_message()

if __name__ == "__main__":
    bot = BlueCoatMitigationBot(sys.argv[1])
    bot.start()
