# -*- coding: utf-8 -*-
"""Microsoft Defender API to text expert bot

Reformats Microsoft Defender alerts to a format that looks good in
text, suitable for e.g. sending by e-mail.

The emitted event has an "output" field suitable for directly showing
to a human.

SPDX-FileCopyrightText: 2021 Linköping University <https://liu.se/>
SPDX-License-Identifier: AGPL-3.0-or-later

"""

from intelmq.lib.bot import Bot
from intelmq.lib.utils import base64_decode

import json


class DefenderToTextExpertBot(Bot):

    def process(self):
        event = self.receive_message()
        raw_alert = base64_decode(event.get("raw"))
        try:
            alert = json.loads(raw_alert)
        except json.decoder.JSONDecodeError as e:
            self.logger.error("JSON error loading alert: %s, Raw: %s.", str(e), raw_alert)
            alert = raw_alert

        self.logger.debug("Decoded alert: %s.", alert)

        event.add("output", json.dumps(alert, indent=4))
        self.send_message(event)
        self.acknowledge_message()


BOT = DefenderToTextExpertBot
