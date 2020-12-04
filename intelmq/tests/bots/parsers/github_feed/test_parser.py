import json
import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.github_feed.parser import GithubFeedParserBot

with open(os.path.join(os.path.dirname(__file__), 'example_ioc_strangereal_intel.json')) as handle:
    EXAMPLE_STRANGERINTEL_FILE_CONTENTS = handle.read()
    EXAMPLE_STRANGERINTEL_FILE_JSON = json.loads(EXAMPLE_STRANGERINTEL_FILE_CONTENTS)

EXAMPLE_STRANGEREALINTEL_REPORT = {
    "feed.url": "https://raw.githubusercontent.com/StrangerealIntel/DailyIOC/master/02-12-19/JSON/IOC_TA505_Nov19_2.json",
    "feed.name": "Strangereal Intel DailyIOC",
    "time.observation": "2019-03-01T01:01:01+00:00",
    "__type": "Report",
    "raw": utils.base64_encode(EXAMPLE_STRANGERINTEL_FILE_CONTENTS)
}

EXAMPLE_STRANGEREALINTEL_EVENT = {
    "feed.url": "https://raw.githubusercontent.com/StrangerealIntel/DailyIOC/master/02-12-19/JSON/IOC_TA505_Nov19_2.json",
    "feed.name": "Strangereal Intel DailyIOC",
    "time.observation": "2019-03-01T01:01:01+00:00",
    "classification.taxonomy": "other",
    "classification.type": "unknown",
    "__type": "Event"
}


@test.skip_exotic()
class TestGithubFeedParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for GithubFeedParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = GithubFeedParserBot
        cls.default_input_message = EXAMPLE_STRANGEREALINTEL_REPORT

    def test_no_processing_is_executed_for_the_feed_is_unknown(self):
        wrong_report = EXAMPLE_STRANGEREALINTEL_REPORT.copy()
        wrong_report['feed.url'] = 'https://raw.githubusercontent.com/DummyUser/NonexistingFeed/master/02-12-19/JSON/IOC_TA505_Nov19_2.json'

        self.input_message = wrong_report
        self.allowed_error_count = 1
        self.run_bot()

        self.assertRegexpMatchesLog("Unknown feed '{}'.".format(wrong_report['feed.url']))

    def test_extra_fields_are_present_in_generated_event(self):
        custom_report = EXAMPLE_STRANGEREALINTEL_REPORT.copy()
        custom_report['extra.file_metadata'] = {
            'sha': 'e345678934567893456789',
            'size': 111
        }

        self.input_message = custom_report
        self.run_bot()

        for event in self.get_output_queue():
            assert 'extra.file_metadata.sha' in event and 'extra.file_metadata.size' in event

    def test_strangerealintel_feed_processing_is_successful(self):
        self.run_bot()

        self.assertOutputQueueLen(len(EXAMPLE_STRANGERINTEL_FILE_JSON))

        sha256_event = EXAMPLE_STRANGEREALINTEL_EVENT.copy()
        sha256_event['malware.hash.sha256'] = EXAMPLE_STRANGERINTEL_FILE_JSON[0]['Indicator']
        sha256_event['event_description.text'] = EXAMPLE_STRANGERINTEL_FILE_JSON[0]['Description']
        sha256_event['classification.taxonomy'] = 'malicious code'
        sha256_event['classification.type'] = 'malware'
        sha256_event['raw'] = utils.base64_encode(str(EXAMPLE_STRANGERINTEL_FILE_JSON[0]))
        self.assertMessageEqual(0, sha256_event)

        md5_event = EXAMPLE_STRANGEREALINTEL_EVENT.copy()
        md5_event['malware.hash.md5'] = EXAMPLE_STRANGERINTEL_FILE_JSON[1]['Indicator']
        md5_event['event_description.text'] = EXAMPLE_STRANGERINTEL_FILE_JSON[1]['Description']
        md5_event['classification.taxonomy'] = 'malicious code'
        md5_event['classification.type'] = 'malware'
        md5_event['raw'] = utils.base64_encode(str(EXAMPLE_STRANGERINTEL_FILE_JSON[1]))
        self.assertMessageEqual(1, md5_event)

        domain_event = EXAMPLE_STRANGEREALINTEL_EVENT.copy()
        domain_event['source.fqdn'] = EXAMPLE_STRANGERINTEL_FILE_JSON[2]['Indicator']
        # description text is empty so no field is created
        # domain_event['event_description.text'] = EXAMPLE_STRANGERINTEL_FILE_JSON[2]['Description']
        domain_event['raw'] = utils.base64_encode(str(EXAMPLE_STRANGERINTEL_FILE_JSON[2]))
        self.assertMessageEqual(2, domain_event)

        ip_event = EXAMPLE_STRANGEREALINTEL_EVENT.copy()
        ip_event['source.ip'] = EXAMPLE_STRANGERINTEL_FILE_JSON[3]['Indicator']
        ip_event['event_description.text'] = EXAMPLE_STRANGERINTEL_FILE_JSON[3]['Description']
        ip_event['raw'] = utils.base64_encode(str(EXAMPLE_STRANGERINTEL_FILE_JSON[3]))
        self.assertMessageEqual(3, ip_event)

        url_event = EXAMPLE_STRANGEREALINTEL_EVENT.copy()
        url_event['source.url'] = EXAMPLE_STRANGERINTEL_FILE_JSON[4]['Indicator']
        url_event['event_description.text'] = EXAMPLE_STRANGERINTEL_FILE_JSON[4]['Description']
        url_event['raw'] = utils.base64_encode(str(EXAMPLE_STRANGERINTEL_FILE_JSON[4]))
        self.assertMessageEqual(4, url_event)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
