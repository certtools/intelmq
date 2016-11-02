import sys
import os
import json
import glob

from intelmq.lib.bot import Bot
from intelmq.bots.experts.certbund_contact.eventjson import \
     get_certbund_contacts, set_certbund_directives


class CERTBundRuleExpertBot(Bot):

    def init(self):
        self.script_directory = \
            getattr(self.parameters, "script_directory",
                    "/opt/intelmq/var/lib/bots/notification_rules")
        self.entry_points = self.load_scripts(self.script_directory)
        if not self.entry_points:
            self.logger.warning("No rules loaded.")

    def load_scripts(self, script_directory):
        entry_points = []
        found_errors = False
        glob_pattern = os.path.join(glob.escape(script_directory),
                                    "[0-9][0-9]*.py")
        for filename in sorted(glob.glob(glob_pattern)):
            try:
                with open(filename, "r") as scriptfile:
                    my_globals = {}
                    exec(compile(scriptfile.read(), filename, "exec"),
                         my_globals)
                    entry = my_globals.get("determine_directives")
                    if entry is not None:
                        entry_points.append(entry)
                    else:
                        found_errors = True
                        self.logger.error("Cannot find entry point"
                                          " 'determine_directives' in %r",
                                          filename)
            except Exception:
                found_errors = True
                self.logger.exception("Exception while trying to find entry"
                                      " point in %r", filename)
        if found_errors:
            raise RuntimeError("Errors found while loading rules."
                               " See log file for details")
        return entry_points

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
