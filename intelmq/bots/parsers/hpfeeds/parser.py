from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
import redis
import json

class HPFeedsBot(Bot):

    def process(self):
        report = self.receive_message()
        self.logger.info(report)
        if report:
                
                #m = json.loads(report)
                m = report
           
                event = Event()
                for k in m.keys():
                    event.add(k, m.value(k))
                    
                event.add('feed', 'hpfeed')
                event.add('feed_url', m.value("sensorname"))

                event = utils.generate_source_time(event, "source_time")
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = HPFeedsBot(sys.argv[1])
    bot.start()
