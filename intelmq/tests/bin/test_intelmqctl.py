# -*- coding: utf-8 -*-
import unittest

import intelmq.bin.intelmqctl as ctl


class TestIntelMQProcessManager(unittest.TestCase):
    def test_interpret_commandline(self):
        func = ctl.IntelMQProcessManager._interpret_commandline
        self.assertTrue(func(1, ('/usr/bin/python3', '/usr/bin/intelmq.bots.collectors.http.collector_http', 'test-collector'),
                             'intelmq.bots.collectors.http.collector_http', 'test-collector'))
        self.assertTrue(func(1, ('/usr/bin/python3', '/usr/local/bin/intelmq.bots.collectors.http.collector_http', 'test-collector'),
                             'intelmq.bots.collectors.http.collector_http', 'test-collector'))
        self.assertFalse(func(1, ('/usr/bin/python3', '/usr/bin/intelmq.bots.collectors.http.collector_http', 'test-collector'),
                             'intelmq.bots.collectors.http.collector_http', 'other-collector'))

        self.assertTrue(func(1, ('/usr/bin/python3', '/usr/bin/intelmqctl', 'run', 'test-collector'),
                             'intelmq.bots.collectors.http.collector_http', 'test-collector'))
        self.assertTrue(func(1, ('/usr/bin/python3', '/usr/local/bin/intelmqctl', 'run', 'test-collector'),
                             'intelmq.bots.collectors.http.collector_http', 'test-collector'))
        self.assertFalse(func(1, ('/usr/bin/python3', '/usr/bin/intelmqctl', 'run', 'test-collector'),
                              'intelmq.bots.collectors.http.collector_http', 'other-collector'))

        self.assertIn('could not be interpreted',
                      func(1, ('/usr/bin/python3', '/usr/bin/intelmqctl', 'run'),
                              'intelmq.bots.collectors.http.collector_http', 'other-collector'))
        self.assertIn('could not be interpreted',
                      func(1, ('/usr/bin/python3', '/usr/bin/intelmqctl'),
                              'intelmq.bots.collectors.http.collector_http', 'other-collector'))
        self.assertIn('could not be interpreted',
                      func(1, ('/usr/bin/python3'),
                              'intelmq.bots.collectors.http.collector_http', 'other-collector'))
        self.assertIn('could not be interpreted',
                      func(1, ('/usr/bin/python3', '/usr/bin/intelmq.bots.collectors.http.collector_http'),
                             'intelmq.bots.collectors.http.collector_http', 'test-collector'))
        self.assertIn('error',
                      func(1, (),
                              'intelmq.bots.collectors.http.collector_http', 'other-collector'))


if __name__ == '__main__':  # pragma: nocover
    unittest.main()
