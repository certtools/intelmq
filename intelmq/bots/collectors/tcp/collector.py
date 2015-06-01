from intelmq.lib.bot import Bot, sys
import socket,base64

class IntelMQCollectorBot(Bot): 

    tcpserver=None
    
    def process(self):  
  
        if self.tcpserver==None:
	   self.tcpserver=TCPSock(self.parameters.host,self.parameters.port,self.send_message,self.logger)	   
	   self.tcpserver.start()		

    def killbot(self):
	self.tcpserver.stop()	
	self.logger.info("Disconnected") 	
	
	

class TCPSock():
            	    
    def __init__(self,host,port,object_send_msg,object_logger):
	self.collectors=object_send_msg	
	self.collectorl=object_logger
	self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (host,port)
	self.collectorl.info("starting up on %s port %s" % (host,port))
	self.sock.bind(server_address)
   	
    def start(self):
	self.sock.listen(10)
	self.collectorl.info("Server Started")
	while True:
	    connection, client_address = self.sock.accept()
	    try:
                self.collectorl.info("connection from %s" % client_address[0])   
		total_data=''
                while True:
            	    data = connection.recv(1024)
                    if not data:break
                    total_data+=data	
		event=unicode(base64.b64decode(total_data))                
		self.collectors(event)
		self.collectorl.info("Event Received")
            finally:
       		# Clean up the connection
                connection.close()         
            
    def stop(self):
	self.sock.close()


if __name__ == "__main__":
    bot = IntelMQCollectorBot(sys.argv[1])
    bot.start()
