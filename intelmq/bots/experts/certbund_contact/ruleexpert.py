import sys

try:
    from intelmqmail.script import load_scripts
except ImportError as err:
    # when running as part of a unittest: skip more gracefully
    if 'unittest' in sys.modules:
        import unittest
        raise unittest.SkipTest("Importing intelmqmail.script failed.")

from intelmq.lib.bot import Bot
from intelmq.bots.experts.certbund_contact.rulesupport import Context
from intelmq.bots.experts.certbund_contact.eventjson import \
    del_certbund_contacts


class CERTBundRuleExpertBot(Bot):

    def init(self):
        self.script_directory = \
            getattr(self.parameters, "script_directory",
                    "/opt/intelmq/var/lib/bots/notification_rules")
        self.entry_points = load_scripts(self.script_directory,
                                         "determine_directives")
        if not self.entry_points:
            self.logger.warning("No rules loaded.")

        self.remove_contact_data = getattr(self.parameters,
                                           "remove_contact_data", "true")

    def process(self):
        self.logger.debug("Calling receive_message")
        event = self.receive_message()
        if event is None:
            self.acknowledge_message()
            return

        for section in ["source", "destination"]:
            context = Context(event, section, self.logger)
            self.logger.debug("Calling scripts for section %r.", section)
            for entry in self.entry_points:
                self.logger.debug("Calling script %r.", entry.filename)
                try:
                    finished = entry(context)
                    self.logger.debug("Script returned %r.", finished)
                finally:
                    self.logger.debug("Script finished.")
                if finished:
                    event = context.get_updated_event()
                    break
            if self.remove_contact_data:
                del_certbund_contacts(event, section)

        self.send_message(event)
        self.acknowledge_message()


BOT = CERTBundRuleExpertBot
