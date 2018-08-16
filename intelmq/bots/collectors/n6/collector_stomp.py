# -*- coding: utf-8 -*-

from intelmq.bots.collectors.stomp.collector import StompCollectorBot


class n6stompCollectorBot(StompCollectorBot):
    """ main class for the n6 STOMP protocol collector """

    def init(self):
        self.logger.warning("This module is deprecated and will be removed in "
                            "version 2.0. Please use intelmq.bots.collectors."
                            "stomp.collector instead.")
        super(n6stompCollectorBot, self).init()


BOT = n6stompCollectorBot
