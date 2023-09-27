"""
SPDX-FileCopyrightText: 2023 CERT.at GmbH <https://cert.at/>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

from intelmq.lib.bot import CollectorBot


class ExampleAdditionalCollectorBot(CollectorBot):
    """
    This is an example bot provided by an extension package
    """

    def process(self):
        report = self.new_report()
        if self.raw:  # noqa: Set as parameter
            report['raw'] = 'test'
        self.send_message(report)


BOT = ExampleAdditionalCollectorBot
