from intelmq.bots.parsers.dcu import lib
import unittest


class TestDCUParserLib(unittest.TestCase):
    """Tests if the dcu-parser library works as expected"""

    def setUp(self):
        # fake dcu records for later testing
        self.test_dcu = ["SinkHoleMessage",
                         "130366192837417292",
                         "B54-BASE",
                         "1.2.3.4",
                         "51762",
                         "AS0123",
                         "1.2.3.6",
                         "53",
                         "",
                         "US",
                         "",
                         "FakeCity",
                         "",
                         "10.99",
                         "11.23",
                         "0",
                         "0",
                         "/images/file.php",
                         "",
                         "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)",
                         "POST",
                         "1.1",
                         "",
                         "",
                         "",
                         "",
                         "",
                         ""]

    def test_windows_filetime(self):
        """Tests if the filetime conversion works correctly"""

        dcu_ts1 = "130366708739532588"
        dcu_ts2 = "130366708907647925"
        converted_ts1 = lib.convert_windows_timestamp(dcu_ts1)
        converted_ts2 = lib.convert_windows_timestamp(dcu_ts2)

        self.assertEqual('2014-02-12 09:27:53.953258+00:00', str(converted_ts1))
        self.assertEqual('2014-02-12 09:28:10.764792+00:00', str(converted_ts2))

    def test_dcu_conversion(self):
        """Tests if a dcu line is correctly converted to IntelMQ fields"""
        fields = dict(zip(lib.dcu_headers(), self.test_dcu))
        converted = lib.convert_dcu_fields(fields)

        self.assertEqual('2014-02-11 19:08:03.741729+00:00', converted["source_time"])
        self.assertEqual('blacklist', converted["type"])
        self.assertEqual('1.2.3.4', converted["source_ip"])
        self.assertEqual('51762', converted["source_port"])
        self.assertEqual('0123',  converted["source_asn"])
        self.assertEqual('FakeCity', converted["source_city"])
        self.assertEqual('B54-BASE', converted["malware"])

        self.assertEqual('1.2.3.6', converted["destination_ip"])
        self.assertEqual('53', converted["destination_port"])
        self.assertEqual('10.99', converted["source_latitude"])
        self.assertEqual('11.23', converted["source_longitude"])

        self.assertEqual('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)', converted["user_agent"])

    def test_threat_code_conversion(self):
        """Tests if a dcu threat code is converted correctly to an IntelMQ type"""

        # some known, relatively obvious dcu threat code to type conversions
        self.assertEqual("backdoor", lib.convert_threatcode_to_type("B106-Tapazom"))
        self.assertEqual("malware", lib.convert_threatcode_to_type("B106-Vobfus"))
        self.assertEqual("blacklist", lib.convert_threatcode_to_type("B54-BASE"))
        self.assertEqual("malware configuration", lib.convert_threatcode_to_type("B54-CONFIG"))

        # if we find something we don't know, then add unknown
        self.assertEqual("unknown", lib.convert_threatcode_to_type("Foobar"))

if __name__ == '__main__':
    unittest.main()
