from intelmq.lib.pipeline import Pipeline
from intelmq.lib.utils import create_stream_logger


class TestPipeline(Pipeline):
    """This TestPipeline is a mock class for a pipeline,
       it behaves in most ways like a normal pipeline would do,
       with the exception that it doesn't need a message broker"""

    def __init__(self, state_dict):
        self.state = state_dict

    def connect(self):
        pass

    def disconnect(self):
        pass

    def sleep(self, intveral):
        # Passes through as we want a test to be deterministic
        pass

    def send(self, message):
        """Sends a message to the destination queues"""
        for destination_queue in self.destination_queues:
            if destination_queue in self.state:
                self.state[destination_queue].append(message)
            else:
                self.state[destination_queue] = [message]

    def receive(self):
        """Receives the last not yet acknowledged message"""
        if len(self.state.get(self.internal_queue, [])) > 0:
            return self.state[self.internal_queue].pop(0)

        # non blocking, we assume that the source queue ISN'T EMPTY
        # the current solution in the normal pipeline code
        # uses blocking as this is provided by the time of writing
        # by redis brpoplpush(,,0) the zero means that this code
        # will block forever. 
        #
        # In a test scenario this is not what
        # we want, so I hope that people don't expect it to behave
        # as if it mimics every aspect of a normal pipeline.

        first_msg = self.state[self.source_queue].pop(0)

        if self.internal_queue in self.state:
            self.state[self.internal_queue].append(first_msg)
        else:
            self.state[self.internal_queue] = [first_msg]

        return first_msg

    def acknowledge(self):
        """Removes a message from the internal queue and returns it"""
        return self.state.get(self.internal_queue, [None]).pop(0)
        
    def count_queued_messages(self, queues):
        """Returns the amount of queued messages 
           over all given queue names. 
           But only without a real message broker behind.
           As this is only for tests"""

        qdict = dict()
        for queue in queues:
            qdict[queue] = len(self.state.get(queue, []))
        return qdict

# other nice test related utility functions
def create_bot_test_configuration(bot_id, log_stream, state, params={}):
    """Creates a configuration which can be feed into a bot for
       testing it in an unit test"""

    config = {}

    config["system"] = {"logging_level": "DEBUG",
                        "logging_path": "/opt/intelmq/var/log/",  # not used
                        "http_proxy":  None,
                        "https_proxy": None}

    config["runtime"] = {bot_id: params, 
                         "__default__": {"rate_limit": 0,
                                         "retry_delay": 0}}
    config["pipeline"] = {bot_id:{"source-queue": ("%s-input" % bot_id),
                                  "destination-queues": ["%s-output" % bot_id]}}

    config["logger"] = create_stream_logger(log_stream, bot_id)

    config["source_pipeline"] = TestPipeline(state)
    config["destination_pipeline"] = TestPipeline(state)

    assert(config["source_pipeline"].state is config["destination_pipeline"].state)

    return config
