from intelmq.lib.pipeline import Pipeline


class TestPipeline(Pipeline):
    def __init__(self, *args):
        pass

    def sleep(self, intveral):
        pass

    def receive(self):
        pass

    def acknowledge(self):
        pass
    
    def send(self, message):
        pass

    def count_queue_messages(self, queues):
        qdict = dict()
        for queue in queues:
        return qdict
