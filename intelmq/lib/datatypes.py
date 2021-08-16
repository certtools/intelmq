# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from enum import Enum
import json


class BotType(str, Enum):
    COLLECTOR   = "Collector"
    PARSER      = "Parser"
    EXPERT      = "Expert"
    OUTPUT      = "Output"

    def toJson(self):
        return self.value
