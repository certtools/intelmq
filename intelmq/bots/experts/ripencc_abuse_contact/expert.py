# -*- coding: utf-8 -*-
from ..ripe.expert import RIPEExpertBot


class RIPENCCExpertDeprecatedBot(RIPEExpertBot):

    def init(self):
        self.logger.warning("The parser 'intelmq.bots.experts.ripencc_abuse_contact"
                            ".expert has been renamed to 'intelmq.bots."
                            "experts.ripe.expert'. This compatibility module "
                            "will be removed in version 3.0.")
        super().init()


BOT = RIPENCCExpertDeprecatedBot
