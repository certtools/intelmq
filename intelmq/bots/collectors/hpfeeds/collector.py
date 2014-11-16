from intelmq.lib.bot import Bot, sys
import hpfeeds
import redis

class HpfeedsBot(Bot):

    def process(self):

        self.logger.info('connecting to %s:%s %s %s' % (self.parameters.broker_host,
                                                        self.parameters.broker_port,
                                                        self.parameters.ident,
                                                        self.parameters.secret))

        redis_host = '127.0.0.1'
        redis_port = 6379
        redis_db = 2
        redis_queue = 'hpfeeds'
        rc = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

        while  rc.llen(redis_queue) > 0:
            mesg = rc.rpop(redis_queue)
            self.send_message(mesg)

#        hpc = hpfeeds.new(self.parameters.broker_host, int(self.parameters.broker_port), self.parameters.ident, self.parameters.secret)
#        hpc.subscribe(self.parameters.channels_subscribe)
#        self.logger.info('connected to %s' % hpc.brokername)
#
#        def on_message(identifier, channel, payload):
#            decoded = ''
#            try: decoded = json.loads(str(payload))
#            except: decoded = {'raw': payload}
#            self.send_message(json.dumps(decoded))
#            self.logger.info('incoming message from {0} on channel {1}, length {2}'.format(identifier, channel, len(payload)))
#
#        def on_error(payload):
#            self.logger(' -> errormessage from server: {0}'.format(payload))
#            hpc.stop()
#
#
#        hpc.s.settimeout(0.01)
#        hpc.run(on_message, on_error)
#        hpc.close()



if __name__ == "__main__":
    bot = HpfeedsBot(sys.argv[1])
    bot.start()
