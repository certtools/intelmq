# -*- encoding: utf-8 -*-
"""
Testing the pipeline functions of intelmq.

We are testing sending and receiving on the same queue for Redis and
Pythonlist.
TODO: clear_queues
TODO: acknowledge
TODO: check internal representation of data in redis (like with Pythonlist)
"""
import os
import unittest

import intelmq.lib.pipeline as pipeline
import intelmq.lib.test as test

SAMPLES = {'normal': [b'Lorem ipsum dolor sit amet',
                      'Lorem ipsum dolor sit amet'],
           'unicode': [b'\xc2\xa9\xc2\xab\xc2\xbb \xc2\xa4\xc2\xbc',
                       '©«» ¤¼']}


class Parameters(object):
    pass


class TestPipeline(unittest.TestCase):

    def setUp(self):
        params = Parameters()
        self.pipe = pipeline.PipelineFactory.create(params)
        self.pipe.set_queues('test-bot-input', 'source')

    def test_creation_from_string(self):
        s = 'test-bot-output'
        self.pipe.set_queues(s, 'destination')
        self.assertEqual({'_default': [s]}, self.pipe.destination_queues)

    def test_creation_from_list(self):
        l = ['test-bot-output-1', 'test-bot-output-2']
        self.pipe.set_queues(l, 'destination')
        self.assertEqual({'_default': l}, self.pipe.destination_queues)

    def test_creation_from_dict(self):
        """ We assure that the queues are in the form of dict of lists, even if some queues were passed as mere strings. """
        d1 = {"_default": "complex-output", "special": ['test-bot-output-1', 'test-bot-output-2']}
        d2 = {"_default": ["complex-output"], "special": ['test-bot-output-1', 'test-bot-output-2']}
        self.pipe.set_queues(d1, 'destination')
        self.assertEqual(d2, self.pipe.destination_queues)


class TestPythonlist(unittest.TestCase):

    def setUp(self):
        params = Parameters()
        params.broker = 'Pythonlist'
        self.pipe = pipeline.PipelineFactory.create(params)
        self.pipe.set_queues('test-bot-input', 'source')
        self.pipe.set_queues('test-bot-output', 'destination')

    def test_receive(self):
        self.pipe.state['test-bot-input'] = [SAMPLES['normal'][0]]
        self.assertEqual(SAMPLES['normal'][1], self.pipe.receive())

    def test_send(self):
        self.pipe.send(SAMPLES['normal'][1])
        self.assertEqual(SAMPLES['normal'][0],
                         self.pipe.state['test-bot-output'][0])

    def test_receive_unicode(self):
        self.pipe.state['test-bot-input'] = [SAMPLES['unicode'][0]]
        self.assertEqual(SAMPLES['unicode'][1], self.pipe.receive())

    def test_send_unicode(self):
        self.pipe.send(SAMPLES['unicode'][1])
        self.assertEqual(SAMPLES['unicode'][0],
                         self.pipe.state['test-bot-output'][0])

    def test_count(self):
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.send(SAMPLES['normal'][1])
        self.pipe.send(SAMPLES['unicode'][0])
        self.assertEqual(self.pipe.count_queued_messages('test-bot-output'),
                         {'test-bot-output': 3})

    def test_count_multi(self):
        self.pipe.state['test-bot-input'] = [SAMPLES['normal'][0]]
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.send(SAMPLES['unicode'][0])
        self.assertEqual(self.pipe.count_queued_messages('test-bot-input', 'test-bot-output'),
                         {'test-bot-input': 1, 'test-bot-output': 2})

    def tearDown(self):
        self.pipe.state = {}


@test.skip_redis()
class TestRedis(unittest.TestCase):

    def setUp(self):
        params = Parameters()
        params.broker = 'Redis'
        setattr(params, 'source_pipeline_password', os.getenv('INTELMQ_TEST_REDIS_PASSWORD'))
        setattr(params, 'source_pipeline_db', 4)
        setattr(params, 'destination_pipeline_password', os.getenv('INTELMQ_TEST_REDIS_PASSWORD'))
        setattr(params, 'destination_pipeline_db', 4)
        self.pipe = pipeline.PipelineFactory.create(params)
        self.pipe.set_queues('test', 'source')
        self.pipe.set_queues('test', 'destination')
        self.pipe.connect()

    def clear(self):
        self.pipe.clear_queue(self.pipe.internal_queue)
        self.pipe.clear_queue(self.pipe.source_queue)

    def test_send_receive(self):
        """ Sending bytest and receiving unicode. """
        self.clear()
        self.pipe.send(SAMPLES['normal'][0])
        self.assertEqual(SAMPLES['normal'][1], self.pipe.receive())

    def test_send_receive_unicode(self):
        self.clear()
        self.pipe.send(SAMPLES['unicode'][1])
        self.assertEqual(SAMPLES['unicode'][1], self.pipe.receive())

    def test_count(self):
        self.clear()
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.send(SAMPLES['normal'][1])
        self.pipe.send(SAMPLES['unicode'][0])
        self.assertEqual(self.pipe.count_queued_messages('test'), {'test': 3})

    def tearDown(self):
        self.pipe.disconnect()
        self.clear()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
