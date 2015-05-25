from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
import re


class GenericBot(Bot):
# Generic parser, will simply parse and add named group to event
# for example if you have the regex :
# '^\s*(?P<ip>(?:(?:\d){1,3}\.){3}\d{1,3})'
# You will have an item 'ip' in your event.

    def process(self):

        self.logger.debug('starting process')
        report = self.receive_message()

        if report:
            # Bug ignore IPv6
            # Parse also with potential white char at the beginning
            regex_ip = '^\s*(?P<IP>(?:(?:\d){1,3}\.){3}\d{1,3})'
            rowcount = 0
            for row in report.split('\n'):  # For each line
                self.logger.debug(row)
                self.logger.debug(self.parameters.regex)
                event = Event()
                match = re.search(self.parameters.regex, row)
                if match:
                    matchtuple = match.groupdict()
                    for key in matchtuple:
                        event.add(key, matchtuple[key])
                else:
                    continue  # skip lines without matching regex
                rowcount += 1
                # Get detail from parser parameters, will be nice to have it by
                # source parameters..
                event.add('feed', self.parameters.feed)
                event.add('feed_url', self.parameters.feed_url)
                event.add('type', self.parameters.type)
                event = utils.parse_source_time(event, "source_time")
                event = utils.generate_observation_time(event,
                  "observation_time")
                event = utils.generate_reported_fields(event)
                self.send_message(event)
        self.logger.info("Processed %d event" % rowcount)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = GenericBot(sys.argv[1])
    bot.start()
