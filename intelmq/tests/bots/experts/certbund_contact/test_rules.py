# -*- coding: utf-8 -*-

"""
Testing rules
"""


import unittest

from intelmq.lib.message import Event

from intelmq.bots.experts.certbund_contact.rulesupport import \
     Context, keep_most_specific_contacts

from intelmq.bots.experts.certbund_contact.eventjson import \
     set_certbund_contacts


def build_event(contact_descriptions, section):
    """Build an empty event with contact info derived from contact_descriptions.
    """
    organisations = []
    matches = []
    for email, managed, fields in contact_descriptions:
        orgid = len(organisations)
        organisations.append({"annotations": [],
                              "contacts": [{"email": email,
                                            "is_primary_contact": True,
                                            "managed": managed,
                                            "role": "abuse-c",
                                            }],
                              "id": orgid,
                              "managed": managed,
                              "name": "Test Organisation %d" % (orgid,),
                              "sector": None})
        for field in fields:
            matches.append({"field": field, "managed": managed,
                            "organisations": [orgid], "address": None,
                            "annotations": []})

    event = Event()
    set_certbund_contacts(event, section,
                          {"matches": matches, "organisations": organisations})
    return event


class TestMostSpecificContact(unittest.TestCase):

    def check(self, contact_descriptions, expected_emails):
        event = build_event(contact_descriptions, "source")
        context = Context(event, "source", None)
        keep_most_specific_contacts(context)
        self.assertEqual(sorted(c.email
                                for c in context.all_contacts()),
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


class TestRuleContext(unittest.TestCase):

    def test_organisation_removal(self):
        event = build_event([("org1", "manual", ["fqdn", "ip"]),
                             ("org2", "manual", ["asn"])],
                            "source")
        context = Context(event, "source", None)
        # Check that the data matches what the actual test step expects:
        # The org IDs are 0 and 1
        self.assertEqual([org.orgid for org in context.organisations],
                         [0, 1])
        # the asn match references the organisation with ID 1:
        self.assertEqual([match.organisations
                          for match in context.matches
                          if match.field == "asn"],
                         [[1]])

        # Remove organisation 1
        context.organisations = [org
                                 for org in context.organisations
                                 if org.orgid != 1]

        # Now the ASN match should have an empty organisations list:
        self.assertEqual([match.organisations
                          for match in context.matches
                          if match.field == "asn"],
                         [])

        # It should not be possible to get the organisation for ID 1
        with self.assertRaises(KeyError):
            context.lookup_organisation(1)


if __name__ == "__main__":
    unittest.main()
