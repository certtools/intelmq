# -*- coding: utf-8 -*-
"""
Testing harmonization classes
"""
import ipaddress
import unittest

import intelmq.lib.harmonization as harmonization
import intelmq.lib.test as test


class TestHarmonization(unittest.TestCase):

    def test_boolean_valid_bool(self):
        """ Test Boolean.is_valid with bool values. """
        self.assertTrue(harmonization.Boolean.is_valid(True))
        self.assertTrue(harmonization.Boolean.is_valid(False))

    def test_boolean_valid_other(self):
        """ Test Boolean.is_valid with otehr invalid values. """
        self.assertFalse(harmonization.Boolean.is_valid(None,))
        self.assertFalse(harmonization.Boolean.is_valid('True'))
        self.assertFalse(harmonization.Boolean.is_valid(0))
        self.assertFalse(harmonization.Boolean.is_valid(1))
        self.assertFalse(harmonization.Boolean.is_valid([]))

    def test_boolean_sanitize_bool(self):
        """ Test Boolean.sanitize with bool values. """
        self.assertTrue(harmonization.Boolean.is_valid(True, sanitize=True))
        self.assertTrue(harmonization.Boolean.is_valid(False, sanitize=True))

    def test_boolean_sanitize_valid(self):
        """ Test Boolean.sanitize with valid string and int values. """
        self.assertTrue(harmonization.Boolean.is_valid(0, sanitize=True))
        self.assertTrue(harmonization.Boolean.is_valid(1, sanitize=True))
        self.assertTrue(harmonization.Boolean.is_valid('true', sanitize=True))
        self.assertTrue(harmonization.Boolean.is_valid('false', sanitize=True))

    def test_boolean_sanitize_invalid(self):
        """ Test Boolean.sanitize with invalid values. """
        self.assertFalse(harmonization.Boolean.is_valid(None, sanitize=True))
        self.assertFalse(harmonization.Boolean.is_valid([], sanitize=True))
        self.assertFalse(harmonization.Boolean.is_valid('test', sanitize=True))

    def test_integer_valid_int(self):
        """ Test Integer.is_valid with integer values. """
        self.assertTrue(harmonization.Integer.is_valid(-4532))
        self.assertTrue(harmonization.Integer.is_valid(1337))

    def test_integer_valid_other(self):
        """ Test Integer.is_valid with invalid values. """
        self.assertFalse(harmonization.Integer.is_valid('1337'))
        self.assertFalse(harmonization.Integer.is_valid(True))

    def test_integer_sanitize_int(self):
        """ Test Integer.sanitize with integer values. """
        self.assertTrue(harmonization.Integer.is_valid(-4532, sanitize=True))
        self.assertTrue(harmonization.Integer.is_valid(1337, sanitize=True))

    def test_integer_sanitize_other(self):
        """ Test Integer.sanitize with integer values. """
        self.assertTrue(harmonization.Integer.is_valid(True, sanitize=True))
        self.assertTrue(harmonization.Integer.is_valid('1337', sanitize=True))
        self.assertTrue(harmonization.Integer.is_valid(b'1337', sanitize=True))
        self.assertTrue(harmonization.Integer.is_valid(' 1337', sanitize=True))

    def test_integer_sanitize_invalid(self):
        """ Test Integer.sanitize with invalid values. """
        self.assertFalse(harmonization.Integer.is_valid(None, sanitize=True))
        self.assertFalse(harmonization.Integer.is_valid('b13', sanitize=True))

    def test_float_valid_flaot(self):
        """ Test Float.is_valid with flaot and integer values. """
        self.assertTrue(harmonization.Float.is_valid(-4532, sanitize=False))
        self.assertTrue(harmonization.Float.is_valid(1337, sanitize=False))
        self.assertTrue(harmonization.Float.is_valid(1337.2354,
                                                     sanitize=False))
        self.assertTrue(harmonization.Float.is_valid(13.234e-4,
                                                     sanitize=False))

    def test_float_valid_other(self):
        """ Test Float.is_valid with invalid values. """
        self.assertFalse(harmonization.Float.is_valid('1337.234',
                                                      sanitize=False))
        self.assertFalse(harmonization.Float.is_valid(True, sanitize=False))

    def test_float_sanitize_number(self):
        """ Test Float.sanitize with integer and float values. """
        self.assertTrue(harmonization.Float.is_valid(-4532.234, sanitize=True))
        self.assertTrue(harmonization.Float.is_valid(13.234e-4, sanitize=True))

    def test_float_sanitize_other(self):
        """ Test Float.sanitize with integer values. """
        self.assertTrue(harmonization.Float.is_valid(True, sanitize=True))
        self.assertTrue(harmonization.Float.is_valid('+137.23', sanitize=True))
        self.assertTrue(harmonization.Float.is_valid(b'17.234', sanitize=True))
        self.assertTrue(harmonization.Float.is_valid(' 1337.2', sanitize=True))
        self.assertTrue(harmonization.Float.is_valid('3.31e+3', sanitize=True))
        self.assertTrue(harmonization.Float.is_valid('-31.e-2', sanitize=True))

    def test_float_sanitize_invalid(self):
        """ Test Float.sanitize with invalid values. """
        self.assertFalse(harmonization.Float.is_valid(None, sanitize=True))
        self.assertFalse(harmonization.Float.is_valid('b13.23', sanitize=True))

    def test_ipaddress_valid(self):
        """ Test IPAddress.is_valid with valid arguments. """
        self.assertTrue(harmonization.IPAddress.is_valid('192.0.2.1',
                                                         sanitize=False))
        self.assertTrue(harmonization.IPAddress.is_valid('::1',
                                                         sanitize=False))
        self.assertTrue(harmonization.IPAddress.is_valid('2001:500:88:200::8',
                                                         sanitize=False))

    def test_ipaddress_valid_invalid(self):
        """ Test IPAddress.is_valid with invalid arguments. """
        self.assertFalse(harmonization.IPAddress.is_valid('192.0.2.1/24',
                                                          sanitize=False))
        self.assertFalse(harmonization.IPAddress.is_valid('2001:DB8::/32',
                                                          sanitize=False))
        self.assertFalse(harmonization.IPAddress.is_valid('localhost',
                                                          sanitize=False))

    def test_ipaddress_sanitize(self):
        """ Test IPAddress.is_valid and sanitize with valid arguments. """
        self.assertTrue(harmonization.IPAddress.sanitize(' 192.0.2.1\r\n'))
        self.assertTrue(harmonization.IPAddress.is_valid(' 192.0.2.1\r\n',
                                                         sanitize=True))
        self.assertTrue(harmonization.IPAddress.is_valid(b'2001:DB8::1',
                                                         sanitize=True))
        self.assertTrue(harmonization.IPAddress.is_valid(ipaddress.ip_address('192.0.2.1'),
                                                         sanitize=True))

    def test_ipaddress_sanitize_invalid(self):
        """ Test IPAddress.is_valid ans sanitize with invalid arguments. """
        self.assertFalse(harmonization.IPAddress.is_valid(' 192.0.2.0/24\r\n',
                                                          sanitize=True))
        self.assertFalse(harmonization.IPAddress.is_valid(b'2001:DB8::1/32',
                                                          sanitize=True))

    def test_ipnetwork_valid(self):
        """ Test IPNetwork.is_valid with valid arguments. """
        self.assertTrue(harmonization.IPNetwork.is_valid('192.0.2.1'))
        self.assertTrue(harmonization.IPNetwork.is_valid('::1'))
        self.assertTrue(harmonization.IPNetwork.is_valid('192.0.2.0/24'))
        self.assertTrue(harmonization.IPNetwork.is_valid('2001:DB8::/32'))
        self.assertTrue(harmonization.IPNetwork.is_valid('2001:500:88:200::8'))

    def test_ipnetwork_valid_invalid(self):
        """ Test IPNetwork.is_valid with invalid arguments. """
        self.assertFalse(harmonization.IPNetwork.is_valid('localhost'))
        self.assertFalse(harmonization.IPNetwork.is_valid('192.0.2.1/37'))
        self.assertFalse(harmonization.IPNetwork.is_valid('192.0.2.1/0'))
        self.assertFalse(harmonization.IPNetwork.is_valid('2001:DB8::/130'))

    def test_ipnetwork_sanitize(self):
        """ Test IPNetwork.is_valid and sanitize with valid arguments. """
        self.assertTrue(harmonization.IPNetwork.is_valid(' 192.0.2.0/24\r\n',
                                                         sanitize=True))
        self.assertTrue(harmonization.IPNetwork.is_valid(b'2001:DB8::/32',
                                                         sanitize=True))
        self.assertTrue(harmonization.IPNetwork.is_valid('127.0.0.1/32',
                                                         sanitize=True))
        self.assertTrue(harmonization.IPNetwork.is_valid(ipaddress.ip_network('192.0.2.0/32'),
                                                         sanitize=True))

    def test_ipnetwork_sanitize_invalid(self):
        """ Test IPNetwork.is_valid and sanitize with invalid arguments. """
        self.assertFalse(harmonization.IPNetwork.is_valid(' 192.0.2.0/-4\r\n',
                                                          sanitize=True))
        self.assertFalse(harmonization.IPNetwork.is_valid(b'2001:DB8Z::1/7',
                                                          sanitize=True))

    def test_datetime_valid(self):
        self.assertTrue(harmonization.DateTime.is_valid(
            '2015-08-31T08:16:10+00:00'))
        self.assertTrue(harmonization.DateTime.is_valid(
            '2015-08-31T08:16:10.1234+00:00'))

    def test_datetime_invalid(self):
        self.assertFalse(harmonization.DateTime.is_valid(
            '2015-08-31T08:16:10+05:00'))
        self.assertFalse(harmonization.DateTime.is_valid(
            '2015-08-31T08:16:10.1234+05:00'))
        self.assertFalse(harmonization.DateTime.is_valid(
            '2015-08-31T36:16:10+00:00'
        ))

    def test_datetime_from_epoch_millis(self):
        """ Test DateTime.from_epoch_millis method. """
        self.assertEqual('2015-08-31T08:16:10+00:00',
                         harmonization.DateTime.from_epoch_millis(1441008970))
        self.assertEqual('2015-08-31T08:16:10+00:00',
                         harmonization.DateTime.from_epoch_millis("1441008970"))
        self.assertEqual('2015-08-31T07:16:10-01:00',
                         harmonization.DateTime.from_epoch_millis(144100897000,
                                                                 'Etc/GMT+1'))
        self.assertEqual('2015-08-31T04:16:10-04:00',
                         harmonization.DateTime.from_epoch_millis(1441008970000,
                                                                     'America/'
                                                                     'Guyana'))

    def test_datetime_from_timestamp(self):
        """ Test DateTime.from_timestamp method. """
        self.assertEqual('2015-08-31T08:16:10+00:00',
                         harmonization.DateTime.from_timestamp(1441008970))
        self.assertEqual('2015-08-31T07:16:10-01:00',
                         harmonization.DateTime.from_timestamp(1441008970,
                                                               'Etc/GMT+1'))
        self.assertEqual('2015-08-31T04:16:10-04:00',
                         harmonization.DateTime.from_timestamp(1441008970,
                                                               'America/'
                                                               'Guyana'))

    def test_datetime_from_windows_nt(self):
        """ Test DateTime.from_ldap method. """
        self.assertEqual('2011-02-01T02:43:11.572760+00:00',
                         harmonization.DateTime.from_windows_nt(129410017915727600))

    def test_datetime_sanitize(self):
        """ Test DateTime.sanitize method. """
        self.assertEqual('2016-07-19T04:40:01.617719+00:00',
                         harmonization.DateTime.sanitize(
                         '2016-07-19 06:40:01.617719+02:00 UTC'))
        self.assertEqual('2016-07-19T13:08:38+00:00',
                         harmonization.DateTime.sanitize(
                         '2016-07-19 13:08:38 UTC'))

    def test_datetime_from_timestamp_invalid(self):
        """ Test DateTime.from_timestamp method with invalid inputs. """
        with self.assertRaises(TypeError):
            harmonization.DateTime.from_timestamp('1441008970')

    def test_fqdn_valid(self):
        """ Test FQDN.is_valid with valid arguments. """
        self.assertTrue(harmonization.FQDN.is_valid('ex-am.ple.example'))
        self.assertTrue(harmonization.FQDN.is_valid('example.org'))
        self.assertTrue(harmonization.FQDN.is_valid('sub_sub2.example.net'))
        self.assertTrue(harmonization.FQDN.is_valid('xn--1-0ga.at'))
        self.assertTrue(harmonization.FQDN.is_valid('212.156.101.43.00-ebgp-atakoy1-k.301-fra-'
                                                    'col-1.statik.turktelekom.com.tr'))

    def test_fqdn_invalid(self):
        """ Test FQDN.is_valid with invalid arguments. """
        self.assertFalse(harmonization.FQDN.is_valid('ex-am.ple.example.'))
        self.assertFalse(harmonization.FQDN.is_valid('exAmple.com'))
        self.assertFalse(harmonization.FQDN.is_valid('ö1.at'))
        self.assertFalse(harmonization.FQDN.is_valid('n/a'))
        self.assertFalse(harmonization.FQDN.is_valid('.'))
        self.assertFalse(harmonization.FQDN.is_valid('.example.com'))
        self.assertFalse(harmonization.FQDN.is_valid('10.0.0.1:8080'))  # 1235

    def test_fqdn_sanitize(self):
        """ Test FQDN.sanitize with valid arguments. """
        self.assertTrue(harmonization.FQDN.is_valid('example.example.',
                                                    sanitize=True))
        self.assertTrue(harmonization.FQDN.is_valid('example.net',
                                                    sanitize=True))
        self.assertTrue(harmonization.FQDN.is_valid('exAmple.net',
                                                    sanitize=True))
        self.assertTrue(harmonization.FQDN.is_valid('ö1.at', sanitize=True))
        self.assertTrue(harmonization.FQDN.is_valid('212.156.101.43.00-ebgp-atakoy1-k.301-fra-'
                                                    'col-1.statik.turktelekom.com.tr',
                                                    sanitize=True))
        self.assertTrue(harmonization.FQDN.is_valid('.example.com',
                                                    sanitize=True))

    def test_fqdn_sanitize_unicodeerror(self):
        """
        Check if FQDN.sanitize does not raise a UnicodeError.
        """
        data = "{subid_3}&aff_sub4={subid_4}&aff_sub5={subid_5}&DOM=trackingmyli"
        self.assertIsNone(harmonization.FQDN.sanitize(data))

    def test_fqdn_sanitize_invalid(self):
        """Test FQDN.sanitize with invalid arguments. """
        self.assertFalse(harmonization.FQDN.is_valid('.', sanitize=False))
        self.assertFalse(harmonization.FQDN.is_valid('...', sanitize=False))
        self.assertFalse(harmonization.FQDN.is_valid('', sanitize=False))

    @test.skip_internet()
    def test_fqdn_to_ip(self):
        """ Test FQDN.to_ip """
        self.assertEqual(None, harmonization.FQDN.to_ip('localhost'))
        self.assertEqual('93.184.216.34',
                         harmonization.FQDN.to_ip('example.org'))

    def test_json_valid(self):
        """ Test JSON.is_valid with valid arguments. """
        self.assertTrue(harmonization.JSON.is_valid('{"foo": "bar"}',
                                                    sanitize=False))
        self.assertTrue(harmonization.JSON.is_valid('"foo"',
                                                    sanitize=False))

    def test_json_invalid(self):
        """ Test JSON.is_valid with invalid arguments. """
        self.assertFalse(harmonization.JSON.is_valid('{'))
        self.assertFalse(harmonization.JSON.is_valid('["foo", ]'))
        self.assertFalse(harmonization.JSON.is_valid(b'{"foo": 1}',
                                                     sanitize=False))
        self.assertFalse(harmonization.JSON.is_valid({"foo": "bar"},
                                                     sanitize=False))

    def test_json_sanitize(self):
        """ Test JSON.sanitize with valid arguments. """
        self.assertTrue(harmonization.JSON.is_valid({"foo": "bar"},
                                                    sanitize=True))
        self.assertTrue(harmonization.JSON.is_valid('{"foo": "bar"}',
                                                    sanitize=True))
        self.assertTrue(harmonization.JSON.is_valid(b'{"foo": "bar"}',
                                                    sanitize=True))

    def test_jsondict_valid(self):
        """ Test JSONDict.is_valid with valid arguments. """
        self.assertTrue(harmonization.JSONDict.is_valid('{"foo": "bar"}',
                                                        sanitize=False))

    def test_jsondict_invalid(self):
        """ Test JSONDict.is_valid with invalid arguments. """
        self.assertFalse(harmonization.JSONDict.is_valid('{}'))
        self.assertFalse(harmonization.JSONDict.is_valid('"example"'))
        self.assertFalse(harmonization.JSONDict.is_valid(b'{"foo": 1}',
                                                         sanitize=False))
        self.assertFalse(harmonization.JSONDict.is_valid({"foo": "bar"},
                                                         sanitize=False))

    def test_jsondict_sanitize(self):
        """ Test JSONDict.sanitize with valid arguments. """
        self.assertTrue(harmonization.JSONDict.is_valid({"foo": "bar"},
                                                        sanitize=True))
        self.assertTrue(harmonization.JSONDict.is_valid('{"foo": "bar"}',
                                                        sanitize=True))
        self.assertTrue(harmonization.JSONDict.is_valid(b'{"foo": "bar"}',
                                                        sanitize=True))

    def test_lowercasestring_valid(self):
        """ Test LowercaseString.is_valid with valid arguments. """
        self.assertTrue(harmonization.LowercaseString.is_valid('foobar'))

    def test_lowercasestring_invalid(self):
        """ Test LowercaseString.is_valid with invalid arguments. """
        self.assertFalse(harmonization.LowercaseString.is_valid('fooBar'))

    def test_lowercasestring_sanitize(self):
        """ Test LowercaseString.sanitize with valid arguments. """
        self.assertTrue(harmonization.LowercaseString.is_valid(b'fooBar',
                                                               sanitize=True))

    def test_registry_valid(self):
        """ Test Registry.is_valid with valid arguments. """
        self.assertTrue(harmonization.Registry.is_valid('RIPE'))
        self.assertTrue(harmonization.Registry.is_valid('lacnic', sanitize=True))
        self.assertTrue(harmonization.Registry.is_valid('RIPE-NCC', sanitize=True))
        self.assertTrue(harmonization.Registry.is_valid('RIPENCC', sanitize=True))

    def test_registry_invalid(self):
        """ Test Registry.is_valid with invalid arguments. """
        self.assertFalse(harmonization.Registry.is_valid('RIPE-NCC', sanitize=False))
        self.assertFalse(harmonization.Registry.is_valid('RIPENCC', sanitize=False))

    def test_registry_sanitize(self):
        """ Test Registry.sanitize with valid arguments. """
        self.assertEqual(harmonization.Registry.sanitize('ripe-ncc'), 'RIPE')

    def test_uppercasestring_valid(self):
        """ Test UppercaseString.is_valid with valid arguments. """
        self.assertTrue(harmonization.UppercaseString.is_valid('FOOBAR'))

    def test_uppercasestring_invalid(self):
        """ Test UppercaseString.is_valid with invalid arguments. """
        self.assertFalse(harmonization.UppercaseString.is_valid('fooBar'))

    def test_uppercasestring_sanitize(self):
        """ Test UppercaseString.sanitize with valid arguments. """
        self.assertTrue(harmonization.UppercaseString.is_valid(b'fooBar',
                                                               sanitize=True))

    def test_url_valid(self):
        """ Test URL.is_valid with valid arguments. """
        self.assertTrue(harmonization.URL.is_valid('http://example.com'))
        self.assertTrue(harmonization.URL.is_valid('http://example.com/foo'))
        self.assertTrue(harmonization.URL.is_valid('file://localhost/etc/hosts'))

    def test_url_invalid(self):
        """ Test URL.is_valid with invalid arguments. """
        self.assertFalse(harmonization.URL.is_valid('example.com'))
        self.assertFalse(harmonization.URL.is_valid(' http://example.com'))
        self.assertFalse(harmonization.URL.is_valid('file:///etc/hosts'))

    def test_url_sanitize(self):
        """ Test URL.sanitize with valid arguments. """
        self.assertTrue(harmonization.URL.is_valid(b'http://example.com',
                                                   sanitize=True))
        self.assertTrue(harmonization.URL.is_valid('hxxps://example.com/foo',
                                                   sanitize=True))
        self.assertTrue(harmonization.URL.is_valid('file:///etc/hosts',
                                                   sanitize=True))
        self.assertTrue(harmonization.URL.is_valid(' http://example.com',
                                                   sanitize=True))
        self.assertEqual(harmonization.URL.sanitize(' http://example.com'),
                         'http://example.com')

    def test_url_sanitize_invalid(self):
        """ Test URL.is_valid with valid arguments. """
        self.assertFalse(harmonization.URL.is_valid('example.com',
                                                    sanitize=True))
        self.assertFalse(harmonization.URL.is_valid('http://',
                                                    sanitize=True))

    def test_asn_valid(self):
        """ Test ASN.is_valid with valid arguments. """
        self.assertTrue(harmonization.ASN.is_valid(123))
        self.assertTrue(harmonization.ASN.is_valid(1234567))

    def test_asn_invalid(self):
        """ Test ASN.is_valid with invalid arguments. """
        self.assertFalse(harmonization.ASN.is_valid(4294967296))
        self.assertFalse(harmonization.ASN.is_valid(0))
        self.assertFalse(harmonization.ASN.is_valid('foo'))
        self.assertFalse(harmonization.ASN.is_valid('1234'))

    def test_asn_sanitize(self):
        """ Test ASN.sanitize with valid arguments. """
        self.assertTrue(harmonization.ASN.is_valid('1234',
                                                   sanitize=True))
        self.assertTrue(harmonization.ASN.is_valid('AS1234',
                                                   sanitize=True))

    def test_asn_sanitize_invalid(self):
        """ Test ASN.is_valid with invalid arguments. """
        self.assertFalse(harmonization.ASN.is_valid(0, sanitize=True))
        self.assertFalse(harmonization.ASN.is_valid('asd', sanitize=True))
        self.assertFalse(harmonization.ASN.is_valid(-1, sanitize=True))
        self.assertFalse(harmonization.ASN.is_valid(4294967296, sanitize=True))

    def test_tlp_valid(self):
        """ Test TLP.is_valid with valid arguments. """
        self.assertTrue(harmonization.TLP.is_valid('WHITE'))

    def test_tlp_invalid(self):
        """ Test TLP.is_valid with invalid arguments. """
        self.assertFalse(harmonization.TLP.is_valid('green'))

    def test_tlp_sanitize(self):
        """ Test TLP.sanitize with valid arguments. """
        self.assertTrue(harmonization.TLP.is_valid('TLP:RED',
                                                   sanitize=True))
        self.assertTrue(harmonization.TLP.is_valid('red ',
                                                   sanitize=True))

    def test_tlp_sanitize_invalid(self):
        """ Test TLP.is_valid with invalid arguments. """
        self.assertFalse(harmonization.TLP.is_valid('TLP AMBER'))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
