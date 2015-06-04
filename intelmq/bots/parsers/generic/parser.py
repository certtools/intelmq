#import unicodecsv
#from cStringIO import StringIO
from intelmq.lib import utils
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime

#from intelmq.lib.bot import Bot, sys
#from intelmq.lib.message import Event
#from intelmq.bots import utils
import re


class GenericBot(Bot):
# Generic parser, will simply parse and add named group to event
# for example if you have the regex :
# '^\s*(?P<ip>(?:(?:\d){1,3}\.){3}\d{1,3})'
# then the mapping field do the mapping between capture group and
# envent field
# "mapping": "ip:source.ip"
# you may use multiple group with "," as delimiter
# You will have an item 'ip' in your event.

    def process(self):
        report = self.receive_message()

        if not report.contains("raw"):
            self.acknowledge_message()

        mapping_dict = {}
        # Will convert regex name to field
        for mapping in self.parameters.mapping.split(","):  # Convert config to array
            mkey, mvalue = mapping.split(":")
            mapping_dict[mkey]=mvalue

        # Invert Dict for defaults values
        rev_mapping_dict = dict(zip(mapping_dict.values(),mapping_dict.keys()))


        raw_report = utils.base64_decode(report.value("raw"))

        self.logger.debug("Will apply regex %s" % self.parameters.regex)
        if report:
            rowcount = 0
            for row in raw_report.split('\n'):  # For each line
                event = Event()
                match = re.search(self.parameters.regex, row)
                if match:
                    for key in match.groupdict():
                        rkey = mapping_dict[key]  # swap regexkey to field
                        event.add(rkey, match.groupdict()[key], sanitize=True)
                else:
                    continue  # skip lines without matching regex
                rowcount += 1
                # Get detail from parser parameters, will be nice to have it by
                # source parameters.. Avoid adding if parsed
                if not 'feed.name' in rev_mapping_dict:
                  event.add('feed.name', self.parameters.feed_name, sanitize=True)
                if not 'feed.url' in rev_mapping_dict:
                  event.add('feed.url', self.parameters.feed_url, sanitize=True)
                if not 'classification.type' in rev_mapping_dict:
                  event.add('classification.type', self.parameters.classification_type, sanitize=True)
                time_observation = DateTime().generate_datetime_now()
                event.add('time.observation', time_observation, sanitize=True)
                self.send_message(event)
            self.logger.info("Processed %d event" % rowcount)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = GenericBot(sys.argv[1])
    bot.start()
