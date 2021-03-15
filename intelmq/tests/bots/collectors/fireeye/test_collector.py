import unittest
import pathlib
import secrets

import requests_mock

import intelmq.lib.test as test
from intelmq.bots.collectors.fireeye.collector_fireeye import FireeyeCollectorBot

RANDSTR = secrets.token_urlsafe(50)
ASSET_PATH_FIRST = pathlib.Path(__file__).parent / '../../../assets/fireeyeFristRequest.json'
ASSET_PATH_SECOND = pathlib.Path(__file__).parent / '../../../assets/fireeyeSecondRequest.xml'
PARAMETERS = {'dns_name': 'myfireeye.local', 'http_username': RANDSTR, 'http_password': RANDSTR, 'logging_level': 'DEBUG', 'request_duration': '24_hours', 'name': 'FireeyeCollector'}


def prepare_mocker(mocker):
<<<<<<< HEAD
    test.skip_exotic()
=======
>>>>>>> efa5499372c5c26d90bf4ccef648b1be8279834f
    mocker.post('https://myfireeye.local/wsapis/v2.0.0/auth/login', headers={'X-FeApi-Token': '1234567890'})
    mocker.get('https://myfireeye.local/wsapis/v2.0.0/alerts?duration=24_hours', text=ASSET_PATH_FIRST.read_text())
    mocker.get('https://myfireeye.local/wsapis/v2.0.0/openioc?alert_uuid=1591de22-4926-4124-b3ed-ffff96766295', text=ASSET_PATH_SECOND.read_text())


@requests_mock.Mocker()
class TestFireeyeCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    Testcases for the Fireeye collector bot
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FireeyeCollectorBot
        cls.use_cache = True

    def test_faulty_config(self, mocker):
        prepare_mocker(mocker)
        params = {'http_username': RANDSTR, 'http_password': RANDSTR, 'logging_level': 'DEBUG', 'request_duration': '24_hours'}
        with self.assertRaises(ValueError) as context:
            self.run_bot(iterations=1, parameters=params)
        exception = context.exception
        self.assertEqual(str(exception), 'No dns name provided.')

    def test_wrong_login(self, mocker):
        prepare_mocker(mocker)
        mocker.post('https://myfireeye.local/wsapis/v2.0.0/auth/login', status_code=500)
        self.run_bot(iterations=1, parameters=PARAMETERS, allowed_error_count=1, allowed_warning_count=1)
        self.assertLogMatches('ValueError: Could not connect to appliance check User/PW. HTTP response status code was 500.')

    def test_report_send(self, mocker):
        prepare_mocker(mocker)
        self.run_bot(iterations=1, parameters=PARAMETERS, allowed_warning_count=1)
        self.assertAnyLoglineEqual('Processed 1 messages since last logging.', 'INFO')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
