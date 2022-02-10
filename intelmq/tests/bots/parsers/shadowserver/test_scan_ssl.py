# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_ssl.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible SSL',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-scan_ssl-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'open-ssl',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.browser_error' : 'x509: unknown error',
   'extra.browser_trusted' : 'N',
   'extra.cert_expiration_date' : '2038-01-19 03:14:07',
   'extra.cert_expired' : False,
   'extra.cert_issue_date' : '2014-06-23 09:56:32',
   'extra.cert_length' : 1024,
   'extra.cert_serial_number' : '168CAE',
   'extra.cert_valid' : True,
   'extra.cipher_suite' : 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
   'extra.content_length' : 131,
   'extra.content_type' : 'text/html',
   'extra.freak_vulnerable' : 'N',
   'extra.handshake' : 'TLSv1.2',
   'extra.http_code' : 200,
   'extra.http_date' : '2022-01-10T00:01:44+00:00',
   'extra.http_reason' : 'OK',
   'extra.http_response_type' : 'HTTP/1.1',
   'extra.issuer_common_name' : 'support',
   'extra.issuer_country' : 'US',
   'extra.issuer_email_address' : 'support@fortinet.com',
   'extra.issuer_locality_name' : 'Sunnyvale',
   'extra.issuer_organization_name' : 'Fortinet',
   'extra.issuer_organization_unit_name' : 'Certificate Authority',
   'extra.issuer_state_or_province_name' : 'California',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : '99:45:1F:2E:AE:EB:88:91:27:43:33:79:FA:93:7D:CA',
   'extra.self_signed' : False,
   'extra.server_type' : 'xxxxxxxx-xxxxx',
   'extra.sha1_fingerprint' : '5A:3D:FF:06:F9:E9:25:37:57:F9:09:52:33:A4:85:15:24:2D:88:7F',
   'extra.sha256_fingerprint' : '35:AB:B6:76:2A:3D:17:B2:FB:40:45:1B:FC:0A:99:0A:6E:48:57:F7:30:0A:3B:B1:1A:E6:99:70:5B:7C:32:41',
   'extra.sha512_fingerprint' : '88:7B:16:DB:39:44:0C:47:0E:4A:8F:0B:C5:FB:4D:45:BC:93:5A:00:43:A1:D9:7F:05:1D:86:33:02:F8:FC:57:67:A6:1D:C0:FF:F7:D2:40:D8:9A:21:AE:4E:6D:DC:E7:FF:72:BF:13:CB:EE:A7:5F:CD:83:EA:8A:5E:FB:87:DD',
   'extra.signature_algorithm' : 'sha1WithRSAEncryption',
   'extra.source.naics' : 517311,
   'extra.ssl_poodle' : 'N',
   'extra.ssl_version' : 2,
   'extra.subject_common_name' : 'FGT60D4614030700',
   'extra.subject_country' : 'US',
   'extra.subject_email_address' : 'support@fortinet.com',
   'extra.subject_locality_name' : 'Sunnyvale',
   'extra.subject_organization_name' : 'Fortinet',
   'extra.subject_organization_unit_name' : 'FortiGate',
   'extra.subject_state_or_province_name' : 'California',
   'extra.tag' : 'ssl,vpn',
   'feed.name' : 'Accessible SSL',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicG9ydCIsImhvc3RuYW1lIiwidGFnIiwiaGFuZHNoYWtlIiwiYXNuIiwiZ2VvIiwicmVnaW9uIiwiY2l0eSIsImNpcGhlcl9zdWl0ZSIsInNzbF9wb29kbGUiLCJjZXJ0X2xlbmd0aCIsInN1YmplY3RfY29tbW9uX25hbWUiLCJpc3N1ZXJfY29tbW9uX25hbWUiLCJjZXJ0X2lzc3VlX2RhdGUiLCJjZXJ0X2V4cGlyYXRpb25fZGF0ZSIsInNoYTFfZmluZ2VycHJpbnQiLCJjZXJ0X3NlcmlhbF9udW1iZXIiLCJzc2xfdmVyc2lvbiIsInNpZ25hdHVyZV9hbGdvcml0aG0iLCJrZXlfYWxnb3JpdGhtIiwic3ViamVjdF9vcmdhbml6YXRpb25fbmFtZSIsInN1YmplY3Rfb3JnYW5pemF0aW9uX3VuaXRfbmFtZSIsInN1YmplY3RfY291bnRyeSIsInN1YmplY3Rfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsInN1YmplY3RfbG9jYWxpdHlfbmFtZSIsInN1YmplY3Rfc3RyZWV0X2FkZHJlc3MiLCJzdWJqZWN0X3Bvc3RhbF9jb2RlIiwic3ViamVjdF9zdXJuYW1lIiwic3ViamVjdF9naXZlbl9uYW1lIiwic3ViamVjdF9lbWFpbF9hZGRyZXNzIiwic3ViamVjdF9idXNpbmVzc19jYXRlZ29yeSIsInN1YmplY3Rfc2VyaWFsX251bWJlciIsImlzc3Vlcl9vcmdhbml6YXRpb25fbmFtZSIsImlzc3Vlcl9vcmdhbml6YXRpb25fdW5pdF9uYW1lIiwiaXNzdWVyX2NvdW50cnkiLCJpc3N1ZXJfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsImlzc3Vlcl9sb2NhbGl0eV9uYW1lIiwiaXNzdWVyX3N0cmVldF9hZGRyZXNzIiwiaXNzdWVyX3Bvc3RhbF9jb2RlIiwiaXNzdWVyX3N1cm5hbWUiLCJpc3N1ZXJfZ2l2ZW5fbmFtZSIsImlzc3Vlcl9lbWFpbF9hZGRyZXNzIiwiaXNzdWVyX2J1c2luZXNzX2NhdGVnb3J5IiwiaXNzdWVyX3NlcmlhbF9udW1iZXIiLCJuYWljcyIsInNpYyIsImZyZWFrX3Z1bG5lcmFibGUiLCJmcmVha19jaXBoZXJfc3VpdGUiLCJzZWN0b3IiLCJzaGEyNTZfZmluZ2VycHJpbnQiLCJzaGE1MTJfZmluZ2VycHJpbnQiLCJtZDVfZmluZ2VycHJpbnQiLCJodHRwX3Jlc3BvbnNlX3R5cGUiLCJodHRwX2NvZGUiLCJodHRwX3JlYXNvbiIsImNvbnRlbnRfdHlwZSIsImh0dHBfY29ubmVjdGlvbiIsInd3d19hdXRoZW50aWNhdGUiLCJzZXRfY29va2llIiwic2VydmVyX3R5cGUiLCJjb250ZW50X2xlbmd0aCIsInRyYW5zZmVyX2VuY29kaW5nIiwiaHR0cF9kYXRlIiwiY2VydF92YWxpZCIsInNlbGZfc2lnbmVkIiwiY2VydF9leHBpcmVkIiwiYnJvd3Nlcl90cnVzdGVkIiwidmFsaWRhdGlvbl9sZXZlbCIsImJyb3dzZXJfZXJyb3IiLCJ0bHN2MTNfc3VwcG9ydCIsInRsc3YxM19jaXBoZXIiLCJqYXJtIgoiMjAyMi0wMS0xMCAwMDowMTo0MiIsIjk2LjYwLjAuMCIsMTA0NDMsIjk2LTYwLTAtMC5leGFtcGxlLmNvbSIsInNzbCx2cG4iLCJUTFN2MS4yIiw0MTgxLCJVUyIsIldJU0NPTlNJTiIsIk1JTFdBVUtFRSIsIlRMU19FQ0RIRV9SU0FfV0lUSF9BRVNfMjU2X0NCQ19TSEEiLCJOIiwxMDI0LCJGR1Q2MEQ0NjE0MDMwNzAwIiwic3VwcG9ydCIsIjIwMTQtMDYtMjMgMDk6NTY6MzIiLCIyMDM4LTAxLTE5IDAzOjE0OjA3IiwiNUE6M0Q6RkY6MDY6Rjk6RTk6MjU6Mzc6NTc6Rjk6MDk6NTI6MzM6QTQ6ODU6MTU6MjQ6MkQ6ODg6N0YiLCIxNjhDQUUiLDIsInNoYTFXaXRoUlNBRW5jcnlwdGlvbiIsInJzYUVuY3J5cHRpb24iLCJGb3J0aW5ldCIsIkZvcnRpR2F0ZSIsIlVTIiwiQ2FsaWZvcm5pYSIsIlN1bm55dmFsZSIsLCwsLCJzdXBwb3J0QGZvcnRpbmV0LmNvbSIsLCwiRm9ydGluZXQiLCJDZXJ0aWZpY2F0ZSBBdXRob3JpdHkiLCJVUyIsIkNhbGlmb3JuaWEiLCJTdW5ueXZhbGUiLCwsLCwic3VwcG9ydEBmb3J0aW5ldC5jb20iLCwsNTE3MzExLCwiTiIsLCwiMzU6QUI6QjY6NzY6MkE6M0Q6MTc6QjI6RkI6NDA6NDU6MUI6RkM6MEE6OTk6MEE6NkU6NDg6NTc6Rjc6MzA6MEE6M0I6QjE6MUE6RTY6OTk6NzA6NUI6N0M6MzI6NDEiLCI4ODo3QjoxNjpEQjozOTo0NDowQzo0NzowRTo0QTo4RjowQjpDNTpGQjo0RDo0NTpCQzo5Mzo1QTowMDo0MzpBMTpEOTo3RjowNToxRDo4NjozMzowMjpGODpGQzo1Nzo2NzpBNjoxRDpDMDpGRjpGNzpEMjo0MDpEODo5QToyMTpBRTo0RTo2RDpEQzpFNzpGRjo3MjpCRjoxMzpDQjpFRTpBNzo1RjpDRDo4MzpFQTo4QTo1RTpGQjo4NzpERCIsIjk5OjQ1OjFGOjJFOkFFOkVCOjg4OjkxOjI3OjQzOjMzOjc5OkZBOjkzOjdEOkNBIiwiSFRUUC8xLjEiLDIwMCwiT0siLCJ0ZXh0L2h0bWwiLCwsLCJ4eHh4eHh4eC14eHh4eCIsMTMxLCwiTW9uLCAxMCBKYW4gMjAyMiAwMDowMTo0NCBHTVQiLCJZIiwiTiIsIk4iLCJOIiwidW5rbm93biIsIng1MDk6IHVua25vd24gZXJyb3IiLCws',
   'source.asn' : 4181,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'MILWAUKEE',
   'source.geolocation.region' : 'WISCONSIN',
   'source.ip' : '96.60.0.0',
   'source.port' : 10443,
   'source.reverse_dns' : '96-60-0-0.example.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:01:42+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-ssl',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.browser_error' : 'x509: unknown error',
   'extra.browser_trusted' : 'N',
   'extra.cert_expiration_date' : '2023-02-06 01:01:34',
   'extra.cert_expired' : False,
   'extra.cert_issue_date' : '2022-01-04 01:01:34',
   'extra.cert_length' : 2048,
   'extra.cert_serial_number' : '36974C4C6B1B3785',
   'extra.cert_valid' : False,
   'extra.cipher_suite' : 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
   'extra.content_type' : 'text/html; charset=UTF-8',
   'extra.freak_vulnerable' : 'N',
   'extra.handshake' : 'TLSv1.2',
   'extra.http_code' : 200,
   'extra.http_connection' : 'keep-alive',
   'extra.http_date' : '2022-01-10T00:01:44+00:00',
   'extra.http_reason' : 'OK',
   'extra.http_response_type' : 'HTTP/1.1',
   'extra.issuer_common_name' : '1078-btb-tbi-HungHa-61d39c6d5a7e2',
   'extra.issuer_organization_name' : 'pfSense webConfigurator Self-Signed Certificate',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : '16:93:9A:F4:35:7F:9A:85:45:71:91:C7:7C:80:88:00',
   'extra.self_signed' : True,
   'extra.server_type' : 'nginx',
   'extra.set_cookie' : 'PHPSESSID=e15bdfa5739c36877608eb4cf46cc388; path=/; secure; HttpO',
   'extra.sha1_fingerprint' : 'A9:00:BB:E1:54:4D:56:54:59:F1:B7:EA:F1:1A:D5:36:5C:63:90:8E',
   'extra.sha256_fingerprint' : '38:85:F0:44:1E:AD:84:B8:2F:43:68:BA:AC:EE:17:13:A4:BF:86:1D:48:75:7E:22:FA:08:4C:28:5F:AC:3E:5F',
   'extra.sha512_fingerprint' : 'AE:1B:4F:D1:E4:C0:35:9D:2A:4F:7A:37:B8:7B:11:9D:84:25:23:21:AB:EF:B2:0F:DC:C9:F2:A3:72:28:92:E1:74:72:FA:E1:09:6C:E1:F6:B6:E3:A7:61:1C:58:89:34:D7:06:5C:3D:0A:A7:F6:CC:8A:D6:24:D0:04:4C:03:02',
   'extra.signature_algorithm' : 'sha256WithRSAEncryption',
   'extra.source.naics' : 517311,
   'extra.ssl_poodle' : 'N',
   'extra.ssl_version' : 2,
   'extra.subject_common_name' : '1078-btb-tbi-HungHa-61d39c6d5a7e2',
   'extra.subject_organization_name' : 'pfSense webConfigurator Self-Signed Certificate',
   'extra.tag' : 'ssl',
   'extra.transfer_encoding' : 'chunked',
   'feed.name' : 'Accessible SSL',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicG9ydCIsImhvc3RuYW1lIiwidGFnIiwiaGFuZHNoYWtlIiwiYXNuIiwiZ2VvIiwicmVnaW9uIiwiY2l0eSIsImNpcGhlcl9zdWl0ZSIsInNzbF9wb29kbGUiLCJjZXJ0X2xlbmd0aCIsInN1YmplY3RfY29tbW9uX25hbWUiLCJpc3N1ZXJfY29tbW9uX25hbWUiLCJjZXJ0X2lzc3VlX2RhdGUiLCJjZXJ0X2V4cGlyYXRpb25fZGF0ZSIsInNoYTFfZmluZ2VycHJpbnQiLCJjZXJ0X3NlcmlhbF9udW1iZXIiLCJzc2xfdmVyc2lvbiIsInNpZ25hdHVyZV9hbGdvcml0aG0iLCJrZXlfYWxnb3JpdGhtIiwic3ViamVjdF9vcmdhbml6YXRpb25fbmFtZSIsInN1YmplY3Rfb3JnYW5pemF0aW9uX3VuaXRfbmFtZSIsInN1YmplY3RfY291bnRyeSIsInN1YmplY3Rfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsInN1YmplY3RfbG9jYWxpdHlfbmFtZSIsInN1YmplY3Rfc3RyZWV0X2FkZHJlc3MiLCJzdWJqZWN0X3Bvc3RhbF9jb2RlIiwic3ViamVjdF9zdXJuYW1lIiwic3ViamVjdF9naXZlbl9uYW1lIiwic3ViamVjdF9lbWFpbF9hZGRyZXNzIiwic3ViamVjdF9idXNpbmVzc19jYXRlZ29yeSIsInN1YmplY3Rfc2VyaWFsX251bWJlciIsImlzc3Vlcl9vcmdhbml6YXRpb25fbmFtZSIsImlzc3Vlcl9vcmdhbml6YXRpb25fdW5pdF9uYW1lIiwiaXNzdWVyX2NvdW50cnkiLCJpc3N1ZXJfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsImlzc3Vlcl9sb2NhbGl0eV9uYW1lIiwiaXNzdWVyX3N0cmVldF9hZGRyZXNzIiwiaXNzdWVyX3Bvc3RhbF9jb2RlIiwiaXNzdWVyX3N1cm5hbWUiLCJpc3N1ZXJfZ2l2ZW5fbmFtZSIsImlzc3Vlcl9lbWFpbF9hZGRyZXNzIiwiaXNzdWVyX2J1c2luZXNzX2NhdGVnb3J5IiwiaXNzdWVyX3NlcmlhbF9udW1iZXIiLCJuYWljcyIsInNpYyIsImZyZWFrX3Z1bG5lcmFibGUiLCJmcmVha19jaXBoZXJfc3VpdGUiLCJzZWN0b3IiLCJzaGEyNTZfZmluZ2VycHJpbnQiLCJzaGE1MTJfZmluZ2VycHJpbnQiLCJtZDVfZmluZ2VycHJpbnQiLCJodHRwX3Jlc3BvbnNlX3R5cGUiLCJodHRwX2NvZGUiLCJodHRwX3JlYXNvbiIsImNvbnRlbnRfdHlwZSIsImh0dHBfY29ubmVjdGlvbiIsInd3d19hdXRoZW50aWNhdGUiLCJzZXRfY29va2llIiwic2VydmVyX3R5cGUiLCJjb250ZW50X2xlbmd0aCIsInRyYW5zZmVyX2VuY29kaW5nIiwiaHR0cF9kYXRlIiwiY2VydF92YWxpZCIsInNlbGZfc2lnbmVkIiwiY2VydF9leHBpcmVkIiwiYnJvd3Nlcl90cnVzdGVkIiwidmFsaWRhdGlvbl9sZXZlbCIsImJyb3dzZXJfZXJyb3IiLCJ0bHN2MTNfc3VwcG9ydCIsInRsc3YxM19jaXBoZXIiLCJqYXJtIgoiMjAyMi0wMS0xMCAwMDowMTo0MiIsIjExMy4xNjAuMC4wIiwxMDQ0MywiIiwic3NsIiwiVExTdjEuMiIsNDU4OTksIlZOIiwiVEhBSSBCSU5IIiwiVEhBSSBCSU5IIiwiVExTX0VDREhFX1JTQV9XSVRIX0FFU18xMjhfR0NNX1NIQTI1NiIsIk4iLDIwNDgsIjEwNzgtYnRiLXRiaS1IdW5nSGEtNjFkMzljNmQ1YTdlMiIsIjEwNzgtYnRiLXRiaS1IdW5nSGEtNjFkMzljNmQ1YTdlMiIsIjIwMjItMDEtMDQgMDE6MDE6MzQiLCIyMDIzLTAyLTA2IDAxOjAxOjM0IiwiQTk6MDA6QkI6RTE6NTQ6NEQ6NTY6NTQ6NTk6RjE6Qjc6RUE6RjE6MUE6RDU6MzY6NUM6NjM6OTA6OEUiLCIzNjk3NEM0QzZCMUIzNzg1IiwyLCJzaGEyNTZXaXRoUlNBRW5jcnlwdGlvbiIsInJzYUVuY3J5cHRpb24iLCJwZlNlbnNlIHdlYkNvbmZpZ3VyYXRvciBTZWxmLVNpZ25lZCBDZXJ0aWZpY2F0ZSIsLCwsLCwsLCwsLCwicGZTZW5zZSB3ZWJDb25maWd1cmF0b3IgU2VsZi1TaWduZWQgQ2VydGlmaWNhdGUiLCwsLCwsLCwsLCwsNTE3MzExLCwiTiIsLCwiMzg6ODU6RjA6NDQ6MUU6QUQ6ODQ6Qjg6MkY6NDM6Njg6QkE6QUM6RUU6MTc6MTM6QTQ6QkY6ODY6MUQ6NDg6NzU6N0U6MjI6RkE6MDg6NEM6Mjg6NUY6QUM6M0U6NUYiLCJBRToxQjo0RjpEMTpFNDpDMDozNTo5RDoyQTo0Rjo3QTozNzpCODo3QjoxMTo5RDo4NDoyNToyMzoyMTpBQjpFRjpCMjowRjpEQzpDOTpGMjpBMzo3MjoyODo5MjpFMTo3NDo3MjpGQTpFMTowOTo2QzpFMTpGNjpCNjpFMzpBNzo2MToxQzo1ODo4OTozNDpENzowNjo1QzozRDowQTpBNzpGNjpDQzo4QTpENjoyNDpEMDowNDo0QzowMzowMiIsIjE2OjkzOjlBOkY0OjM1OjdGOjlBOjg1OjQ1OjcxOjkxOkM3OjdDOjgwOjg4OjAwIiwiSFRUUC8xLjEiLDIwMCwiT0siLCJ0ZXh0L2h0bWw7IGNoYXJzZXQ9VVRGLTgiLCJrZWVwLWFsaXZlIiwsIlBIUFNFU1NJRD1lMTViZGZhNTczOWMzNjg3NzYwOGViNGNmNDZjYzM4ODsgcGF0aD0vOyBzZWN1cmU7IEh0dHBPIiwibmdpbngiLCwiY2h1bmtlZCIsIk1vbiwgMTAgSmFuIDIwMjIgMDA6MDE6NDQgR01UIiwiTiIsIlkiLCJOIiwiTiIsInVua25vd24iLCJ4NTA5OiB1bmtub3duIGVycm9yIiwsLA==',
   'source.asn' : 45899,
   'source.geolocation.cc' : 'VN',
   'source.geolocation.city' : 'THAI BINH',
   'source.geolocation.region' : 'THAI BINH',
   'source.ip' : '113.160.0.0',
   'source.port' : 10443,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:01:42+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-ssl',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.browser_trusted' : 'Y',
   'extra.cert_expiration_date' : '2022-11-06 15:30:28',
   'extra.cert_expired' : False,
   'extra.cert_issue_date' : '2021-10-07 15:30:28',
   'extra.cert_length' : 2048,
   'extra.cert_serial_number' : '7B388364A24B88E77E5553B5C6748100',
   'extra.cert_valid' : True,
   'extra.cipher_suite' : 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
   'extra.content_length' : 131,
   'extra.content_type' : 'text/html',
   'extra.freak_vulnerable' : 'N',
   'extra.handshake' : 'TLSv1.2',
   'extra.http_code' : 200,
   'extra.http_date' : '2022-01-10T00:01:44+00:00',
   'extra.http_reason' : 'OK',
   'extra.http_response_type' : 'HTTP/1.1',
   'extra.issuer_common_name' : 'Entrust Certification Authority - L1K',
   'extra.issuer_country' : 'US',
   'extra.issuer_organization_name' : 'Entrust, Inc.',
   'extra.issuer_organization_unit_name' : '(c) 2012 Entrust, Inc. - for authorized use only',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : 'E7:34:BC:92:84:FA:39:DE:E1:46:6C:27:DA:5A:01:F4',
   'extra.self_signed' : False,
   'extra.server_type' : 'xxxxxxxx-xxxxx',
   'extra.sha1_fingerprint' : 'AD:19:B2:1C:CB:88:70:9B:DB:8E:7E:F5:65:50:13:D6:43:6C:BE:6E',
   'extra.sha256_fingerprint' : '9A:64:73:0B:8A:FA:DE:22:D4:6D:5A:C6:C4:6F:D4:A4:2A:28:FA:41:1E:FF:81:DC:D4:D9:00:FD:78:DF:C4:DD',
   'extra.sha512_fingerprint' : '9A:B7:BD:68:7D:F3:E7:C1:B7:D3:F4:2F:01:B6:C4:77:90:A3:2B:1E:C0:89:F5:08:EC:43:87:35:60:36:D4:87:61:AA:B8:A8:B3:8A:E9:F1:04:AA:5B:67:12:FF:63:D5:14:80:77:6E:8F:7D:C3:E2:3A:F3:13:DF:08:43:6C:B0',
   'extra.signature_algorithm' : 'sha256WithRSAEncryption',
   'extra.source.naics' : 454110,
   'extra.source.sector' : 'Retail Trade',
   'extra.ssl_poodle' : 'N',
   'extra.ssl_version' : 2,
   'extra.subject_country' : 'US',
   'extra.subject_locality_name' : 'Hanover',
   'extra.subject_organization_name' : 'Ciena Corporation',
   'extra.subject_state_or_province_name' : 'Maryland',
   'extra.tag' : 'ssl,vpn',
   'extra.validation_level' : 'OV',
   'feed.name' : 'Accessible SSL',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicG9ydCIsImhvc3RuYW1lIiwidGFnIiwiaGFuZHNoYWtlIiwiYXNuIiwiZ2VvIiwicmVnaW9uIiwiY2l0eSIsImNpcGhlcl9zdWl0ZSIsInNzbF9wb29kbGUiLCJjZXJ0X2xlbmd0aCIsInN1YmplY3RfY29tbW9uX25hbWUiLCJpc3N1ZXJfY29tbW9uX25hbWUiLCJjZXJ0X2lzc3VlX2RhdGUiLCJjZXJ0X2V4cGlyYXRpb25fZGF0ZSIsInNoYTFfZmluZ2VycHJpbnQiLCJjZXJ0X3NlcmlhbF9udW1iZXIiLCJzc2xfdmVyc2lvbiIsInNpZ25hdHVyZV9hbGdvcml0aG0iLCJrZXlfYWxnb3JpdGhtIiwic3ViamVjdF9vcmdhbml6YXRpb25fbmFtZSIsInN1YmplY3Rfb3JnYW5pemF0aW9uX3VuaXRfbmFtZSIsInN1YmplY3RfY291bnRyeSIsInN1YmplY3Rfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsInN1YmplY3RfbG9jYWxpdHlfbmFtZSIsInN1YmplY3Rfc3RyZWV0X2FkZHJlc3MiLCJzdWJqZWN0X3Bvc3RhbF9jb2RlIiwic3ViamVjdF9zdXJuYW1lIiwic3ViamVjdF9naXZlbl9uYW1lIiwic3ViamVjdF9lbWFpbF9hZGRyZXNzIiwic3ViamVjdF9idXNpbmVzc19jYXRlZ29yeSIsInN1YmplY3Rfc2VyaWFsX251bWJlciIsImlzc3Vlcl9vcmdhbml6YXRpb25fbmFtZSIsImlzc3Vlcl9vcmdhbml6YXRpb25fdW5pdF9uYW1lIiwiaXNzdWVyX2NvdW50cnkiLCJpc3N1ZXJfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsImlzc3Vlcl9sb2NhbGl0eV9uYW1lIiwiaXNzdWVyX3N0cmVldF9hZGRyZXNzIiwiaXNzdWVyX3Bvc3RhbF9jb2RlIiwiaXNzdWVyX3N1cm5hbWUiLCJpc3N1ZXJfZ2l2ZW5fbmFtZSIsImlzc3Vlcl9lbWFpbF9hZGRyZXNzIiwiaXNzdWVyX2J1c2luZXNzX2NhdGVnb3J5IiwiaXNzdWVyX3NlcmlhbF9udW1iZXIiLCJuYWljcyIsInNpYyIsImZyZWFrX3Z1bG5lcmFibGUiLCJmcmVha19jaXBoZXJfc3VpdGUiLCJzZWN0b3IiLCJzaGEyNTZfZmluZ2VycHJpbnQiLCJzaGE1MTJfZmluZ2VycHJpbnQiLCJtZDVfZmluZ2VycHJpbnQiLCJodHRwX3Jlc3BvbnNlX3R5cGUiLCJodHRwX2NvZGUiLCJodHRwX3JlYXNvbiIsImNvbnRlbnRfdHlwZSIsImh0dHBfY29ubmVjdGlvbiIsInd3d19hdXRoZW50aWNhdGUiLCJzZXRfY29va2llIiwic2VydmVyX3R5cGUiLCJjb250ZW50X2xlbmd0aCIsInRyYW5zZmVyX2VuY29kaW5nIiwiaHR0cF9kYXRlIiwiY2VydF92YWxpZCIsInNlbGZfc2lnbmVkIiwiY2VydF9leHBpcmVkIiwiYnJvd3Nlcl90cnVzdGVkIiwidmFsaWRhdGlvbl9sZXZlbCIsImJyb3dzZXJfZXJyb3IiLCJ0bHN2MTNfc3VwcG9ydCIsInRsc3YxM19jaXBoZXIiLCJqYXJtIgoiMjAyMi0wMS0xMCAwMDowMTo0MiIsIjM0LjIyNC4wLjAiLDEwNDQzLCIiLCJzc2wsdnBuIiwiVExTdjEuMiIsMTQ2MTgsIlVTIiwiVklSR0lOSUEiLCJBU0hCVVJOIiwiVExTX0VDREhFX1JTQV9XSVRIX0FFU18yNTZfQ0JDX1NIQSIsIk4iLDIwNDgsIiIsIkVudHJ1c3QgQ2VydGlmaWNhdGlvbiBBdXRob3JpdHkgLSBMMUsiLCIyMDIxLTEwLTA3IDE1OjMwOjI4IiwiMjAyMi0xMS0wNiAxNTozMDoyOCIsIkFEOjE5OkIyOjFDOkNCOjg4OjcwOjlCOkRCOjhFOjdFOkY1OjY1OjUwOjEzOkQ2OjQzOjZDOkJFOjZFIiwiN0IzODgzNjRBMjRCODhFNzdFNTU1M0I1QzY3NDgxMDAiLDIsInNoYTI1NldpdGhSU0FFbmNyeXB0aW9uIiwicnNhRW5jcnlwdGlvbiIsIkNpZW5hIENvcnBvcmF0aW9uIiwsIlVTIiwiTWFyeWxhbmQiLCJIYW5vdmVyIiwsLCwsLCwsIkVudHJ1c3QsIEluYy4iLCIoYykgMjAxMiBFbnRydXN0LCBJbmMuIC0gZm9yIGF1dGhvcml6ZWQgdXNlIG9ubHkiLCJVUyIsLCwsLCwsLCwsNDU0MTEwLCwiTiIsLCJSZXRhaWwgVHJhZGUiLCI5QTo2NDo3MzowQjo4QTpGQTpERToyMjpENDo2RDo1QTpDNjpDNDo2RjpENDpBNDoyQToyODpGQTo0MToxRTpGRjo4MTpEQzpENDpEOTowMDpGRDo3ODpERjpDNDpERCIsIjlBOkI3OkJEOjY4OjdEOkYzOkU3OkMxOkI3OkQzOkY0OjJGOjAxOkI2OkM0Ojc3OjkwOkEzOjJCOjFFOkMwOjg5OkY1OjA4OkVDOjQzOjg3OjM1OjYwOjM2OkQ0Ojg3OjYxOkFBOkI4OkE4OkIzOjhBOkU5OkYxOjA0OkFBOjVCOjY3OjEyOkZGOjYzOkQ1OjE0OjgwOjc3OjZFOjhGOjdEOkMzOkUyOjNBOkYzOjEzOkRGOjA4OjQzOjZDOkIwIiwiRTc6MzQ6QkM6OTI6ODQ6RkE6Mzk6REU6RTE6NDY6NkM6Mjc6REE6NUE6MDE6RjQiLCJIVFRQLzEuMSIsMjAwLCJPSyIsInRleHQvaHRtbCIsLCwsInh4eHh4eHh4LXh4eHh4IiwxMzEsLCJNb24sIDEwIEphbiAyMDIyIDAwOjAxOjQ0IEdNVCIsIlkiLCJOIiwiTiIsIlkiLCJPViIsLCws',
   'source.asn' : 14618,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'ASHBURN',
   'source.geolocation.region' : 'VIRGINIA',
   'source.ip' : '34.224.0.0',
   'source.port' : 10443,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:01:42+00:00'
}
]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
