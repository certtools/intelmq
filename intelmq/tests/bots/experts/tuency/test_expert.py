"""
© 2021 Sebastian Wagner <wagner@cert.at>

SPDX-License-Identifier: AGPL-3.0-or-later

This unittest can test the bot against a read tuency instance as well as using requests mock.
The latter is the default while the first is only in use if a tunency instance URL and authentication token is given a environment variable.
"""

import os
import unittest

from intelmq.lib.test import BotTestCase
from intelmq.bots.experts.tuency.expert import TuencyExpertBot

import requests_mock


INPUT = {
    "__type": "Event",
    "classification.taxonomy": "availability",
    "classification.type": "system-compromise",
    "classification.identifier": "hacked-server",
    "feed.provider": "Some Provider",
    "feed.name": "FTP",
    "feed.code": "ftp",
    "source.ip": "123.123.123.23",
    "source.fqdn": "www.example.at",
}
INPUT_IP = INPUT.copy()
del INPUT_IP["source.fqdn"]
INPUT_IP["source.abuse_contact"] = "abuse@example.com"
INPUT_DOMAIN = INPUT.copy()
del INPUT_DOMAIN["source.ip"]
OUTPUT = INPUT.copy()
OUTPUT_IP = INPUT_IP.copy()
OUTPUT_IP["extra.notify"] = False
OUTPUT_IP["source.abuse_contact"] = "test@ntvtn.de"
OUTPUT_IP["extra.constituency"] = "Tenant1,Tenant2"
OUTPUT_IP_NO_OVERWRITE = OUTPUT_IP.copy()
OUTPUT_IP_NO_OVERWRITE["source.abuse_contact"] = "abuse@example.com"
OUTPUT_DOMAIN = INPUT_DOMAIN.copy()
OUTPUT_DOMAIN["extra.ttl"] = 24 * 60 * 60  # 1 day
OUTPUT_DOMAIN["source.abuse_contact"] = "abuse+www@example.at"
OUTPUT_BOTH = OUTPUT.copy()
OUTPUT_BOTH["extra.ttl"] = 24 * 60 * 60  # 1 day
OUTPUT_BOTH["source.abuse_contact"] = "test@ntvtn.de,abuse+www@example.at"
EMPTY = {"__type": "Event", "comment": "foobar"}
UNKNOWN_IP = INPUT_IP.copy()
UNKNOWN_IP["source.ip"] = "10.0.0.1"


PREFIX = (
    "http://localhost/intelmq/lookup?classification_taxonomy=availability"
    "&classification_type=system-compromise&feed_provider=Some+Provider"
    "&feed_status=production"
)


def prepare_mocker(mocker):
    # IP address
    mocker.get(
        f"{PREFIX}&ip=123.123.123.23&feed_name=FTP",
        request_headers={"Authorization": "Bearer Lorem ipsum"},
        json={
            "ip": {
                "destinations": [
                    {
                        "source": "portal",
                        "name": "Thurner",
                        "contacts": [{"email": "test@ntvtn.de"}],
                    }
                ]
            },
            "suppress": True,
            "interval": {"unit": "days", "length": 1},
            "constituencies": ["Tenant1", "Tenant2"],
        },
    )

    # Domain:
    mocker.get(
        f"{PREFIX}&domain=www.example.at&feed_name=FTP",
        request_headers={"Authorization": "Bearer Lorem ipsum"},
        json={
            "domain": {
                "destinations": [
                    {
                        "source": "portal",
                        "name": "EineOrganisation",
                        "contacts": [{"email": "abuse+www@example.at"}],
                    }
                ]
            },
            "suppress": False,
            "interval": {"unit": "days", "length": 1},
        },
    )
    # Both
    mocker.get(
        f"{PREFIX}&ip=123.123.123.23&domain=www.example.at&feed_name=FTP",
        request_headers={"Authorization": "Bearer Lorem ipsum"},
        json={
            "ip": {
                "destinations": [
                    {
                        "source": "portal",
                        "name": "Thurner",
                        "contacts": [{"email": "test@ntvtn.de"}],
                    }
                ]
            },
            "domain": {
                "destinations": [
                    {
                        "source": "portal",
                        "name": "EineOrganisation",
                        "contacts": [{"email": "abuse+www@example.at"}],
                    }
                ]
            },
            "suppress": False,
            "interval": {"unit": "day", "length": 1},
        },
    )

    # Unknown IP address
    mocker.get(
        f"{PREFIX}&ip=10.0.0.1&feed_name=FTP",
        request_headers={"Authorization": "Bearer Lorem ipsum"},
        json={"ip": {"destinations": [], "netobject": None}},
    )

    # feed_code
    mocker.get(
        f"{PREFIX}&ip=123.123.123.23&feed_code=ftp",
        request_headers={"Authorization": "Bearer Lorem ipsum"},
        json={
            "ip": {
                "destinations": [
                    {
                        "source": "portal",
                        "name": "Thurner",
                        "contacts": [{"email": "test+code@ntvtn.de"}],
                    }
                ]
            },
            "suppress": False,
            "interval": {"unit": "days", "length": 1},
            "constituencies": ["Tenant1", "Tenant2"],
        },
    )

    # classification identifier
    mocker.get(
        f"{PREFIX}&ip=123.123.123.23&feed_name=FTP&classification_identifier=hacked-server",
        request_headers={"Authorization": "Bearer Lorem ipsum"},
        json={
            "ip": {
                "destinations": [
                    {
                        "source": "portal",
                        "name": "Thurner",
                        "contacts": [{"email": "test+identifier@ntvtn.de"}],
                    }
                ]
            },
            "suppress": True,
            "interval": {"unit": "days", "length": 1},
            "constituencies": ["Tenant1", "Tenant2"],
        },
    )

    # IP address directly from RIPE
    mocker.get(
        f"{PREFIX}&ip=123.123.123.123&feed_name=FTP",
        request_headers={"Authorization": "Bearer Lorem ipsum"},
        json={
            "ip": {
                "destinations": [
                    {
                        "source": "ripe",
                        "name": "Thurner",
                        "contacts": [{"email": "test@ntvtn.de"}],
                    }
                ]
            },
            "suppress": True,
            "constituencies": ["Tenant1", "Tenant2"],
        },
    )


@requests_mock.Mocker()
class TestTuencyExpertBot(BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = TuencyExpertBot
        if not os.environ.get("INTELMQ_TEST_TUNECY_URL") or not os.environ.get(
            "INTELMQ_TEST_TUNECY_TOKEN"
        ):
            cls.mock = True
            cls.sysconfig = {
                "url": "http://localhost/",
                "authentication_token": "Lorem ipsum",
            }
        else:
            cls.mock = False
            cls.sysconfig = {
                "url": os.environ["INTELMQ_TEST_TUNECY_URL"],
                "authentication_token": os.environ["INTELMQ_TEST_TUNECY_TOKEN"],
            }
        cls.default_input_message = INPUT

    def test_both(self, mocker):
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_BOTH)

    def test_ip(self, mocker):
        """
        Using an IP address as input. Existing source.abuse_contact should be overwritten.
        """
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.input_message = INPUT_IP
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_IP)

    def test_ip_no_overwrite(self, mocker):
        """
        Using an IP address as input. Existing source.abuse_contact should not be overwritten.
        """
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.input_message = INPUT_IP
        self.run_bot(parameters={"overwrite": False})
        self.assertMessageEqual(0, OUTPUT_IP_NO_OVERWRITE)

    def test_domain(self, mocker):
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.input_message = INPUT_DOMAIN
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_DOMAIN)

    def test_feed_code(self, mocker):
        """Using feed.code to identify feeds"""
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True

        self.input_message = INPUT_IP
        self.run_bot(parameters={"query_feed_code": True})
        expected = {
            **OUTPUT_IP,
            "source.abuse_contact": "test+code@ntvtn.de",
            "extra.ttl": 86400,
            "extra.notify": None,
        }
        del expected["extra.notify"]
        self.assertMessageEqual(
            0,
            expected,
        )

    def test_classification_identifier(self, mocker):
        """Using classification.identifier to filter events"""
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True

        self.input_message = INPUT_IP
        self.run_bot(parameters={"query_classification_identifier": True})
        self.assertMessageEqual(
            0,
            {
                **OUTPUT_IP,
                "source.abuse_contact": "test+identifier@ntvtn.de",
            },
        )

    def test_custom_fields(self, mocker):
        """Allow customize fields that bot sets"""
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True

        self.input_message = INPUT_IP
        self.run_bot(
            parameters={
                "notify_field": "extra.my_notify",
                "constituency_field": "extra.my_constituency",
                # Response for feed_code is not suspended - allows testing TTL
                # "query_feed_code": True,
            }
        )

        output = OUTPUT_IP.copy()
        output["extra.my_notify"] = output["extra.notify"]
        del output["extra.notify"]
        output["extra.my_constituency"] = output["extra.constituency"]
        del output["extra.constituency"]
        self.assertMessageEqual(0, output)

    def test_custom_fields_ttl(self, mocker):
        """Allow customize fields that bot sets"""
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True

        self.input_message = INPUT_IP
        self.run_bot(
            parameters={
                "ttl_field": "extra.my_ttl",
                # Response for feed_code is not suspended - allows testing TTL
                "query_feed_code": True,
            }
        )

        output = OUTPUT_IP.copy()
        del output["extra.notify"]
        output["extra.my_ttl"] = 86400
        output["source.abuse_contact"] = "test+code@ntvtn.de"
        self.assertMessageEqual(0, output)

    def test_ttl_on_suspended(self, mocker):
        """Allow setting custom TTL when Tuency decides on suspending sending"""
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True

        self.input_message = INPUT_IP
        self.run_bot(
            parameters={
                "ttl_on_suspended": -1,
            }
        )

        self.assertMessageEqual(
            0,
            {
                **OUTPUT_IP,
                "extra.ttl": -1,
            },
        )

    def test_empty(self, mocker):
        """
        A message with neither an IP address nor a domain, should be ignored and just passed on.
        """
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True

        self.input_message = EMPTY
        self.run_bot()
        self.assertMessageEqual(0, EMPTY)

        self.input_message = INPUT
        self.run_bot(
            parameters={"query_ip": False, "query_domain": False},
            allowed_warning_count=1,
        )
        self.assertMessageEqual(0, INPUT)

    def test_no_result(self, mocker):
        """
        This IP address is not in the database
        """
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.input_message = UNKNOWN_IP
        self.run_bot()
        self.assertMessageEqual(0, UNKNOWN_IP)

    def test_data_from_ripe(self, mocker):
        """
        Data sourced from ripe don't get interval
        """
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True

        input_msq = INPUT_IP.copy()
        input_msq["source.ip"] = "123.123.123.123"

        self.input_message = input_msq
        self.run_bot()

        output_msg = OUTPUT_IP.copy()
        output_msg["source.ip"] = "123.123.123.123"
        self.assertMessageEqual(0, output_msg)
