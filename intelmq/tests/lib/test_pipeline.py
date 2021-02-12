# -*- encoding: utf-8 -*-
"""
Testing the pipeline functions of intelmq.

We are testing sending and receiving on the same queue for Redis and
Pythonlist.
TODO: clear_queues
TODO: check internal representation of data in redis (like with Pythonlist)
"""
import logging
import os
import time
import unittest
import sys

import intelmq.lib.pipeline as pipeline
import intelmq.lib.test as test
import intelmq.lib.exceptions as exceptions

SAMPLES = {'normal': [b'Lorem ipsum dolor sit amet',
                      'Lorem ipsum dolor sit amet'],
           'unicode': [b'\xc2\xa9\xc2\xab\xc2\xbb \xc2\xa4\xc2\xbc',
                       '©«» ¤¼'],
           'badencoding': b'foo\xc9bar',
           }


class Parameters(object):
    pass


class TestPipeline(unittest.TestCase):

    def setUp(self):
        params = Parameters()
        logger = logging.getLogger('foo')
        logger.addHandler(logging.NullHandler())
        self.pipe = pipeline.PipelineFactory.create(params,
                                                    logger=logger)
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
        logger = logging.getLogger('foo')
        logger.addHandler(logging.NullHandler())
        self.pipe = pipeline.PipelineFactory.create(params,
                                                    logger=logger)
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

    def test_has_message(self):
        self.assertFalse(self.pipe._has_message)
        self.pipe.state['test-bot-input'] = [SAMPLES['normal'][0]]
        self.pipe.receive()
        self.assertTrue(self.pipe._has_message)

    def test_reject(self):
        self.pipe.state['test-bot-input'] = [SAMPLES['normal'][0]]
        self.pipe.receive()
        self.pipe.reject_message()
        self.assertEqual(SAMPLES['normal'][1], self.pipe.receive())

    def test_acknowledge(self):
        self.pipe.state['test-bot-input'] = [SAMPLES['normal'][0]]
        self.pipe.receive()
        self.pipe.acknowledge()
        self.assertEqual(self.pipe.count_queued_messages('test-bot-input')['test-bot-input'], 0)
        self.assertEqual(self.pipe.count_queued_messages('test-bot-input-internal')['test-bot-input-internal'], 0)

    def test_bad_encoding_and_pop(self):
        self.pipe.state['test-bot-input'] = [SAMPLES['badencoding']]
        try:
            self.pipe.receive()
        except exceptions.DecodingError:
            pass
        self.pipe.acknowledge()
        self.assertEqual(self.pipe.count_queued_messages('test-bot-input')['test-bot-input'], 0)
        self.assertEqual(self.pipe.count_queued_messages('test-bot-input-internal')['test-bot-input-internal'], 0)

    def tearDown(self):
        self.pipe.state = {}


@test.skip_redis()
class TestRedis(unittest.TestCase):
    """
    We use the queue 'test' for both source and destination
    """

    def setUp(self):
        params = Parameters()
        params.broker = 'Redis'
        setattr(params, 'source_pipeline_host', os.getenv('INTELMQ_PIPELINE_HOST', 'localhost'))
        setattr(params, 'source_pipeline_password', os.getenv('INTELMQ_TEST_REDIS_PASSWORD'))
        setattr(params, 'source_pipeline_db', 4)
        setattr(params, 'destination_pipeline_host', os.getenv('INTELMQ_PIPELINE_HOST', 'localhost'))
        setattr(params, 'destination_pipeline_password', os.getenv('INTELMQ_TEST_REDIS_PASSWORD'))
        setattr(params, 'destination_pipeline_db', 4)
        logger = logging.getLogger('foo')
        logger.addHandler(logging.NullHandler())
        self.pipe = pipeline.PipelineFactory.create(params,
                                                    logger)
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

    def test_has_message(self):
        self.assertFalse(self.pipe._has_message)
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.receive()
        self.assertTrue(self.pipe._has_message)

    def test_reject(self):
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.receive()
        self.pipe.reject_message()
        self.assertEqual(SAMPLES['normal'][1], self.pipe.receive())

    def test_acknowledge(self):
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.receive()
        self.pipe.acknowledge()
        self.assertEqual(self.pipe.count_queued_messages('test')['test'], 0)
        self.assertEqual(self.pipe.count_queued_messages('test-internal')['test-internal'], 0)

    def test_bad_encoding_and_pop(self):
        self.pipe.send(SAMPLES['badencoding'])
        try:
            self.pipe.receive()
        except exceptions.DecodingError:
            pass
        self.pipe.acknowledge()
        self.assertEqual(self.pipe.count_queued_messages('test-bot-input')['test-bot-input'], 0)
        self.assertEqual(self.pipe.count_queued_messages('test-bot-input-internal')['test-bot-input-internal'], 0)

    def tearDown(self):
        self.pipe.disconnect()
        self.clear()


@test.skip_exotic()
class TestAmqp(unittest.TestCase):

    def setUp(self):
        params = Parameters()
        params.broker = 'Amqp'
        logger = logging.getLogger('foo')
        logger.addHandler(logging.NullHandler())
        self.pipe = pipeline.PipelineFactory.create(params,
                                                    logger=logger)
        self.pipe.set_queues('test', 'source')
        self.pipe.set_queues('test', 'destination')
        self.pipe.connect()

    def clear(self):
        self.pipe.clear_queue(self.pipe.internal_queue)
        self.pipe.clear_queue(self.pipe.source_queue)

    def test_send_receive(self):
        """ Sending and receiving bytes. """
        self.clear()
        self.pipe.connect()
        self.pipe.send(SAMPLES['normal'][0])
        self.assertEqual(SAMPLES['normal'][1], self.pipe.receive())

    def test_send_receive_unicode(self):
        """ Sending and receiving unicode. """
        self.clear()
        self.pipe.connect()
        self.pipe.send(SAMPLES['unicode'][1])
        self.assertEqual(SAMPLES['unicode'][1], self.pipe.receive())

    # it's crazy
    @unittest.expectedFailure
    def test_count(self):
        self.clear()
        self.pipe.connect()
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.send(SAMPLES['normal'][1])
        self.pipe.send(SAMPLES['unicode'][0])
        time.sleep(0.006)
        self.assertEqual(self.pipe.count_queued_messages('test'), {'test': 3})

    def test_has_message(self):
        self.assertFalse(self.pipe._has_message)
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.receive()
        self.assertTrue(self.pipe._has_message)

    def test_reject(self):
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.receive()
        self.pipe.reject_message()
        self.assertEqual(SAMPLES['normal'][1], self.pipe.receive())

    @unittest.skipIf(os.getenv('CI') == 'true' and sys.version_info[:2] == (3, 8),
                     'Fails on CI with Python 3.8')
    def test_acknowledge(self):
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.receive()
        self.pipe.acknowledge()
        self.assertEqual(self.pipe.count_queued_messages('test')['test'], 0)
        self.assertEqual(self.pipe.count_queued_messages('test-internal')['test-internal'], 0)

    def test_bad_encoding_and_pop(self):
        self.pipe.send(SAMPLES['badencoding'])
        try:
            self.pipe.receive()
        except exceptions.DecodingError:
            pass
        self.pipe.acknowledge()
        self.assertEqual(self.pipe.count_queued_messages('test-bot-input')['test-bot-input'], 0)
        self.assertEqual(self.pipe.count_queued_messages('test-bot-input-internal')['test-bot-input-internal'], 0)

    def tearDown(self):
        self.clear()
        self.pipe.disconnect()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
