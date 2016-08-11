# -*- coding: utf-8 -*-
"""
Squelcher Expert marks events as new or old depending on a TTL(ASN, Net, IP).
"""
from __future__ import unicode_literals
from ipaddress import ip_address, ip_network
import psycopg2
import sys

from intelmq.lib.bot import Bot
from intelmq.lib.utils import load_configuration


SELECT_QUERY = '''
SELECT COUNT(*) FROM {table}
WHERE
"time.source" + INTERVAL '%s SECONDS' > LOCALTIMESTAMP AND
"classification.type" = %s AND
"classification.identifier" = %s AND
"source.ip" = %s AND
notify IS TRUE
'''


class SquelcherExpertBot(Bot):

    def init(self):
        self.config = load_configuration(self.parameters.configuration_path)

        self.logger.debug("Connecting to PostgreSQL.")
        try:
            if hasattr(self.parameters, 'connect_timeout'):
                connect_timeout = self.parameters.connect_timeout
            else:
                connect_timeout = 5

            self.con = psycopg2.connect(database=self.parameters.database,
                                        user=self.parameters.user,
                                        password=self.parameters.password,
                                        host=self.parameters.host,
                                        port=self.parameters.port,
                                        sslmode=self.parameters.sslmode,
                                        connect_timeout=connect_timeout,
                                        )
            self.cur = self.con.cursor()
            global SELECT_QUERY
            SELECT_QUERY = SELECT_QUERY.format(table=self.parameters.table)
        except:
            self.logger.exception('Failed to connect to database.')
            self.stop()
        self.logger.info("Connected to PostgreSQL.")

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        if 'source.ip' not in event and 'source.fqdn' in event:
            event.add('notify', True, force=True)
            self.modify_end(event)
            return
        if 'source.asn' not in event:
            event.add('notify', False, force=True)
            self.modify_end(event)
            return

        ttl = None
        for ruleset in self.config:
            condition = ruleset[0].copy()
            in_net = True
            if 'source.network' in condition and 'source.ip' in event:
                in_net = (ip_address(event['source.ip']) in
                          ip_network(condition['source.network']))
                del condition['source.network']
            if set(condition.items()).issubset(event.items()) and in_net:
                ttl = ruleset[1]['ttl']
                break

        self.logger.debug('Found TTL {} for ({}, {}).'
                          ''.format(ttl, event['source.asn'],
                                    event['source.ip']))

        try:
            self.cur.execute(SELECT_QUERY, (ttl, event['classification.type'],
                                            event['classification.identifier'],
                                            event['source.ip']))
        except (psycopg2.InterfaceError, psycopg2.InternalError,
                psycopg2.OperationalError, AttributeError):
            self.logger.exception('Cursor has been closed, connecting again.')
            self.init()
        else:
            result = self.cur.fetchone()[0]
            if result == 0:
                notify = True
            else:
                notify = False

            event.add('notify', notify, force=True)
            self.modify_end(event)

    def stop(self):
        try:
            self.cur.close()
        except:
            pass
        try:
            self.con.close()
        except:
            pass
        super(SquelcherExpertBot, self).stop()

    def modify_end(self, event):
        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = SquelcherExpertBot(sys.argv[1])
    bot.start()
