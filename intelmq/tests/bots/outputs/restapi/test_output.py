# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.outputs.restapi.output import RestAPIOutputBot


@test.skip_local_web()
class TestRestAPIOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RestAPIOutputBot
        cls.sysconfig = {"hierarchical_output": True,
                         "http_proxy": "localhost:8123",
                         "https_proxy": "localhost:8123",
                         "auth_token_name": "username",
                         "auth_token": "password",
                         "auth_type": "http_basic_auth",
                         "use_json": True,
                         "host": "http://localhost/"}
        cls.default_input_message = {'__type': 'Event'}

    def test_event(self):
        """
        Just tests if connection to proxy and webserver works.

        TODO: Check proxy and webserver
        """
        self.run_bot()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
