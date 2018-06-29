# -*- coding: utf-8 -*-
"""

ESMOutputBot connects to McAfee Enterprise Security Manager, and updates Destination IP based watchlists

Parameters:
esm_ip: IP Address of ESM
esm_user: username to connect to ESM
esm_pw: Password of esm_user
esm_watchlist: Destination watchlist to update

"""

from intelmq.lib.bot import Bot

import json

try:
    from mfe_saw.esm import ESM
except ImportError:
    ESM = None


class ESMIPOutputBot(Bot):

    def init(self):
        if ESM is None:
            self.logger.error('Could not import mfe_saw. Please install it.')
            self.stop()

        esm = ESM()
        esm.login(self.parameters.esm_ip, self.parameters.esm_user, self.parameters.esm_pw)
        # print(esm.time())
        # retVal = esm.post('sysGetWatchlistFields')
        # print(json.dumps(retVal, indent=4))
        watchlist = {'filters': [{'name': 'IPAddress', 'id': 0}]}
        print (json.dumps(watchlist, indent=4, sort_keys=True))
        retVal = esm.post('sysGetWatchlists?hidden=false&dynamic=false&writeOnly=false&indexedOnly=false', watchlist)
        for WL in retVal:
            print('Next watchlist:')
            if (WL['name'] == 'TIE Data Source IPs'):
                watchlist = {'watchlist': {'value': WL['id']}, 'values': ['1.2.3.4']}
                print(json.dumps(watchlist, indent=4))
                retVal=esm.post('sysAddWatchlistValues', watchlist, raw=True)

    def process(self):
        event = self.receive_message()


BOT = ESMIPOutputBot
