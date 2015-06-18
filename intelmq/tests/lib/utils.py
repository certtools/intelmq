from intelmq.lib import utils
import unittest
import tempfile
import re
import os.path
import StringIO


class TestBaseUtils(unittest.TestCase):

    def test_file_logger_creation(self):
        """Tests if a logger can be created as mostly done 
           in the code with log()"""
        dirname = tempfile.mkdtemp()
        logger = utils.log(dirname, "test")

        logger.info("Hello")
        logger.warning("Oh lovely")
        logger.error("too bad")
        
        filename = os.path.join(dirname, "test.log")

        self.assertTrue(os.path.isfile(filename))
        log_lines = open(filename).readlines()

        self.check_log_lines(log_lines)

    def check_log_lines(self, log_lines):
        """Checks the given log lines for our chosen format"""
        log_format = "^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d+ - {name} - {type} - {text}"

        self.assertEqual(3, len(log_lines))

        expected_line = log_format.format(name="test", type="INFO", text="Hello")
        match = re.match(expected_line, log_lines[0])
        self.assertTrue(match, "Logline 0 was: '%s' expected '%s'" % (log_lines[0], expected_line))

        expected_line = log_format.format(name="test", type="WARNING", text="Oh lovely")
        match = re.match(expected_line, log_lines[1])
        self.assertTrue(match, "Logline 1 was: '%s' expected '%s'" % (log_lines[1], expected_line))
        
        expected_line = log_format.format(name="test", type="ERROR", text="too bad")
        match = re.match(expected_line, log_lines[2])
        self.assertTrue(match, "Logline 2 was: '%s' expected '%s'" % (log_lines[2], expected_line))

    def test_stream_logger_creation(self):
        """Tests if a logger for a stream can be generated with log().
           Why? This is useful for writing tests for loglines. 
           For example, when a bot needs to be tested if it generates a specific logline"""

        io = StringIO.StringIO()
        logger = utils.create_stream_logger(io, "test")

        logger.info("Hello")
        logger.warning("Oh lovely")
        logger.error("too bad")

        log_lines = io.getvalue().splitlines()

        self.check_log_lines(log_lines)

    def test_parse_logline(self):
        """Tests if the parse_logline() function works as expected"""
        line = "2015-05-29 21:00:24,379 - malware-domain-list-collector - ERROR - Something went wrong"

        fields = utils.parse_logline(line)

        self.assertIsInstance(fields, dict)
        self.assertEqual("Something went wrong", fields["message"])
        self.assertEqual("ERROR", fields["levelname"])
        self.assertEqual("malware-domain-list-collector", fields["name"])
        self.assertEqual("2015-05-29 21:00:24,379", fields["asctime"])


if __name__ == "__main__":
    unittest.main()
