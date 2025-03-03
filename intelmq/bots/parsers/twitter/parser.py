# SPDX-FileCopyrightText: 2025 Institute for Common Good Technology, Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
A stub for backwards-compatibility
"""
from typing import Optional, List

from intelmq.bots.parsers.ioc_extractor.parser import IocExtractorParserBot


DEPRECATION_WARNING = "This bot is deprecated and will be removed in version 4.0. Use the 'IoC Extractor' bot instead."


class TwitterParserBot(IocExtractorParserBot):

    def init(self):
        self.logger.warn(DEPRECATION_WARNING)
        super().init()

    @staticmethod
    def check(parameters: dict) -> Optional[List[List[str]]]:
        return [["warning", DEPRECATION_WARNING]]


BOT = TwitterParserBot
