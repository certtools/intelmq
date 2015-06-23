from intelmq.lib.bot import Bot
from intelmq.lib.test import create_bot_test_configuration

from intelmq.bots import utils
from intelmq.lib.message import Event

import unittest
import StringIO

import pdb
import json


class TestBot(Bot):
    """This is a TestBot for testing if a bot can be modified and
        tested. IT HAS ABSOLUTELY NO OTHER USE! You MUST NOT use 
        it for anything else as this TestCase"""

    def process(self):
        # This process method emulates a basic parser bot
        report = self.receive_message()

        self.logger.info("This is an awesome testbot!")
        self.logger.warning("It is soo awesome, we put also a warning there")
        
        if report:
            report = report.strip().split("\t")

            event = Event()
            
            event.add('feed', 'test')
            event.add('feed_url', 'hxx://127.0.0.1')
            event.add('type', 'brute-force')

            event.add('source_ip', report[0])
            event.add('destination_ip', report[1])
            event.add('source_time', report[2])

            event = utils.generate_source_time(event, "source_time")
            event = utils.generate_observation_time(event, "observation_time")
            event = utils.generate_reported_fields(event)

            self.send_message(event)
        self.acknowledge_message()


class TestBotInterface(unittest.TestCase):
    """Includes testcases for testing if a bot can be tested through
       an interface to it. This is basically only a rough testcase,
       on which better, more readable test abstractions can be built.

       It is basically an example of how to write a crude test for bots.
    """

    def setUp(self):
        self.maxDiff = None  # For unittest module, so that it prints long diffs

        self.bot_id = "test-bot"
        self.queue_state = {}
        self.log_stream = StringIO.StringIO()

        self.config = create_bot_test_configuration(self.bot_id,
                                                    self.log_stream,
                                                    self.queue_state)

        self.bot = TestBot(self.bot_id, config=self.config)

        # run it only once, no loop please
        # no blocking, no hassle testing it
        self.bot.run_once = True 

    def test_bot_start(self):
        """Tests if we can start a bot and feed data into 
            it and have a reasonable output"""

        self.queue_state["test-bot-input"] = ["1.1.2.3\t2.2.4.5\t2015-06-11 16:49:42.262784"]


        self.bot.start()
        loglines_buffer = self.log_stream.getvalue()
        loglines = loglines_buffer.splitlines()
        
        # if something new for bots are added then this test should break
        self.assertEquals(20, len(loglines), "Bot-Log was too long(%d lines):\n %s" % (len(loglines), loglines_buffer))
        
        # errors and warnings are IMHO prohibited when doing such a basic test
        self.assertNotRegexpMatches(loglines_buffer, "ERROR")

        self.assertRegexpMatches(loglines_buffer, "WARNING - It is soo awesome, we put also a warning there")

        # testing the internal behaviour of a pipeline, this is how the system at the moment behaves
        # and so we test that here. To have an almost real behaviour.
        self.assertListEqual(["test-bot-input", "test-bot-input-internal", "test-bot-output"], self.queue_state.keys())

        msg = json.loads(self.queue_state["test-bot-output"][0])

        expected_event = {u"feed": u"test",
                          u"feed_url": u"hxx://127.0.0.1",
                          u"type": u"brute-force",
                          u"reported_source_ip": u"1.1.2.3",
                          u"reported_destination_ip": u"2.2.4.5",
                          u"source_time": u"2015-06-11 16:49:42.262784"}

        self.assertDictContainsSubset(expected_event, msg)


if __name__ == '__main__':
    unittest.main()
