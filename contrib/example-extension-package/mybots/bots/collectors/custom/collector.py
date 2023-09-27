"""
SPDX-FileCopyrightText: 2023 CERT.at GmbH <https://cert.at/>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

# Use your package as usual
from mybots.lib import common

from intelmq.lib.bot import CollectorBot


class ExampleAdditionalCollectorBot(CollectorBot):
    """
    This is an example bot provided by an extension package
    """

    def process(self):
        report = self.new_report()
        if self.raw:  # noqa: Set as parameter
            report['raw'] = common.return_value('example')
        self.send_message(report)


BOT = ExampleAdditionalCollectorBot
