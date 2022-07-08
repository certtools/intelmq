# SPDX-FileCopyrightText: 2022 Shadowserver Foundation
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_ssh.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible SSH',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-scan_ssh-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'open-ssh',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.algorithm' : 'ecdsa-sha2-nistp256',
   'extra.available_ciphers' : 'chacha20-poly1305@openssh.com, aes128-ctr, aes192-ctr, aes256-ctr, aes128-gcm@openssh.com, aes256-gcm@openssh.com, aes128-cbc, aes192-cbc, aes256-cbc, blowfish-cbc, cast128-cbc, 3des-cbc',
   'extra.available_compression' : 'none, zlib@openssh.com',
   'extra.available_kex' : 'curve25519-sha256, curve25519-sha256@libssh.org, ecdh-sha2-nistp256, ecdh-sha2-nistp384, ecdh-sha2-nistp521, diffie-hellman-group-exchange-sha256, diffie-hellman-group16-sha512, diffie-hellman-group18-sha512, diffie-hellman-group-exchange-sha1, diffie-hellman-group14-sha256, diffie-hellman-group14-sha1, diffie-hellman-group1-sha1',
   'extra.available_mac' : 'umac-64-etm@openssh.com, umac-128-etm@openssh.com, hmac-sha2-256-etm@openssh.com, hmac-sha2-512-etm@openssh.com, hmac-sha1-etm@openssh.com, umac-64@openssh.com, umac-128@openssh.com, hmac-sha2-256, hmac-sha2-512, hmac-sha1',
   'extra.ecdsa_curve' : 'P-256',
   'extra.ecdsa_curve25519' : '1xx7ASut7BF4ED8b592bebZBMBKTCzOsmbH4cjwx/0U=',
   'extra.ecdsa_public_key_b' : 'WsY12Ko6k+ez671VdpiGvGUdBrDMU7D2O848PifSYEs=',
   'extra.ecdsa_public_key_gx' : 'axfR8uEsQkf4vOblY6RA8ncDfYEt6zOg9KE5RdiYwpY=',
   'extra.ecdsa_public_key_gy' : 'T+NC4v4af5uO5+tKfA+eFivOM1drMV7Oy7ZAaDe/UfU=',
   'extra.ecdsa_public_key_length' : '256',
   'extra.ecdsa_public_key_n' : '/////wAAAAD//////////7zm+q2nF56E87nKwvxjJVE=',
   'extra.ecdsa_public_key_p' : '/////wAAAAEAAAAAAAAAAAAAAAD///////////////8=',
   'extra.ecdsa_public_key_x' : 'NIQdotpy2HAHfSu0DjEmA3cb3NeQKabZaFX9OU0GsPY=',
   'extra.ecdsa_public_key_y' : '0fuNQAZX7XciX2YkqIHtK2dWLBYwVCCqvl//zoM42kI=',
   'extra.selected_cipher' : 'aes128-ctr',
   'extra.selected_compression' : 'none',
   'extra.selected_kex' : 'curve25519-sha256@libssh.org',
   'extra.selected_mac' : 'hmac-sha2-256',
   'extra.server_cookie' : 'bGjsifbPIDWT7tAu8BMjyg==',
   'extra.server_host_key' : 'AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBDSEHaLacthwB30rtA4xJgN3G9zXkCmm2WhV/TlNBrD20fuNQAZX7XciX2YkqIHtK2dWLBYwVCCqvl//zoM42kI=',
   'extra.server_host_key_sha256' : 'a6e4e1c16ba25d51bcddc58a6e16797144575dd18d02d9dedf75093d2b15c557',
   'extra.server_signature_raw' : 'AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAABKAAAAIQCd+X/B/OEx+FrwJSlVecOvNMuS5w2vTRz0z4prM+5VBwAAACEArU60b9CHs/d5BgyaOd7vmFygTMK5SyL90bS8VIztX/4=',
   'extra.server_signature_value' : 'AAAAIQCd+X/B/OEx+FrwJSlVecOvNMuS5w2vTRz0z4prM+5VBwAAACEArU60b9CHs/d5BgyaOd7vmFygTMK5SyL90bS8VIztX/4=',
   'extra.serverid_raw' : 'SSH-2.0-OpenSSH_7.4',
   'extra.serverid_software' : 'OpenSSH_7.4',
   'extra.serverid_version' : '2.0',
   'extra.source.naics' : 454110,
   'extra.tag' : 'ssh',
   'extra.userauth_methods' : 'publickey',
   'feed.name' : 'Accessible SSH',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
   'source.asn' : 16509,
   'source.geolocation.cc' : 'JP',
   'source.geolocation.city' : 'TOKYO',
   'source.geolocation.region' : 'TOKYO',
   'source.ip' : '18.179.0.0',
   'source.port' : 22,
   'source.reverse_dns' : 'ec2-18-179-0-0.ap-northeast-1.compute.amazonaws.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T02:20:37+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-ssh',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.algorithm' : 'ssh-rsa',
   'extra.available_ciphers' : 'aes128-cbc, 3des-cbc, aes256-cbc, twofish256-cbc, twofish-cbc, twofish128-cbc, blowfish-cbc',
   'extra.available_compression' : 'none',
   'extra.available_kex' : 'diffie-hellman-group1-sha1',
   'extra.available_mac' : 'hmac-sha1-96, hmac-sha1, hmac-md5',
   'extra.device_vendor' : 'Arris',
   'extra.rsa_exponent' : '65537',
   'extra.rsa_length' : '1040',
   'extra.rsa_modulus' : 'g6tZBqqsHUFa8gjXKMg2waZy/6JLzNnfTZkdDo6a3E6Amdk2eVlGbdgRsDxNUCyWLJI4b+xsJX0OKoRKhw4N+cDK5Du4/S00Auylt8YrDi7lIpeBZjMT5KJerN/feOcwRqY8NJfwZiZ1A5brcWr5HXfOH6aRTMFzadr248VdUmFXPQ==',
   'extra.selected_cipher' : 'aes128-cbc',
   'extra.selected_compression' : 'none',
   'extra.selected_kex' : 'diffie-hellman-group1-sha1',
   'extra.selected_mac' : 'hmac-sha1',
   'extra.server_cookie' : 'Y4RQS9sdRgEFwNJKVP6bZg==',
   'extra.server_host_key' : 'AAAAB3NzaC1yc2EAAAADAQABAAAAgwCDq1kGqqwdQVryCNcoyDbBpnL/okvM2d9NmR0OjprcToCZ2TZ5WUZt2BGwPE1QLJYskjhv7GwlfQ4qhEqHDg35wMrkO7j9LTQC7KW3xisOLuUil4FmMxPkol6s39945zBGpjw0l/BmJnUDlutxavkdd84fppFMwXNp2vbjxV1SYVc9',
   'extra.server_host_key_sha256' : 'd53fedbfe92e631264629882b2e85bfd213ca4b07b824cd31f8de1fcb8d0ddcb',
   'extra.server_signature_raw' : 'AAAAB3NzaC1yc2EAAACCLQj+UTJEQqdb/p/c/19yVc63eo+rnedwXKjP6eNNxxijN2cFoOjVMeqT2QTBjyoN7yRWBU2EID+3y2jUYT8mCqmqfyUv1eEbiCfLVlUyQ0X/CY9I5DDb5l6yEjNkuH2xVNNV6R7GFRwyYKAsYzfy+i9o1OORlUh3tozkkPfA9z/NlA==',
   'extra.server_signature_value' : 'LQj+UTJEQqdb/p/c/19yVc63eo+rnedwXKjP6eNNxxijN2cFoOjVMeqT2QTBjyoN7yRWBU2EID+3y2jUYT8mCqmqfyUv1eEbiCfLVlUyQ0X/CY9I5DDb5l6yEjNkuH2xVNNV6R7GFRwyYKAsYzfy+i9o1OORlUh3tozkkPfA9z/NlA==',
   'extra.serverid_raw' : 'SSH-2.0-ARRIS_0.50',
   'extra.serverid_software' : 'ARRIS_0.50',
   'extra.serverid_version' : '2.0',
   'extra.tag' : 'ssh',
   'extra.userauth_methods' : 'publickey, password',
   'feed.name' : 'Accessible SSH',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
   'source.asn' : 11976,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'MARSHALL',
   'source.geolocation.region' : 'TEXAS',
   'source.ip' : '170.10.0.0',
   'source.port' : 22,
   'source.reverse_dns' : '170-10-0-0.example.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T02:20:37+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-ssh',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.algorithm' : 'ssh-rsa',
   'extra.available_ciphers' : 'aes128-cbc, 3des-cbc, aes192-cbc, aes256-cbc',
   'extra.available_compression' : 'none',
   'extra.available_kex' : 'diffie-hellman-group-exchange-sha1, diffie-hellman-group14-sha1, diffie-hellman-group1-sha1',
   'extra.available_mac' : 'hmac-sha1, hmac-sha1-96, hmac-md5, hmac-md5-96',
   'extra.device_sector' : 'enterprise',
   'extra.device_vendor' : 'Cisco',
   'extra.rsa_exponent' : '65537',
   'extra.rsa_length' : '4096',
   'extra.rsa_modulus' : 'yFVwcChoYt+YGm8BzWYugcZbNQRrQ1VWRYcL4U6SSkyoVeE9h5wxRu/hQaWHo3PdsB9Nuln/riRyKZypFUEZ5zlffMyl1uvE8/jp8E/GgUHSyPkGAwu8C8BkX/nDolxAJKTK6djiZnvhsEPe6AXHBMHbto/b3GABUNPngjzX8D63GYcFW9NJLf5qC1UsVkXbAzM0IjQ2X9s3pfhUCAJeXAn2i0gEGtUyF8vEjNdwdG655aXciKrpEEtM1L/zy/+gLH4YC13kAYI7NVyH+qi/mXbULLOQClA7iYK1g3Et58jWUIPwgLfF3SLC57bt2wp/lRgNTv4FBi0tWvRqBnf5UQK5ZjgzbW3bO+Ju4cWgH/4M4NCxSceh4cLm5lQs01xB5feSh2ByqA7wrVDoFJu81LoMVo4bCz30+lH2QsLwmNtUhlWLKBD4k09g4bgBa4jPj0/Nya3rBR4GQ6LG6ltFQotm8wCkgbv76YWqk20nQ6NMYZFvSQm981JFtoHv3vxq48VeHDV0QvV0P12BCFprRf4B0otIvSsHl+LDeUxJAf+Nbw78gzncjyfCbWtCPbwaJQ8CeqnTBzj5TluaFvN8goG5lCTWJGfjIrwAZXOokv9NOqmIiMJJx3s22OX6GHfJAzje2ALLDsAiXBub4iCOdGdTfVbBpFL+bGTK9qfa8vE=',
   'extra.selected_cipher' : 'aes128-cbc',
   'extra.selected_compression' : 'none',
   'extra.selected_kex' : 'diffie-hellman-group14-sha1',
   'extra.selected_mac' : 'hmac-sha1',
   'extra.server_cookie' : 'Z2fOfWsrLlh76Y0bOqa1cw==',
   'extra.server_host_key' : 'AAAAB3NzaC1yc2EAAAADAQABAAACAQDIVXBwKGhi35gabwHNZi6Bxls1BGtDVVZFhwvhTpJKTKhV4T2HnDFG7+FBpYejc92wH026Wf+uJHIpnKkVQRnnOV98zKXW68Tz+OnwT8aBQdLI+QYDC7wLwGRf+cOiXEAkpMrp2OJme+GwQ97oBccEwdu2j9vcYAFQ0+eCPNfwPrcZhwVb00kt/moLVSxWRdsDMzQiNDZf2zel+FQIAl5cCfaLSAQa1TIXy8SM13B0brnlpdyIqukQS0zUv/PL/6AsfhgLXeQBgjs1XIf6qL+ZdtQss5AKUDuJgrWDcS3nyNZQg/CAt8XdIsLntu3bCn+VGA1O/gUGLS1a9GoGd/lRArlmODNtbds74m7hxaAf/gzg0LFJx6HhwubmVCzTXEHl95KHYHKoDvCtUOgUm7zUugxWjhsLPfT6UfZCwvCY21SGVYsoEPiTT2DhuAFriM+PT83JresFHgZDosbqW0VCi2bzAKSBu/vphaqTbSdDo0xhkW9JCb3zUkW2ge/e/GrjxV4cNXRC9XQ/XYEIWmtF/gHSi0i9KweX4sN5TEkB/41vDvyDOdyPJ8Jta0I9vBolDwJ6qdMHOPlOW5oW83yCgbmUJNYkZ+MivABlc6iS/006qYiIwknHezbY5foYd8kDON7YAssOwCJcG5viII50Z1N9VsGkUv5sZMr2p9ry8Q==',
   'extra.server_host_key_sha256' : '06ff3cce443ed832927576d982b69d5a526d0e63334c72e87201deda61679406',
   'extra.server_signature_raw' : 'AAAAB3NzaC1yc2EAAAIAlrzL2DY9fVvwYg6CgB75uf2s8CLo+rL8Mp9tU1Ja3sDfBzj9QJjVDykupiy8s3usHfxMrHS2v3DhTiZjz/b5K6tVTgUBTXL94JfM4lwB+3EbLggPzKnlm1jQgnnU9c+tb7RX3IhBqU9Yj1gqxhErv9NFotgajQOOLgY0Ua5C0Ee+AIaMlLaNZe3LTejMsNUZMN5tl+sEmtutMHkGQsmjJxiJ3feF+Pys0I2+ojiiAfzqlMYar/5xOPl4Dj+HO+h91xVQ1/8nQRBc082fM7+ZJtDbRLtt4G8srlB5gew26jqfVASc/ui5gx4+BR9DG9VH8w+rJWBGfhOAaWqLFE2M3YuEWkjEmQMR1SQK1WFQ/oNiWJO2K5L3rk2LcAmyR6nQMtClVxYZ7CQOwa3uFL+JNXp9AhiiAtVaqhrEK81NJrJNh/+egTBl5STphxIShXd4KI9wyvkGlCIvNIMO94iXPVaWUXXbsGnU03+dsUkBzGf0eJ4DePInCk/RtunlSmOsjGld+rpS9g0VRxPrzbQRWuhpkgpV+CldyrI3C/rOxJRs2vSAKXocRsGwhqEKseAJzHXmiZ5ncsaGKoeB5lUkWLwcKjyok2tHVCDlzDUpE4aA/JHNEhT48det9RqtjC71yz8m0PeK2ySI/I+Qb7eBgevgduBmt+OUxgvfKi2UB6s=',
   'extra.server_signature_value' : 'lrzL2DY9fVvwYg6CgB75uf2s8CLo+rL8Mp9tU1Ja3sDfBzj9QJjVDykupiy8s3usHfxMrHS2v3DhTiZjz/b5K6tVTgUBTXL94JfM4lwB+3EbLggPzKnlm1jQgnnU9c+tb7RX3IhBqU9Yj1gqxhErv9NFotgajQOOLgY0Ua5C0Ee+AIaMlLaNZe3LTejMsNUZMN5tl+sEmtutMHkGQsmjJxiJ3feF+Pys0I2+ojiiAfzqlMYar/5xOPl4Dj+HO+h91xVQ1/8nQRBc082fM7+ZJtDbRLtt4G8srlB5gew26jqfVASc/ui5gx4+BR9DG9VH8w+rJWBGfhOAaWqLFE2M3YuEWkjEmQMR1SQK1WFQ/oNiWJO2K5L3rk2LcAmyR6nQMtClVxYZ7CQOwa3uFL+JNXp9AhiiAtVaqhrEK81NJrJNh/+egTBl5STphxIShXd4KI9wyvkGlCIvNIMO94iXPVaWUXXbsGnU03+dsUkBzGf0eJ4DePInCk/RtunlSmOsjGld+rpS9g0VRxPrzbQRWuhpkgpV+CldyrI3C/rOxJRs2vSAKXocRsGwhqEKseAJzHXmiZ5ncsaGKoeB5lUkWLwcKjyok2tHVCDlzDUpE4aA/JHNEhT48det9RqtjC71yz8m0PeK2ySI/I+Qb7eBgevgduBmt+OUxgvfKi2UB6s=',
   'extra.serverid_raw' : 'SSH-1.99-Cisco-1.25',
   'extra.serverid_software' : 'Cisco-1.25',
   'extra.serverid_version' : '1.99',
   'extra.source.naics' : 517311,
   'extra.tag' : 'ssh',
   'extra.userauth_methods' : 'publickey, keyboard-interactive, password',
   'feed.name' : 'Accessible SSH',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[3]])),
   'source.asn' : 33363,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'ORLANDO',
   'source.geolocation.region' : 'FLORIDA',
   'source.ip' : '72.17.0.0',
   'source.port' : 22,
   'source.reverse_dns' : '072-017-0-0.example.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T02:20:37+00:00'
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
