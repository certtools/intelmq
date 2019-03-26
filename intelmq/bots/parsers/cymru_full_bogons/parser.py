# -*- coding: utf-8 -*-
from ..cymru.parser_full_bogons import CymruFullBogonsParserBot


class CymruFullBogonsParserDeprecatedBot(CymruFullBogonsParserBot):

    def init(self):
        self.logger.warning("The parser 'intelmq.bots.parsers.cymru_full_bogons"
                            ".bots.parser has been renamed to 'intelmq.bots."
                            "parsers.cymru.full_bogons'. This compatibility "
                            "will be removed in version 2.0.")
        super().init()


BOT = CymruFullBogonsParserDeprecatedBot
