from intelmq.lib.bot import Bot, sys
import socket,base64

class TCPCollector(Bot): 

    

    def init(self):
        self.logger.info("Starting up on %s port %s" % (self.parameters.host, self.parameters.port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.parameters.host, self.parameters.port))
        self.started=False
        
    
    
    def process(self):  
  
        if not self.started:  #not sure if this "if" is needed since sock.accept() has blocking behaviour, but this ensures that the method process runs the code only once
	   self.logger.info("Server Started")
	   self.sock.listen(10)
	   self.started=True
	   while True:
	   	connection, client_address = self.sock.accept()		
	   	try:
	       	    self.logger.info("Connection from %s" % client_address[0])
	       	    total_data=''
	            while True:
          	         data = connection.recv(1024)
                         if not data:break        
			 total_data+=data	
		    event=unicode(base64.b64decode(total_data))
		    if event:                
		       self.send_message(event)
		       self.logger.info("Event Received")
                finally:
       		    connection.close()  
   


    def killbot(self):
	self.sock.close()	
	self.logger.info("Disconnected") 	
	



if __name__ == "__main__":
    bot =  TCPCollector(sys.argv[1])
    bot.start()
