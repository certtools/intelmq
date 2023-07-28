from intelmq.lib.bot import CollectorBot


class DummyCollectorBot(CollectorBot):
    """
    A dummy collector bot only for testing purpose.
    """

    def process(self):
        report = self.new_report()
        if self.raw:  # noqa: Set as parameter
            report['raw'] = 'test'
        self.send_message(report)


BOT = DummyCollectorBot
