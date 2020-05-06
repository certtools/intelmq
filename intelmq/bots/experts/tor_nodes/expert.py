# -*- coding: utf-8 -*-
"""
See README for database download.
"""
import re
import sys
import pathlib
import requests
import subprocess

from intelmq.lib.bot import Bot
from intelmq import RUNTIME_CONF_FILE
from intelmq.lib.utils import load_configuration


class TorExpertBot(Bot):

    database = set()

    def init(self):
        self.logger.info("Loading TOR exit node IPs.")

        try:
            with open(self.parameters.database) as fp:
                for line in fp:
                    line = line.strip()

                    if len(line) == 0 or line[0] == "#":
                        continue

                    self.database.add(line)

        except IOError:
            raise ValueError("TOR rule not defined or failed on open.")

        self.overwrite = getattr(self.parameters, 'overwrite', False)

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:
            if key + 'ip' in event:
                if key + 'tor_node' not in event:
                    if event.get(key + 'ip') in self.database:
                        event.add(key + 'tor_node', True)
                elif key + 'tor_node' in event and self.overwrite:
                    if event.get(key + 'ip') in self.database:
                        event.change(key + 'tor_node', True)

        self.send_message(event)
        self.acknowledge_message()

    @classmethod
    def run(cls):
        if len(sys.argv) > 1 and sys.argv[1] == "--update-database":
            cls.update_database()
        else:
            super(TorExpertBot, TorExpertBot).run()

    @classmethod
    def update_database(cls):
        bots = {}
        runtime_conf = load_configuration(RUNTIME_CONF_FILE)
        try:
            for bot in runtime_conf:
                if runtime_conf[bot]["module"] == __name__:
                    bots[bot] = runtime_conf[bot]["parameters"]["database"]

        except KeyError as e:
            print(f"Your configuration of {bot} is missing key {e}.")
            exit(1)

        if not bots:
            print(f"No bots of type {__name__} present in runtime.conf.")
            exit(0)

        try:
            response = requests.get("https://check.torproject.org/exit-addresses")
        except requests.exceptions.RequestException as e:
            print(f"Connection Error: {e}")
            exit(1)

        ipv4_re = re.compile("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)")
        tor_exits = "\n".join(ipv4_re.findall(response.text))

        for database_path in set(bots.values()):
            database_dir = pathlib.Path(database_path).parent
            database_dir.mkdir(parents=True, exist_ok=True)
            with open(database_path, "w") as database:
                database.write(tor_exits)

        command = ["intelmqctl", "reload"] + list(bots.keys())

        subprocess.run(command)


BOT = TorExpertBot
