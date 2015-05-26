from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
import re

# Simple ip will parse a raw ip list
class simpleip(Bot):
  def process(self):
    report = self.receive_message()

    if report:
      # Bug ignore IPv6
      # Parse also with potential white char at the beginning
      regex_ip = '^\s*(?P<IP>(?:(?:\d){1,3}\.){3}\d{1,3})'
      rowcount = 0
      for row in report.split('\n'):
        #self.logger.debug(row)
        if row.startswith('#') or row.startswith(";"): # avoid commented out
          continue
        event = Event()
        match = re.search(regex_ip, row)
        if match:
          ip = match.group("IP")
        else:
          continue    # skip lines without IP address
        rowcount += 1
        event.add("source_ip", ip)

        # Get detail from parser parameters, will be nice to have it by source parameters..
        event.add('feed', self.parameters.feed)
        event.add('feed_url', self.parameters.feed_url) 
        event.add('type', self.parameters.type)

        event = utils.parse_source_time(event, "source_time")
        event = utils.generate_observation_time(event, "observation_time")
        event = utils.generate_reported_fields(event)
        self.send_message(event)
      self.logger.info("Processed %d event"%rowcount)
    self.acknowledge_message()

if __name__ == "__main__":
  bot = simpleip(sys.argv[1])
  bot.start()
