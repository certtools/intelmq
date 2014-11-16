from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
import re

class NetFlowHTMLBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            for row in report.split('\n'):
                row = row.strip()

                if len(row) == 0 or not row.startswith('<td style'):
                    continue

                m = re.search("color: black;\">(\d+.\d+.\d+.\d+)</span></td><td>(.*)</td>", row)
                if m:
                    event = Event()

                    event.add("source_ip", m.group(1))
                    
                    event.add('feed', 'netflowhtml')
                    event.add('feed_url', 'https://tc.edu.tw/net/netflow/lkout/recent/1')
                    event.add('type', m.group(2))

                    event = utils.generate_source_time(event, "source_time")
                    event = utils.generate_observation_time(event, "observation_time")
                    event = utils.generate_reported_fields(event)
                
                    self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = NetFlowHTMLBot(sys.argv[1])
    bot.start()
