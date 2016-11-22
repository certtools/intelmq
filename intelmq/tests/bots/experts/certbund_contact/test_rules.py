# -*- coding: utf-8 -*-

"""
Testing rules
"""


import unittest

from intelmq.bots.experts.certbund_contact.rulesupport import \
     Contact, most_specific_contacts


class TestMostSpecificContact(unittest.TestCase):

    def check(self, contact_descriptions, expected_emails):
        contacts = [Contact(auto, email, "", matched_fields=fields)
                    for email, auto, fields in contact_descriptions]
        self.assertEqual(sorted(c.email
                                for c in most_specific_contacts(contacts)),
                         sorted(expected_emails))

    def test_manual_fqdn_only(self):
        self.check([("manual-fqdn", "manual", ["fqdn"])],
                   ["manual-fqdn"])

    def test_manual_auto_fqdn_only(self):
        self.check([("manual-fqdn", "manual", ["fqdn"]),
                    ("automatic-fqdn", "automatic", ["fqdn"])],
                   ["manual-fqdn"])

    def test_manual_auto_fqdn_ip_ignore_asn(self):
        self.check([("manual-fqdn", "manual", ["fqdn"]),
                    ("manual-ip-asn", "manual", ["ip", "asn"]),
                    ("automatic-asn", "automatic", ["asn"]),
                    ("automatic-asn", "automatic", ["fqdn"]),
                    ],
                   ["manual-fqdn", "manual-ip-asn"])

    def test_manual_auto_fqdn_asn_if_no_ip(self):
        self.check([("manual-fqdn", "manual", ["fqdn"]),
                    ("manual-asn", "manual", ["asn"]),
                    ("automatic-asn", "automatic", ["asn"]),
                    ("automatic-fqdn", "automatic", ["fqdn"]),
                    ],
                   ["manual-fqdn", "manual-asn"])

    def test_no_fqdn_asn(self):
        self.check([("manual-asn", "manual", ["asn"]),
                    ("automatic-asn", "automatic", ["asn"]),
                    ],
                   ["manual-asn"])

    def test_no_duplicated_contacts(self):
        self.check([("manual-fqdn", "manual", ["fqdn", "ip"]),
                    ("manual-asn", "manual", ["asn"]),
                    ("automatic-asn", "automatic", ["asn"]),
                    ("automatic-fqdn", "automatic", ["fqdn"]),
                    ],
                   ["manual-fqdn"])


if __name__ == "__main__":
    unittest.main()
