# -*- encoding: utf-8 -*-
import unittest

import intelmq.lib.pipeline as pipeline


SAMPLES = {'normal': [b'Lorem ipsum dolor sit amet',
                      u'Lorem ipsum dolor sit amet'],
           'unicode': [b'\xc2\xa9\xc2\xab\xc2\xbb \xc2\xa4\xc2\xbc',
                       u'©«» ¤¼']}


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
        self.pipe.state['src'] = [SAMPLES['normal'][1]]
        self.assertEqual(SAMPLES['normal'][1], self.pipe.receive())

    def test_send(self):
        self.pipe.send(SAMPLES['normal'][1])
        self.assertEqual(SAMPLES['normal'][1],
                         self.pipe.state['dst'][0])

    def test_receive_unicode(self):
        self.pipe.state['src'] = [SAMPLES['unicode'][1]]
        self.assertEqual(SAMPLES['unicode'][1], self.pipe.receive())

    def test_send_unicode(self):
        self.pipe.send(SAMPLES['unicode'][1])
        self.assertEqual(SAMPLES['unicode'][1],
                         self.pipe.state['dst'][0])


class TestRedis(unittest.TestCase):
    def setUp(self):
        params = Parameters()
        params.broker = 'Redis'
        self.pipe = pipeline.PipelineFactory.create(params)
        self.pipe.set_queues('test', 'source')
        self.pipe.set_queues('test', 'destination')
        self.pipe.connect()

    def test_send_receive(self):
        self.pipe.send(SAMPLES['normal'][0])
        self.assertEqual(SAMPLES['normal'][0], self.pipe.receive())

    @unittest.expectedFailure
    def test_send_receive_unicode(self):
        self.pipe.send(SAMPLES['unicode'][1])
        self.assertEqual(SAMPLES['unicode'][1], self.pipe.receive())

    def tearDown(self):
        self.pipe.disconnect()


class TestZeromq(unittest.TestCase):
    def setUp(self):
        params = Parameters()
        params.broker = 'Zeromq'
        self.pipe = pipeline.PipelineFactory.create(params)
        self.pipe.source_queues('test')
        self.pipe.destination_queues(['test'])
        self.pipe.connect()

    def test_send_receive(self):
        self.pipe.send(SAMPLES['normal'][0])
        self.assertEqual(SAMPLES['normal'][0], self.pipe.receive())

    @unittest.expectedFailure
    def test_send_receive_unicode(self):
        self.pipe.send(SAMPLES['unicode'][1])
        self.assertEqual(SAMPLES['unicode'][1], self.pipe.receive())

    def tearDown(self):
        self.pipe.disconnect()


if __name__ == '__main__':
    unittest.main()
