import sys
import json

from intelmq.lib.bot import Bot

# The bot has two parameters:
#  - dropforsource
#  - dropfordestination
# If those are true, the bot replaces the ttl of a notification
# with -1 which indicates that no information should be sent.


class NoNotificationExpertBot(Bot):

    def __misconfigurationWarning(self):
        self.logger.warn("This bot is not configured properly."
                         "  Neither DropForSource nor DropForDestination"
                         "  are set.")

    def init(self):
        self.dropsrc = self.parameters.dropforsource
        self.dropdst = self.parameters.dropfordestination

        if not self.dropsrc and not self.dropdst:
            self.__misconfigurationWarning()

    def process(self):
        self.logger.debug("Calling receive_message")
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        if self.dropsrc and not self.dropdst:
            event = self.removeSrcNotificationInformation(event)

        elif self.dropdst and not self.dropsrc:
            event = self.removeDstNotificationInformation(event)

        elif self.dropsrc and self.dropdst:
            event = self.removeAllNotificationInformation(event)

        else:
            self.__misconfigurationWarning()

        self.send_message(event)
        self.acknowledge_message()

    def removeSrcNotificationInformation(self, event):
        return self.removeNotificationInformation(event, "source")

    def removeDstNotificationInformation(self, event):
        return self.removeNotificationInformation(event, "destination")

    def removeAllNotificationInformation(self, event):
        return self.removeNotificationInformation(event, "all")

    # Retrieve the JSON field "extra" of the event and search for the
    # dictionary called "certbund".
    # This dict can contain two additional fields "notify_source" and
    # "notify_destination"
    def removeNotificationInformation(self, event, where):
        if event and where in ["source", "destination", "all"]:
            if "extra" in event:
                extra = json.loads(event["extra"])

                cb = extra.get("certbund")
                src = cb.get("notify_source")
                dst = cb.get("notify_destination")

                if src and (where == "source" or where == "all"):
                    for element in src:
                        if "ttl" in element:
                            element["ttl"] = -1

                if dst and (where == "destination" or where == "all"):
                    for element in dst:
                        if "ttl" in element:
                            element["ttl"] = -1

                self.logger.debug("Replaced '%s' occurences of ttl with -1",
                                  where)

                # Now add the possibly modified extra-dict to the
                # event by overwriting the old one.
                event.add("extra", extra, force=True)

        return event


if __name__ == "__main__":
    bot = NoNotificationExpertBot(sys.argv[1])
    bot.start()
