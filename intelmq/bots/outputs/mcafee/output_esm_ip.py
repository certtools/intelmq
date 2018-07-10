# -*- coding: utf-8 -*-
"""

ESMOutputBot connects to McAfee Enterprise Security Manager, and updates IP based watchlists

Parameters:
esm_ip: IP Address of ESM
esm_user: username to connect to ESM
esm_pw: Password of esm_user
esm_watchlist: Destination watchlist to update
field: field from intelMQ message to extract (e.g. destination.ip)

"""

from intelmq.lib.bot import Bot

try:
    from mfe_saw.esm import ESM
except ImportError:
    ESM = None


class ESMIPOutputBot(Bot):

    def init(self):
        if ESM is None:
            raise ValueError('Could not import mfe_saw. Please install it.')

        self.esm = ESM()
        try:
            self.esm.login(self.parameters.esm_ip, self.parameters.esm_user, self.parameters.esm_pw)
        except:
            self.logger.error('Could not Login to ESM.')
            self.stop()

        watchlist_filter = {'filters': [{'name': 'IPAddress', 'id': 0}]}
        try:
            retVal = self.esm.post('sysGetWatchlists?hidden=false&dynamic=false&writeOnly=false&indexedOnly=false',
                                   watchlist_filter)
            for WL in retVal:
                if (WL['name'] == self.parameters.esm_watchlist):
                    watchlist = {'watchlist': {'value': WL['id']}, 'values': '["' + event.get(self.parameters.field) + '"]'}
        except TypeError:
            self.logger.error('Watchlist not found. Please verify name of the watchlist.')
            self.stop()

    def process(self):
        event = self.receive_message()
        try:
            retVal = self.esm.post('sysAddWatchlistValues', self.watchlist, raw=True)
            self.logger.info('ESM Watchlist updated')
            self.acknowledge_message()
        except Exception:
            self.logger.exception('Error when updating watchlist.')


BOT = ESMIPOutputBot
