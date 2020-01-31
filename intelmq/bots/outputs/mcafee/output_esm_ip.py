# -*- coding: utf-8 -*-
"""
ESMOutputBot connects to McAfee Enterprise Security Manager, and updates IP based watchlists

Parameters:
esm_ip: IP Address of ESM
esm_user: username to connect to ESM
esm_password: Password of esm_user
esm_watchlist: Destination watchlist to update
field: field from IntelMQ message to extract (e.g. destination.ip)

"""

from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError

try:
    from mfe_saw.esm import ESM
except ImportError:
    ESM = None


class ESMIPOutputBot(Bot):

    def init(self):
        if ESM is None:
            raise MissingDependencyError("mfe_saw")

        self.esm = ESM()
        try:
            self.esm.login(self.parameters.esm_ip, self.parameters.esm_user, self.parameters.esm_password)
        except Exception:
            raise ValueError('Could not Login to ESM.')

        watchlist_filter = {'filters': [{'name': 'IPAddress', 'id': 0}]}
        self.watchlist_id = None
        try:
            retVal = self.esm.post('sysGetWatchlists?hidden=false&dynamic=false&writeOnly=false&indexedOnly=false',
                                   watchlist_filter)
            for WL in retVal:
                if (WL['name'] == self.parameters.esm_watchlist):
                    self.watchlist_id = WL['id']
        except TypeError:
            self.logger.error('Watchlist not found. Please verify name of the watchlist.')
            self.stop()

    def process(self):
        event = self.receive_message()
        self.logger.info('Message received.')
        try:
            self.esm.post('sysAddWatchlistValues', {'watchlist': {'value': self.watchlist_id},
                                                    'values': '["' + event.get(self.parameters.field) + '"]'},
                          raw=True)
            self.logger.info('ESM Watchlist updated')
            self.acknowledge_message()
        except Exception:
            self.logger.exception('Error when updating watchlist.')
        self.acknowledge_message()


BOT = ESMIPOutputBot
