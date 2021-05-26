# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil import parser
from intelmq.lib.utils import get_timedelta
from intelmq.lib.bot import Bot
from datetime import timezone


class TimeFilterExpertBot(Bot):
    search_field: str = 'time.source'
    search_from: str  = '1d'

    not_after = None

    def init(self):
        self.search_field = self.search_field
        if self.search_from:
            timedelta_params = get_timedelta(self.search_from)
            self.not_after = datetime.now(tz=timezone.utc) - timedelta(**timedelta_params)

    def process(self):
        event = self.receive_message()
        # time based filtering
        if self.search_field in event:
            try:
                event_time = parser.parse(str(event.get(self.search_field)))
            except ValueError:
                event_time = self.not_after
                self.process_message(event_time, event)
                return
            else:
                self.process_message(event_time, event)
                return
        else:
            # not found field
            event_time = self.not_after
            self.process_message(event_time, event)
            return

    def process_message(self, event_time, event):
        event_time = event_time.replace(tzinfo=None)
        self.not_after = self.not_after.replace(tzinfo=None)

        if event_time < self.not_after:
            self.acknowledge_message()
            self.logger.debug(
                f"Filtered out event with search field {self.search_field} and event time {event_time} .")
            return
        else:
            self.send_message(event)
            self.acknowledge_message()
            return


BOT = TimeFilterExpertBot
