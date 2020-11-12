# -*- coding: utf-8 -*-
import json
import unittest

import requests_mock

import intelmq.lib.test as test
from intelmq.bots.outputs.restapi.output import RestAPIOutputBot


def request_callback(expected):
    def callback(request, context):
        if json.loads(request.text) == expected:
            context.status_code = 200
        else:
            context.status_code = 400
        return 'ok'
    return callback


class TestRestAPIOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RestAPIOutputBot
        cls.sysconfig = {"hierarchical_output": True,
                         "auth_token_name": "username",
                         "auth_token": "password",
                         "auth_type": "http_basic_auth",
                         "use_json": True,
                         "host": "http://localhost/"}
        cls.default_input_message = {'__type': 'Event',
                                     'source.ip': '10.0.0.1'}

    @requests_mock.Mocker()
    def test_event(self, mocker):
        """
        Test if data is posted correctly to webserver.
        """
        mocker.post('http://localhost/',
                    text=request_callback({'source': {'ip': '10.0.0.1'}}),
                    request_headers={'Authorization': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ=',
                                     'Content-Type': 'application/json; charset=utf-8'})
        self.run_bot()

    @requests_mock.Mocker()
    def test_status_check(self, mocker):
        """
        Test if response from webserver is correctly validated.
        """
        mocker.post('http://localhost/',
                    status_code=500,
                    request_headers={'Authorization': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ=',
                                     'Content-Type': 'application/json; charset=utf-8'})
        self.run_bot(allowed_error_count=1)
        self.assertLogMatches('requests.exceptions.HTTPError: 500 Server Error: None for url: http://localhost/',
                              'ERROR')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
