# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import json
from intelmq.lib.bot import Bot


class ECSExpertBot(Bot):
    """Write some fields to the output field in ECS format"""

    def process(self):
        msg = self.receive_message()

        ecs = {}

        # If the event source has no original timestamp, this value is
        # typically populated by the first time the event was received by the
        # pipeline.
        # (https://www.elastic.co/guide/en/ecs/current/ecs-base.html)
        ecs['@timestamp'] = msg['time.source'] if 'time.source' in msg else msg['time.observation']

        if 'feed.provider' in msg:
            ecs['event.provider'] = msg['feed.provider']
        if 'source.ip' in msg:
            ecs['server.ip'] = msg['source.ip']
        if 'source.fqdn' in msg:
            ecs['server.domain'] = msg['source.fqdn']
        if 'feed.name' in msg:
            ecs['event.dataset'] = msg['feed.name']

        msg.add("output", json.dumps(ecs))

        self.send_message(msg)
        self.acknowledge_message()


BOT = ECSExpertBot
