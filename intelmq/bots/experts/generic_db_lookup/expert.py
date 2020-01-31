# -*- coding: utf-8 -*-
"""
Generic DB Lookup
"""

from intelmq.lib.bot import SQLBot


class GenericDBLookupExpertBot(SQLBot):

    def init(self):
        super().init()

        self.replace = self.parameters.replace_fields
        self.match = self.parameters.match_fields
        query = 'SELECT "{replace}" FROM "{table}" WHERE ' + 'AND '.join(['"{}" = ' + self.format_char + ' '] * len(self.match))
        self.query = query.format(*self.match.values(),
                                  table=self.parameters.table,
                                  replace='", "'.join(self.replace.keys()))

    def process(self):
        event = self.receive_message()

        # Skip events with missing match-keys
        for key in self.match.keys():
            if key not in event:
                self.logger.debug('%s not present in event. Skipping event.', key)
                self.send_message(event)
                self.acknowledge_message()
                return

        # Skip events with existing data and overwrite is not allowed
        if all([key in event for key in self.replace.values()]) and not self.parameters.overwrite:
            self.send_message(event)
            self.acknowledge_message()
            return

        if self.execute(self.query, [event[key] for key in self.match.keys()]):
            if self.cur.rowcount > 1:
                raise ValueError('Lookup returned more then one result. Please inspect.')
            elif self.cur.rowcount == 1 or (self.cur.rowcount == -1 and self.parameters.engine == SQLBot.SQLITE):
                result = None
                if self.cur.rowcount == 1:
                    result = self.cur.fetchone()
                elif self.cur.rowcount == -1 and self.parameters.engine == SQLBot.SQLITE:
                    # https://docs.python.org/2/library/sqlite3.html#sqlite3.Cursor.rowcount
                    # since the DB’s own support for the determination is quirky we try to fetch even when rowcount=-1
                    result = self.cur.fetchone()

                if result:
                    for i, (key, value) in enumerate(self.replace.items()):
                        event.add(value, result[i], overwrite=True)
                    self.logger.debug('Applied.')
                else:
                    self.logger.debug('No row found.')

            self.send_message(event)
            self.acknowledge_message()


BOT = GenericDBLookupExpertBot
