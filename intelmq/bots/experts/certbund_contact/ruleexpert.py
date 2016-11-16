import sys
import os
import json
import glob

from intelmqmail.script import load_scripts

from intelmq.lib.bot import Bot
from intelmq.bots.experts.certbund_contact.eventjson import \
     get_certbund_contacts, set_certbund_directives


class CERTBundRuleExpertBot(Bot):

    def init(self):
        self.script_directory = \
            getattr(self.parameters, "script_directory",
                    "/opt/intelmq/var/lib/bots/notification_rules")
        self.entry_points = load_scripts(self.script_directory,
                                         "determine_directives")
        if not self.entry_points:
            self.logger.warning("No rules loaded.")

    def process(self):
        self.logger.debug("Calling receive_message")
        event = self.receive_message()
        if event is None:
            self.acknowledge_message()
            return

        for section in ["source", "destination"]:
            contacts = get_certbund_contacts(event, section)
            for entry in self.entry_points:
                directives = entry(event, contacts, section)
                if directives:
                    set_certbund_directives(event, section, directives)
                    break

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = CERTBundRuleExpertBot(sys.argv[1])
    bot.start()
