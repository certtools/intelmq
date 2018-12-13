from html.parser import HTMLParser
from intelmq.lib.bot import ParserBot
from intelmq.lib import utils


class MyHTMLParser(HTMLParser):

    Data = ""
    EndTag = ""
    StartTag = ""

    def handle_data(self, data):
        self.Data = data

    def handle_endtag(self, tag):
        self.EndTag = tag

    def handle_starttag(self, tag, attrs):
        self.StartTag = tag

    def feed(self, text):
        self.Data = ""
        self.EndTag = ""
        self.StartTag = ""
        super().feed(text)


parser = MyHTMLParser()


class AnyrunParserBot(ParserBot):
    def init(self):
        self.accuracy = {"malicious": 80, "suspicious": 60, "unknown": 50}

    def process(self):
        report = self.receive_message()
        lines = utils.base64_decode(report["raw"]).splitlines()
        for x in range(len(lines)):
            parser.feed(lines[x])
            if parser.Data == "Verdict":
                break
        parser.feed(lines[x+2])
        if parser.Data == "Malicious activity":
            while parser.EndTag != "div":
                x += 1
                parser.feed(lines[x])
                if parser.Data == "Tags:":
                    tags = []
                    while parser.EndTag != "dd":
                        x += 1
                        parser.feed(lines[x])
                        tags.append(parser.Data)
            while (parser.Data, parser.EndTag) != ("DNS requests", "h4"):
                x += 1
                try:
                    parser.feed(lines[x])
                except IndexError:
                    self.acknowledge_message()
                    return 
            while parser.EndTag != "div":
                x += 1
                parser.feed(lines[x])
                if (parser.StartTag, parser.EndTag) == ("td", "td"):
                    domain = parser.Data
                    raw_start_index = x
                    while parser.StartTag != "span":
                        x += 1
                        parser.feed(lines[x])
                    status = lines[x+1].lstrip()
                    if status in self.accuracy:
                        event = self.new_event(report)
                        event.add("source.fqdn", domain)
                        event.add("feed.accuracy", self.accuracy[status])
                        event.add("raw", "".join(lines[raw_start_index: x+2]))
                        try:
                            event.add("classification.identifier", ", ".join(tags[1:-1]))
                        except UnboundLocalError:
                            pass
                        event.add("classification.type", "malware")
                        self.send_message(event)
        self.acknowledge_message()


BOT = AnyrunParserBot

