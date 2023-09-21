from intelmq.lib.bot import CollectorBot


class ExampleAdditionalCollectorBot(CollectorBot):
    """
    This is an example bot provided by extension package
    """

    def process(self):
        report = self.new_report()
        if self.raw:  # noqa: Set as parameter
            report['raw'] = 'test'
        self.send_message(report)


BOT = ExampleAdditionalCollectorBot
