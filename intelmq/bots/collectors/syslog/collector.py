from intelmq.lib.bot import Bot, sys
import SocketServer

class SyslogCollectorBot(Bot): 

    server=None
    
    def process(self):  
  
        if self.server==None:	
	   self.server=SocketServer.UDPServer((self.parameters.host,self.parameters.port),SyslogUDP)
	   self.server.collectorl=self.logger
	   self.server.collectors=self.send_message
	   self.server.serve_forever(poll_interval=0.5)


    def killbot(self):
	self.server.shutdown()	
	self.logger.info("Disconnected") 	
	
	

class SyslogUDP(SocketServer.BaseRequestHandler):
            	    
       	
    def handle(self):
	event = self.request[0].strip()
	socket = self.request[1]
	self.server.collectorl.info("Event received")
	self.server.collectors(event)



if __name__ == "__main__":
    bot = SyslogCollectorBot(sys.argv[1])
    bot.start()
