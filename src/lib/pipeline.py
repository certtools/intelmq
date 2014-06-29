import pika

class Pipeline():
        
    def __init__(self, source_queue, destination_queues, host=None, port=None):
        if source_queue is not None:
            self.source_connection = pika.BlockingConnection()
            self.source_channel = self.source_connection.channel()
            self.source_channel.queue_declare(queue=source_queue, durable=True)
            self.source_generator = self.source_channel.consume(source_queue)

        self.destination_exchange = '-'.join(destination_queues)
        self.destination_connection = pika.BlockingConnection()
        self.destination_channel = self.destination_connection.channel()
        self.destination_channel.exchange_declare(exchange=self.destination_exchange, type='fanout')

        if destination_queues:
            for destination_queue in destination_queues:
                self.destination_channel.queue_declare(queue=destination_queue, durable=True)
                self.destination_channel.queue_bind(exchange=self.destination_exchange, queue=destination_queue)



    # Send a message to queue

    def send(self, message):
        if not hasattr(self, 'destination_channel'):
            return
            
        self.destination_channel.basic_publish(exchange=self.destination_exchange, routing_key='', body=unicode(message))



    # Get a message from queue without remove it from queue.

    def receive(self):
        if not hasattr(self, 'source_generator'):
            return

        self.last_method_frame, self.last_properties, self.last_body = self.source_generator.next()
        return self.last_body



    # Get a message from queue and remove it from queue.
        
    def acknowledge(self):
        if not hasattr(self, 'source_channel'):
            return
        self.source_channel.basic_ack(self.last_method_frame.delivery_tag)
