import unittest
import os

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot


with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_telnet.csv')) as handle:
    TELNET_FILE = handle.read()
EXAMPLE_TELNET = {
    "raw": utils.base64_encode(TELNET_FILE),
    "__type": "Report",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "extra.file_name": "2019-01-01-scan_telnet.csv",
}
with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_vnc.csv')) as handle:
    TELNET_FILE = handle.read()
EXAMPLE_VNC = {
    "raw": utils.base64_encode(TELNET_FILE),
    "__type": "Report",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "extra.file_name": "2019-01-01-scan_vnc.csv",
}


class TestShadowserverMapping(test.BotTestCase, unittest.TestCase):

    def test_filename(self):
        self.assertEqual('scan_chargen',
                         ShadowserverParserBot._ShadowserverParserBot__is_filename_regex.search('2020-01-01-scan_chargen.csv').group(1))
        self.assertEqual('scan_chargen',
                         ShadowserverParserBot._ShadowserverParserBot__is_filename_regex.search('scan_chargen.csv').group(1))

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.sysconfig = {'feedname': ''}

    def test_changed_feed(self):
        """
        Tests if the parser correctly re-detects the feed for the second received report
        #1493
        """
        self.input_message = (EXAMPLE_TELNET, EXAMPLE_VNC)
        self.run_bot(iterations=2)



if __name__ == '__main__':  # pragma: no cover
    unittest.main()
