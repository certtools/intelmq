# -*- coding: utf-8 -*-
"""
Squelcher Expert marks events as new or old depending on a TTL(ASN, Net, IP).
"""
from __future__ import unicode_literals
from ipaddress import ip_address, ip_network
import psycopg2

from intelmq import SQUELCHER_CONF_FILE
from intelmq.lib.bot import Bot
import intelmq.lib.utils


SELECT_QUERY = '''
SELECT COUNT(*) FROM {table}
WHERE
"time.source" + INTERVAL '%s HOURS' > LOCALTIMESTAMP AND
"classification.type" = %s AND
"classification.identifier" = %s AND
"source.ip" = %s AND
notify IS TRUE
'''


class SquelcherExpertBot(Bot):

    def init(self):
        self.config = intelmq.lib.utils.load_configuration(SQUELCHER_CONF_FILE)

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

        self.logger.debug(event.keys())
        ev_type = event['classification.type']
        ev_ident = event['classification.identifier']
        ev_asn = event['source.asn']
        ev_address = event['source.ip']

        # get AS section -> net_section
        # json keys can't be integer, so use strings
        if str(ev_asn) in self.config:
            net_section = self.config[str(ev_asn)]
        elif '*' in self.config:
            net_section = self.config['*']
        else:
            self.logger.debug('No TTL found for ({}).'.format(ev_asn))
            self.modify_end(event)
            return

        # get network section -> ip_section
        ip_section = None
        for net_key, net_value in net_section.items():
            if net_key == '*':
                continue
            if ip_address(ev_address) in ip_network(net_key):
                ip_section = net_section[net_key]
        if ip_section is None and '*' in net_section:
            ip_section = net_section['*']
        elif ip_section is None:
            self.logger.debug('No TTL found for ({}, {}).'.format(ev_asn,
                                                                  ev_address))
            self.modify_end(event)
            return

        # get ip address -> ttl
        if ev_address in ip_section:
            ttl = ip_section[ev_address]
        elif '*' in ip_section:
            ttl = ip_section['*']
        else:
            self.logger.debug('No TTL found for ({}, {}).'.format(ev_asn,
                                                                  ev_address))
            self.modify_end(event)
            return
        print('Found TTL {} for ({}, {}).'
                          ''.format(ttl, ev_asn, ev_address))

        self.cur.execute(SELECT_QUERY, (ttl, ev_type, ev_ident, ev_address))
        result = self.cur.fetchone()[0]
        if result == 0:
            notify = True
        else:
            notify = False
        print('Result {}.'.format(result))

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
