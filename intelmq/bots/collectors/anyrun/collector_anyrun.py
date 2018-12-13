# -*- coding: utf-8 -*-
from intelmq.lib.bot import CollectorBot
from requests import get


class AnyrunCollectorBot(CollectorBot):
    def init(self):
        self.anyrun_url = "https://any.run/report/"
        self.last_ioc_url = None

    def process(self):
        urls = []
        res = get(self.anyrun_url)
        if res.status_code // 100 != 2:
            raise ValueError('HTTP response status code was %i.' % resp.status_code)

        if not self.last_ioc_url:
            lines = res.text.splitlines()
            for i in range(len(lines)):
                if lines[i].lstrip() == "<div class=\"td hash\">":
                    urls.append(lines[i+1].split("\"")[1])
                if len(urls) == 10:
                    break
        else:
            lines = res.text.split(self.last_ioc_url)[0].splitlines()[:-2]
            for i in range(len(lines)):
                line = lines[i].lstrip()
                if line == "<div class=\"td hash\">":
                    urls.append(lines[i+1].split("\"")[1])

        if urls:
            self.last_ioc_url = urls[0]
            for url in urls:
                res = get(url)
                if res.status_code // 100 != 2:
                    raise ValueError('HTTP response status code was %i.' % resp.status_code)
                report = self.new_report()
                report.add("raw", res.text)
                report.add("feed.url", url)
                self.send_message(report)


BOT = AnyrunCollectorBot

