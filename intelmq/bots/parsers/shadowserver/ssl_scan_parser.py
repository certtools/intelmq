# -*- coding: utf-8 -*-

"""
https://www.shadowserver.org/wiki/pmwiki.php/Services/Ssl-Scan

timestamp              Time that the IP was probed in UTC+0
ip                     The IP address of the device in question
port                   Port that the SSL response came from
hostname               Reverse DNS name of the device in question
tag                    Report tag (ssl)
handshake              The highest SSL handshake that could be negotiated (TLSv1.2, TLSv1.1, TLSv1.0, SSLv3)
asn                    ASN of where the device in question resides
geo                    Country where the device in question resides
region                 State / Province / Administrative region where the device in question resides
city                   City in which the device in question resides
cipher_suite           The highest CipherSuite that was able to be negotiated
ssl_poodle             If "Y", then the device completed an SSLv3 handshake that used CBC (Cipher-Block Chaining) CipherSuites, which is vulnerable to a POODLE attack
cert_length            Certificate Key Length (1024 bit, 2048 bit, et cetera)
subject_common_name    The Common Name (CN) of the SSL certificate
issuer_common_name     The Common Name of the entity that signed the SSL certificate
cert_issue_date        Date when the SSL certificate became valid
cert_expiration_date   Date when the SSL certificate expires
sha1_fingerprint                 [UNDOCUMENTED]
cert_serial_number               [UNDOCUMENTED]
ssl_version                      [UNDOCUMENTED]
signature_algorithm              [UNDOCUMENTED]
key_algorithm                    [UNDOCUMENTED]
subject_organization_name        [UNDOCUMENTED]
subject_organization_unit_name   [UNDOCUMENTED]
subject_country                  [UNDOCUMENTED]
subject_state_or_province_name   [UNDOCUMENTED]
subject_locality_name            [UNDOCUMENTED]
subject_street_address           [UNDOCUMENTED]
subject_postal_code              [UNDOCUMENTED]
subject_surname                  [UNDOCUMENTED]
subject_given_name               [UNDOCUMENTED]
subject_email_address            [UNDOCUMENTED]
subject_business_category        [UNDOCUMENTED]
subject_serial_number            [UNDOCUMENTED]
issuer_organization_name         [UNDOCUMENTED]
issuer_organization_unit_name    [UNDOCUMENTED]
issuer_country                   [UNDOCUMENTED]
issuer_state_or_province_name    [UNDOCUMENTED]
issuer_locality_name             [UNDOCUMENTED]
issuer_street_address            [UNDOCUMENTED]
issuer_postal_code               [UNDOCUMENTED]
issuer_surname                   [UNDOCUMENTED]
issuer_given_name                [UNDOCUMENTED]
issuer_email_address             [UNDOCUMENTED]
issuer_business_category         [UNDOCUMENTED]
issuer_serial_number             [UNDOCUMENTED]
naics                            [UNDOCUMENTED]
sic                              [UNDOCUMENTED]
sector                           [UNDOCUMENTED]
sha256_fingerprint               [UNDOCUMENTED]
sha512_fingerprint               [UNDOCUMENTED]
md5_fingerprint                  [UNDOCUMENTED]
"""

import csv
import io
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

from intelmq.lib.exceptions import InvalidValue


class ShadowServerSSLScanParserBot(Bot):

    mapping = [
        ("protocol.transport"         , "protocol"),
        ("source.reverse_dns"         , "hostname"),
        ("source.asn"                 , "asn"),
        ("source.geolocation.cc"      , "geo"),
        ("source.geolocation.region"  , "region"),
        ("source.geolocation.city"    , "city"),
    ]

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report["raw"])
        for row in csv.DictReader(io.StringIO(raw_report)):

            event = Event(report)
            extra = {}

            # Required fields which must not fail
            event.add('time.source', row['timestamp']+' UTC')
            event.add('source.ip', row['ip'])
            event.add('source.port', row['port'])
            event.add('classification.type', 'vulnerable service')

            # Add events
            for item in self.mapping:
                intelmq_key, shadow_key = item[:2]
                if len(item) > 2:
                    conv = item[2]
                else:
                    conv = None
                value = row.get(shadow_key)
                raw_value = value
                if raw_value is not None:
                    if conv is not None:
                        value = conv(raw_value)
                    else:
                        value = raw_value
                    try:
                        event.add(intelmq_key, value)
                    except InvalidValue:
                        self.logger.warn(
                                'Could not add event "{}";'\
                                ' adding it to extras...'.format(shadow_key)
                        )
                        extra[shadow_key] = raw_value

            # Add extras
            if int(row['naics']):
                extra['naics'] = int(row['naics'])
            if int(row['sic']):
                extra['sic'] = int(row['sic'])
            # documented extra fields
            if row['tag']:
                extra['tag'] = row['tag']
            if row['handshake']:
                extra['handshake'] = row['tag']
            # undocumented extra fields
            for field in [
                    "sha1_fingerprint"               ,
                    "cert_serial_number"             ,
                    "ssl_version"                    ,
                    "signature_algorithm"            ,
                    "key_algorithm"                  ,
                    "subject_organization_name"      ,
                    "subject_organization_unit_name" ,
                    "subject_country"                ,
                    "subject_state_or_province_name" ,
                    "subject_locality_name"          ,
                    "subject_street_address"         ,
                    "subject_postal_code"            ,
                    "subject_surname"                ,
                    "subject_given_name"             ,
                    "subject_email_address"          ,
                    "subject_business_category"      ,
                    "subject_serial_number"          ,
                    "issuer_organization_name"       ,
                    "issuer_organization_unit_name"  ,
                    "issuer_country"                 ,
                    "issuer_state_or_province_name"  ,
                    "issuer_locality_name"           ,
                    "issuer_street_address"          ,
                    "issuer_postal_code"             ,
                    "issuer_surname"                 ,
                    "issuer_given_name"              ,
                    "issuer_email_address"           ,
                    "issuer_business_category"       ,
                    "issuer_serial_number"           ,
                    "naics"                          ,
                    "sic"                            ,
                    "sector"                         ,
                    "sha256_fingerprint"             ,
                    "sha512_fingerprint"             ,
                    "md5_fingerprint"
                    ]:
                if field in row:
                    extra[field] = row[field]

            event.add('raw', '"'+','.join(map(str, row.items()))+'"')
            if extra:
                event.add('extra', extra)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ShadowServerSSLScanParserBot(sys.argv[1])
    bot.start()
