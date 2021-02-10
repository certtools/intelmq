import unittest
import pathlib
import secrets

import requests_mock

import intelmq.lib.test as test
from intelmq.bots.collectors.shadowserver.collector_reports_api import ShadowServerAPICollectorBot

RANDSTR = secrets.token_urlsafe(50)
ASSET_PATH = pathlib.Path(__file__).parent / 'reports-list.json'
PARAMETERS = {'country': 'anarres', 'api_key': RANDSTR, 'secret': RANDSTR, 'logging_level': 'DEBUG', 'types': ['scan_smb', 'cisco_smart_install', 'nonexistent'], 'name': 'shadowservercollector'}
REPORT = {'__type': 'Report', 'extra.file_name': '2020-08-02-scan_smb-anarres-geo.csv', 'feed.accuracy': 100.0, 'feed.name': 'shadowservercollector', 'raw': 'e30='}


def prepare_mocker(mocker):
    mocker.post('https://transform.shadowserver.org/api2/reports/list', content=ASSET_PATH.read_bytes())
    mocker.post('https://transform.shadowserver.org/api2/reports/download', text='{}')


# Explicit skip_redis is required (although implicitly called by no_cache), otherwise fails in package build environments
@test.skip_redis()
@requests_mock.Mocker()
class TestShadowServerAPICollectorBot(test.BotTestCase, unittest.TestCase):
    """
    Testcases for the Shadowserver API collector bot
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowServerAPICollectorBot
        cls.use_cache = True

    def test_no_config(self, mocker):
        with self.assertRaises(ValueError) as context:
            self.run_bot(iterations=1)
        exception = context.exception
        self.assertEqual(str(exception), 'No api_key provided.')

    def test_faulty_config_0(self, mocker):
        parameters = {'api_key': RANDSTR}
        with self.assertRaises(ValueError) as context:
            self.run_bot(iterations=1, parameters=parameters)
        exception = context.exception
        self.assertEqual(str(exception), 'No secret provided.')

    def test_faulty_config_1(self, mocker):
        parameters = {'api_key': RANDSTR, 'secret': RANDSTR}
        with self.assertRaises(ValueError) as context:
            self.run_bot(iterations=1, parameters=parameters)
        exception = context.exception
        self.assertEqual(str(exception), 'No country provided.')

    def test_empty_response(self, mocker):
        mocker.post('https://transform.shadowserver.org/api2/reports/list', text='{}')
        self.run_bot(iterations=1, parameters=PARAMETERS)
        self.assertAnyLoglineEqual('Downloaded report list, 0 entries.', 'DEBUG')

    def test_reportlist_entries(self, mocker):
        prepare_mocker(mocker)
        self.run_bot(iterations=1, parameters=PARAMETERS)
        self.assertAnyLoglineEqual('Downloaded report list, 5 entries.', 'DEBUG')

    def test_reportlist_filtered(self, mocker):
        prepare_mocker(mocker)
        self.run_bot(iterations=1, parameters=PARAMETERS)
        self.assertAnyLoglineEqual('Reports list contains 2 entries after filtering.', 'DEBUG')

    def test_report_id(self, mocker):
        self.cache.flushdb()
        prepare_mocker(mocker)
        self.run_bot(iterations=1, parameters=PARAMETERS)
        self.assertAnyLoglineEqual('Downloading report with data: { "apikey": "' + RANDSTR + '" ,"id": "unnzVtn92tS9459rKIEz2J8qb7oJDv0Fa2feGUOiJLCDLqBXnN"}.', 'DEBUG')

    def test_report_sent(self, mocker):
        self.cache.flushdb()
        prepare_mocker(mocker)
        self.run_bot(iterations=1, parameters=PARAMETERS)
        self.assertAnyLoglineEqual('Sent report: 2020-08-02-cisco_smart_install-anarres-geo.csv.', 'DEBUG')

    def test_report_content(self, mocker):
        self.cache.flushdb()
        prepare_mocker(mocker)
        self.run_bot(iterations=1, parameters=PARAMETERS)
        self.assertMessageEqual(0, REPORT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
