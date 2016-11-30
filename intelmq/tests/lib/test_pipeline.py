# -*- encoding: utf-8 -*-
"""
Testing the pipeline functions of intelmq.

We are testing sending and receiving on the same queue for Redis and
Pythonlist.
TODO: clear_queues
TODO: count_queued_messages
TODO: acknowledge
TODO: check internal representation of data in redis (like with Pythonlist)
"""

import unittest

import intelmq.lib.pipeline as pipeline
import intelmq.lib.test as test

SAMPLES = {'normal': [b'Lorem ipsum dolor sit amet',
                      'Lorem ipsum dolor sit amet'],
           'unicode': [b'\xc2\xa9\xc2\xab\xc2\xbb \xc2\xa4\xc2\xbc',
                       '©«» ¤¼']}


class Parameters(object):
    pass


class TestPythonlist(unittest.TestCase):

    def setUp(self):
        params = Parameters()
        params.broker = 'Pythonlist'
        self.pipe = pipeline.PipelineFactory.create(params)
        self.pipe.set_queues('src', 'source')
        self.pipe.set_queues('dst', 'destination')

    def test_receive(self):
        self.pipe.state['src'] = [SAMPLES['normal'][0]]
        self.assertEqual(SAMPLES['normal'][1], self.pipe.receive())

    def test_send(self):
        self.pipe.send(SAMPLES['normal'][1])
        self.assertEqual(SAMPLES['normal'][0],
                         self.pipe.state['dst'][0])

    def test_receive_unicode(self):
        self.pipe.state['src'] = [SAMPLES['unicode'][0]]
        self.assertEqual(SAMPLES['unicode'][1], self.pipe.receive())

    def test_send_unicode(self):
        self.pipe.send(SAMPLES['unicode'][1])
        self.assertEqual(SAMPLES['unicode'][0],
                         self.pipe.state['dst'][0])

    def test_count(self):
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.send(SAMPLES['normal'][1])
        self.pipe.send(SAMPLES['unicode'][0])
        self.assertEqual(self.pipe.count_queued_messages('dst'), {'dst': 3})

    def test_count_multi(self):
        self.pipe.state['src'] = [SAMPLES['normal'][0]]
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.send(SAMPLES['unicode'][0])
        self.assertEqual(self.pipe.count_queued_messages('src', 'dst'),
                         {'src': 1, 'dst': 2})


@test.skip_redis()
class TestRedis(unittest.TestCase):

    def setUp(self):
        params = Parameters()
        params.broker = 'Redis'
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
        self.pipe.send(SAMPLES['normal'][0])
        self.pipe.send(SAMPLES['normal'][1])
        self.pipe.send(SAMPLES['unicode'][0])
        self.assertEqual(self.pipe.count_queued_messages('test'), {'test': 3})

    def tearDown(self):
        self.pipe.disconnect()


if __name__ == '__main__':  # pragma: no cover  # pragma: no cover
    unittest.main()
