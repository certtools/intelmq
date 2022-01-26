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
                       'testdata/scan_mqtt_anon.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open Anonymous MQTT',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-scan_mqtt_anon-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'scan-mqtt-anon',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.cert_expiration_date' : '2030-05-06 08:07:05',
   'extra.cert_issue_date' : '2020-05-08 08:07:05',
   'extra.cert_length' : 2048,
   'extra.cert_serial_number' : '02',
   'extra.cipher_suite' : 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
   'extra.code' : 'Connection Accepted',
   'extra.hex_code' : '00',
   'extra.issuer_common_name' : 'RootCA',
   'extra.issuer_country' : 'CN',
   'extra.issuer_organization_name' : 'EMQ',
   'extra.issuer_state_or_province_name' : 'hangzhou',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : 'AB:A8:E0:2C:EF:AE:BF:9D:DD:FA:70:BA:2F:F2:CA:5C',
   'extra.raw_response' : '20020000',
   'extra.sha1_fingerprint' : '70:1A:1E:1F:EC:5F:7E:A9:12:32:B2:C9:8A:C9:EE:91:8E:0B:82:45',
   'extra.sha256_fingerprint' : '85:26:A2:F2:A2:50:CD:96:33:19:A6:2D:12:2E:97:6B:D3:06:3C:11:EA:01:B4:B7:25:2A:B7:4F:0A:8F:45:40',
   'extra.sha512_fingerprint' : '72:50:07:30:9A:6F:CB:FD:E2:80:69:02:65:62:77:16:C3:B4:0C:98:44:4E:D4:2C:AC:6B:AF:F8:9E:AB:51:C2:FA:A8:72:A3:45:DF:81:09:50:08:18:EB:03:34:FC:92:33:A7:12:46:FE:90:20:91:86:C5:4D:89:48:86:4C:CD',
   'extra.signature_algorithm' : 'sha256WithRSAEncryption',
   'extra.source.naics' : 518210,
   'extra.ssl_version' : 2,
   'extra.subject_common_name' : 'Server',
   'extra.subject_country' : 'CN',
   'extra.subject_organization_name' : 'EMQ',
   'extra.subject_state_or_province_name' : 'hangzhou',
   'extra.tag' : 'mqtt,mqtt-anon',
   'feed.name' : 'Open Anonymous MQTT',
   'protocol.application' : 'mqtt',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJhc24iLCJnZW8iLCJyZWdpb24iLCJjaXR5IiwibmFpY3MiLCJzaWMiLCJyYXdfcmVzcG9uc2UiLCJoZXhfY29kZSIsImNvZGUiLCJjaXBoZXJfc3VpdGUiLCJjZXJ0X2xlbmd0aCIsInN1YmplY3RfY29tbW9uX25hbWUiLCJpc3N1ZXJfY29tbW9uX25hbWUiLCJjZXJ0X2lzc3VlX2RhdGUiLCJjZXJ0X2V4cGlyYXRpb25fZGF0ZSIsInNoYTFfZmluZ2VycHJpbnQiLCJzaGEyNTZfZmluZ2VycHJpbnQiLCJzaGE1MTJfZmluZ2VycHJpbnQiLCJtZDVfZmluZ2VycHJpbnQiLCJjZXJ0X3NlcmlhbF9udW1iZXIiLCJzc2xfdmVyc2lvbiIsInNpZ25hdHVyZV9hbGdvcml0aG0iLCJrZXlfYWxnb3JpdGhtIiwic3ViamVjdF9vcmdhbml6YXRpb25fbmFtZSIsInN1YmplY3Rfb3JnYW5pemF0aW9uX3VuaXRfbmFtZSIsInN1YmplY3RfY291bnRyeSIsInN1YmplY3Rfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsInN1YmplY3RfbG9jYWxpdHlfbmFtZSIsInN1YmplY3Rfc3RyZWV0X2FkZHJlc3MiLCJzdWJqZWN0X3Bvc3RhbF9jb2RlIiwic3ViamVjdF9zdXJuYW1lIiwic3ViamVjdF9naXZlbl9uYW1lIiwic3ViamVjdF9lbWFpbF9hZGRyZXNzIiwic3ViamVjdF9idXNpbmVzc19jYXRlZ29yeSIsInN1YmplY3Rfc2VyaWFsX251bWJlciIsImlzc3Vlcl9vcmdhbml6YXRpb25fbmFtZSIsImlzc3Vlcl9vcmdhbml6YXRpb25fdW5pdF9uYW1lIiwiaXNzdWVyX2NvdW50cnkiLCJpc3N1ZXJfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsImlzc3Vlcl9sb2NhbGl0eV9uYW1lIiwiaXNzdWVyX3N0cmVldF9hZGRyZXNzIiwiaXNzdWVyX3Bvc3RhbF9jb2RlIiwiaXNzdWVyX3N1cm5hbWUiLCJpc3N1ZXJfZ2l2ZW5fbmFtZSIsImlzc3Vlcl9lbWFpbF9hZGRyZXNzIiwiaXNzdWVyX2J1c2luZXNzX2NhdGVnb3J5IiwiaXNzdWVyX3NlcmlhbE51bWJlciIKIjIwMjItMDEtMTAgMDA6NTk6MzQiLCI0Ny4xMDYuMC4wIiwidGNwIiw4ODgzLCwibXF0dCxtcXR0LWFub24iLDM3OTYzLCJDTiIsIkdVQU5HRE9ORyBTSEVORyIsIlNIRU5aSEVOIiw1MTgyMTAsLDIwMDIwMDAwLDAwLCJDb25uZWN0aW9uIEFjY2VwdGVkIiwiVExTX0VDREhFX1JTQV9XSVRIX0FFU18xMjhfR0NNX1NIQTI1NiIsMjA0OCwiU2VydmVyIiwiUm9vdENBIiwiMjAyMC0wNS0wOCAwODowNzowNSIsIjIwMzAtMDUtMDYgMDg6MDc6MDUiLCI3MDoxQToxRToxRjpFQzo1Rjo3RTpBOToxMjozMjpCMjpDOTo4QTpDOTpFRTo5MTo4RTowQjo4Mjo0NSIsIjg1OjI2OkEyOkYyOkEyOjUwOkNEOjk2OjMzOjE5OkE2OjJEOjEyOjJFOjk3OjZCOkQzOjA2OjNDOjExOkVBOjAxOkI0OkI3OjI1OjJBOkI3OjRGOjBBOjhGOjQ1OjQwIiwiNzI6NTA6MDc6MzA6OUE6NkY6Q0I6RkQ6RTI6ODA6Njk6MDI6NjU6NjI6Nzc6MTY6QzM6QjQ6MEM6OTg6NDQ6NEU6RDQ6MkM6QUM6NkI6QUY6Rjg6OUU6QUI6NTE6QzI6RkE6QTg6NzI6QTM6NDU6REY6ODE6MDk6NTA6MDg6MTg6RUI6MDM6MzQ6RkM6OTI6MzM6QTc6MTI6NDY6RkU6OTA6MjA6OTE6ODY6QzU6NEQ6ODk6NDg6ODY6NEM6Q0QiLCJBQjpBODpFMDoyQzpFRjpBRTpCRjo5RDpERDpGQTo3MDpCQToyRjpGMjpDQTo1QyIsMDIsMiwic2hhMjU2V2l0aFJTQUVuY3J5cHRpb24iLCJyc2FFbmNyeXB0aW9uIiwiRU1RIiwsIkNOIiwiaGFuZ3pob3UiLCwsLCwsLCwsIkVNUSIsLCJDTiIsImhhbmd6aG91IiwsLCwsLCws',
   'source.asn' : 37963,
   'source.geolocation.cc' : 'CN',
   'source.geolocation.city' : 'SHENZHEN',
   'source.geolocation.region' : 'GUANGDONG SHENG',
   'source.ip' : '47.106.0.0',
   'source.port' : 8883,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:59:34+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'scan-mqtt-anon',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.cert_expiration_date' : '2022-03-06 13:48:03',
   'extra.cert_issue_date' : '2021-12-06 13:48:04',
   'extra.cert_length' : 2048,
   'extra.cert_serial_number' : '06B25BEAD1F43266ABCFCDDE408D3544D04B',
   'extra.cipher_suite' : 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
   'extra.code' : 'Connection Accepted',
   'extra.hex_code' : '00',
   'extra.issuer_common_name' : 'R3',
   'extra.issuer_country' : 'US',
   'extra.issuer_organization_name' : 'Lets Encrypt',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : '23:99:39:C6:77:D8:9F:55:90:FC:A5:FB:BA:72:8B:42',
   'extra.raw_response' : '20020000',
   'extra.sha1_fingerprint' : '20:0E:AC:E7:AF:07:8D:D3:16:7C:63:D1:B9:12:AD:1D:2C:F0:46:86',
   'extra.sha256_fingerprint' : 'DD:7A:4C:8A:1D:66:1D:7C:F5:17:04:5B:A0:B4:C4:E0:80:58:44:B4:DB:A7:5E:61:AE:43:9D:85:4C:9E:DC:83',
   'extra.sha512_fingerprint' : '55:B6:3D:56:A4:39:6E:99:B6:AF:72:AF:4D:3C:7C:C5:A8:C5:4F:A1:79:92:D0:46:8A:A2:9B:2A:48:0D:00:68:39:F0:B8:67:B4:E0:88:51:2A:D7:55:46:83:BD:ED:1E:09:6E:DB:3D:21:E2:AA:DB:42:6A:33:45:1A:2A:DB:4C',
   'extra.signature_algorithm' : 'sha256WithRSAEncryption',
   'extra.source.naics' : 518210,
   'extra.ssl_version' : 2,
   'extra.subject_common_name' : 'example.com',
   'extra.tag' : 'mqtt,mqtt-anon',
   'feed.name' : 'Open Anonymous MQTT',
   'protocol.application' : 'mqtt',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJhc24iLCJnZW8iLCJyZWdpb24iLCJjaXR5IiwibmFpY3MiLCJzaWMiLCJyYXdfcmVzcG9uc2UiLCJoZXhfY29kZSIsImNvZGUiLCJjaXBoZXJfc3VpdGUiLCJjZXJ0X2xlbmd0aCIsInN1YmplY3RfY29tbW9uX25hbWUiLCJpc3N1ZXJfY29tbW9uX25hbWUiLCJjZXJ0X2lzc3VlX2RhdGUiLCJjZXJ0X2V4cGlyYXRpb25fZGF0ZSIsInNoYTFfZmluZ2VycHJpbnQiLCJzaGEyNTZfZmluZ2VycHJpbnQiLCJzaGE1MTJfZmluZ2VycHJpbnQiLCJtZDVfZmluZ2VycHJpbnQiLCJjZXJ0X3NlcmlhbF9udW1iZXIiLCJzc2xfdmVyc2lvbiIsInNpZ25hdHVyZV9hbGdvcml0aG0iLCJrZXlfYWxnb3JpdGhtIiwic3ViamVjdF9vcmdhbml6YXRpb25fbmFtZSIsInN1YmplY3Rfb3JnYW5pemF0aW9uX3VuaXRfbmFtZSIsInN1YmplY3RfY291bnRyeSIsInN1YmplY3Rfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsInN1YmplY3RfbG9jYWxpdHlfbmFtZSIsInN1YmplY3Rfc3RyZWV0X2FkZHJlc3MiLCJzdWJqZWN0X3Bvc3RhbF9jb2RlIiwic3ViamVjdF9zdXJuYW1lIiwic3ViamVjdF9naXZlbl9uYW1lIiwic3ViamVjdF9lbWFpbF9hZGRyZXNzIiwic3ViamVjdF9idXNpbmVzc19jYXRlZ29yeSIsInN1YmplY3Rfc2VyaWFsX251bWJlciIsImlzc3Vlcl9vcmdhbml6YXRpb25fbmFtZSIsImlzc3Vlcl9vcmdhbml6YXRpb25fdW5pdF9uYW1lIiwiaXNzdWVyX2NvdW50cnkiLCJpc3N1ZXJfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsImlzc3Vlcl9sb2NhbGl0eV9uYW1lIiwiaXNzdWVyX3N0cmVldF9hZGRyZXNzIiwiaXNzdWVyX3Bvc3RhbF9jb2RlIiwiaXNzdWVyX3N1cm5hbWUiLCJpc3N1ZXJfZ2l2ZW5fbmFtZSIsImlzc3Vlcl9lbWFpbF9hZGRyZXNzIiwiaXNzdWVyX2J1c2luZXNzX2NhdGVnb3J5IiwiaXNzdWVyX3NlcmlhbE51bWJlciIKIjIwMjItMDEtMTAgMDA6NTk6MzQiLCIxNDQuNzYuMC4wIiwidGNwIiw4ODgzLCwibXF0dCxtcXR0LWFub24iLDI0OTQwLCJERSIsIlNBQ0hTRU4tQU5IQUxUIiwiV0VSTklHRVJPREUiLDUxODIxMCwsMjAwMjAwMDAsMDAsIkNvbm5lY3Rpb24gQWNjZXB0ZWQiLCJUTFNfRUNESEVfUlNBX1dJVEhfQUVTXzEyOF9HQ01fU0hBMjU2IiwyMDQ4LCJleGFtcGxlLmNvbSIsIlIzIiwiMjAyMS0xMi0wNiAxMzo0ODowNCIsIjIwMjItMDMtMDYgMTM6NDg6MDMiLCIyMDowRTpBQzpFNzpBRjowNzo4RDpEMzoxNjo3Qzo2MzpEMTpCOToxMjpBRDoxRDoyQzpGMDo0Njo4NiIsIkREOjdBOjRDOjhBOjFEOjY2OjFEOjdDOkY1OjE3OjA0OjVCOkEwOkI0OkM0OkUwOjgwOjU4OjQ0OkI0OkRCOkE3OjVFOjYxOkFFOjQzOjlEOjg1OjRDOjlFOkRDOjgzIiwiNTU6QjY6M0Q6NTY6QTQ6Mzk6NkU6OTk6QjY6QUY6NzI6QUY6NEQ6M0M6N0M6QzU6QTg6QzU6NEY6QTE6Nzk6OTI6RDA6NDY6OEE6QTI6OUI6MkE6NDg6MEQ6MDA6Njg6Mzk6RjA6Qjg6Njc6QjQ6RTA6ODg6NTE6MkE6RDc6NTU6NDY6ODM6QkQ6RUQ6MUU6MDk6NkU6REI6M0Q6MjE6RTI6QUE6REI6NDI6NkE6MzM6NDU6MUE6MkE6REI6NEMiLCIyMzo5OTozOTpDNjo3NzpEODo5Rjo1NTo5MDpGQzpBNTpGQjpCQTo3Mjo4Qjo0MiIsIjA2QjI1QkVBRDFGNDMyNjZBQkNGQ0RERTQwOEQzNTQ0RDA0QiIsMiwic2hhMjU2V2l0aFJTQUVuY3J5cHRpb24iLCJyc2FFbmNyeXB0aW9uIiwsLCwsLCwsLCwsLCwiTGV0cyBFbmNyeXB0IiwsIlVTIiwsLCwsLCwsLA==',
   'source.asn' : 24940,
   'source.geolocation.cc' : 'DE',
   'source.geolocation.city' : 'WERNIGERODE',
   'source.geolocation.region' : 'SACHSEN-ANHALT',
   'source.ip' : '144.76.0.0',
   'source.port' : 8883,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:59:34+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'scan-mqtt-anon',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.cert_expiration_date' : '2030-08-05 16:51:57',
   'extra.cert_issue_date' : '2020-08-07 16:51:57',
   'extra.cert_length' : 2048,
   'extra.cert_serial_number' : 'A71541EFAE529B03',
   'extra.cipher_suite' : 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
   'extra.code' : 'Connection Accepted',
   'extra.hex_code' : '00',
   'extra.issuer_common_name' : 'ClearView2Dev',
   'extra.issuer_organization_name' : 'Sohonet',
   'extra.issuer_organization_unit_name' : 'ClearView2Dev',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : '43:0D:A7:89:9E:76:8D:6E:D5:AD:95:CC:F2:91:87:56',
   'extra.raw_response' : '20020000',
   'extra.sha1_fingerprint' : '32:4B:66:98:FA:5B:D2:D1:F2:53:83:21:19:11:5A:A9:BE:85:56:16',
   'extra.sha256_fingerprint' : 'AE:0D:65:34:2F:51:F7:32:1E:DF:B1:DA:12:C7:6A:DE:42:B5:4B:FF:80:2C:E5:EF:99:F6:CC:01:4B:C9:77:68',
   'extra.sha512_fingerprint' : '44:C4:B8:19:FA:39:55:51:EC:E4:6D:C4:6D:0F:A5:46:BB:D5:F9:FD:A6:8D:DF:F3:2D:D2:92:6C:0B:D5:D3:25:CB:19:50:9D:A6:A4:D4:D3:2E:53:10:F5:8D:77:F7:90:F8:65:A7:79:AB:14:62:72:01:F3:EA:38:E2:68:C7:25',
   'extra.signature_algorithm' : 'sha256WithRSAEncryption',
   'extra.ssl_version' : 0,
   'extra.subject_common_name' : 'foo.example.com',
   'extra.subject_locality_name' : '<',
   'extra.subject_organization_name' : 'Sohonet',
   'extra.tag' : 'mqtt,mqtt-anon',
   'feed.name' : 'Open Anonymous MQTT',
   'protocol.application' : 'mqtt',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJhc24iLCJnZW8iLCJyZWdpb24iLCJjaXR5IiwibmFpY3MiLCJzaWMiLCJyYXdfcmVzcG9uc2UiLCJoZXhfY29kZSIsImNvZGUiLCJjaXBoZXJfc3VpdGUiLCJjZXJ0X2xlbmd0aCIsInN1YmplY3RfY29tbW9uX25hbWUiLCJpc3N1ZXJfY29tbW9uX25hbWUiLCJjZXJ0X2lzc3VlX2RhdGUiLCJjZXJ0X2V4cGlyYXRpb25fZGF0ZSIsInNoYTFfZmluZ2VycHJpbnQiLCJzaGEyNTZfZmluZ2VycHJpbnQiLCJzaGE1MTJfZmluZ2VycHJpbnQiLCJtZDVfZmluZ2VycHJpbnQiLCJjZXJ0X3NlcmlhbF9udW1iZXIiLCJzc2xfdmVyc2lvbiIsInNpZ25hdHVyZV9hbGdvcml0aG0iLCJrZXlfYWxnb3JpdGhtIiwic3ViamVjdF9vcmdhbml6YXRpb25fbmFtZSIsInN1YmplY3Rfb3JnYW5pemF0aW9uX3VuaXRfbmFtZSIsInN1YmplY3RfY291bnRyeSIsInN1YmplY3Rfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsInN1YmplY3RfbG9jYWxpdHlfbmFtZSIsInN1YmplY3Rfc3RyZWV0X2FkZHJlc3MiLCJzdWJqZWN0X3Bvc3RhbF9jb2RlIiwic3ViamVjdF9zdXJuYW1lIiwic3ViamVjdF9naXZlbl9uYW1lIiwic3ViamVjdF9lbWFpbF9hZGRyZXNzIiwic3ViamVjdF9idXNpbmVzc19jYXRlZ29yeSIsInN1YmplY3Rfc2VyaWFsX251bWJlciIsImlzc3Vlcl9vcmdhbml6YXRpb25fbmFtZSIsImlzc3Vlcl9vcmdhbml6YXRpb25fdW5pdF9uYW1lIiwiaXNzdWVyX2NvdW50cnkiLCJpc3N1ZXJfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsImlzc3Vlcl9sb2NhbGl0eV9uYW1lIiwiaXNzdWVyX3N0cmVldF9hZGRyZXNzIiwiaXNzdWVyX3Bvc3RhbF9jb2RlIiwiaXNzdWVyX3N1cm5hbWUiLCJpc3N1ZXJfZ2l2ZW5fbmFtZSIsImlzc3Vlcl9lbWFpbF9hZGRyZXNzIiwiaXNzdWVyX2J1c2luZXNzX2NhdGVnb3J5IiwiaXNzdWVyX3NlcmlhbE51bWJlciIKIjIwMjItMDEtMTAgMDA6NTk6MzQiLCIxNzMuMC4wLjAiLCJ0Y3AiLDg4ODMsImV4YW1wbGUuY29tIiwibXF0dCxtcXR0LWFub24iLDU1NTUsIlVTIiwiQ0FMSUZPUk5JQSIsIkJVUkJBTksiLCwsMjAwMjAwMDAsMDAsIkNvbm5lY3Rpb24gQWNjZXB0ZWQiLCJUTFNfRUNESEVfUlNBX1dJVEhfQUVTXzI1Nl9DQkNfU0hBIiwyMDQ4LCJmb28uZXhhbXBsZS5jb20iLCJDbGVhclZpZXcyRGV2IiwiMjAyMC0wOC0wNyAxNjo1MTo1NyIsIjIwMzAtMDgtMDUgMTY6NTE6NTciLCIzMjo0Qjo2Njo5ODpGQTo1QjpEMjpEMTpGMjo1Mzo4MzoyMToxOToxMTo1QTpBOTpCRTo4NTo1NjoxNiIsIkFFOjBEOjY1OjM0OjJGOjUxOkY3OjMyOjFFOkRGOkIxOkRBOjEyOkM3OjZBOkRFOjQyOkI1OjRCOkZGOjgwOjJDOkU1OkVGOjk5OkY2OkNDOjAxOjRCOkM5Ojc3OjY4IiwiNDQ6QzQ6Qjg6MTk6RkE6Mzk6NTU6NTE6RUM6RTQ6NkQ6QzQ6NkQ6MEY6QTU6NDY6QkI6RDU6Rjk6RkQ6QTY6OEQ6REY6RjM6MkQ6RDI6OTI6NkM6MEI6RDU6RDM6MjU6Q0I6MTk6NTA6OUQ6QTY6QTQ6RDQ6RDM6MkU6NTM6MTA6RjU6OEQ6Nzc6Rjc6OTA6Rjg6NjU6QTc6Nzk6QUI6MTQ6NjI6NzI6MDE6RjM6RUE6Mzg6RTI6Njg6Qzc6MjUiLCI0MzowRDpBNzo4OTo5RTo3Njo4RDo2RTpENTpBRDo5NTpDQzpGMjo5MTo4Nzo1NiIsIkE3MTU0MUVGQUU1MjlCMDMiLDAsInNoYTI1NldpdGhSU0FFbmNyeXB0aW9uIiwicnNhRW5jcnlwdGlvbiIsIlNvaG9uZXQiLCwsLCI8IiwsLCwsLCwsIlNvaG9uZXQiLCJDbGVhclZpZXcyRGV2IiwsLCwsLCwsLCw=',
   'source.asn' : 5555,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'BURBANK',
   'source.geolocation.region' : 'CALIFORNIA',
   'source.ip' : '173.0.0.0',
   'source.port' : 8883,
   'source.reverse_dns' : 'example.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:59:34+00:00'
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
