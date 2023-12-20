"""Control IntelMQ with the intelmqctl command.

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Herzog <bernhard.herzog@intevation.de>

This module contains code to run the intelmqctl command as needed by the
manager's API backend.
"""

import io
import json
import subprocess
from typing import List, Dict, Optional

from intelmq_api.util import shell_command_for_errors
from .version import __version__

#
# Typing aliases for use with RunIntelMQCtl
#
# Arguments for a subprocess command line are a list of strings.
Args = List[str]

# JSON output of intelmqctl is returned as bytes and then simply
# passed to the response without (de)serialization. Type alias
# for clear understanding of expected format and content type
JSONFile = bytes


class IntelMQCtlError(Exception):

    def __init__(self, error_dict):
        self.error_dict = error_dict

    def __str__(self):
        return self.error_dict["message"]


failure_tips = [
    ("sudo: no tty present and no askpass program specified",
     "Is sudoers file or IntelMQ-Manager "
     "<a href='https://github.com/certtools/intelmq-manager/"
     "blob/master/docs/INSTALL.md#allow-access-to-intelmqctl'>set up correctly</a>?"),
    ("Permission denied: '/opt/intelmq",
     "Has the user accessing intelmq folder the read/write permissions?"
     " This might be user intelmq or www-data, depending on your configuration,"
     " ex: <code>sudo chown intelmq.intelmq /opt/intelmq -R"
     " && sudo chmod u+rw /opt/intelmq -R</code>"),
    ("sqlite3.OperationalError: no such table",
     "SQLite database may not have been"
     " <a href='https://github.com/certtools/intelmq/blob/develop/docs/Bots.md#sqlite'>initialized</a>.")  # noqa
]


class RunIntelMQCtl:

    def __init__(self, base_cmd: Args):
        self.base_cmd = base_cmd

    def _run_intelmq_ctl(self, args: Args) -> subprocess.CompletedProcess:
        command = self.base_cmd + args
        result = subprocess.run(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        # Detect errors
        #
        # The logic here follows the original PHP code but it differs in
        # some respects. One difference is that intelmqctl can exit with
        # an exit code != 0 even if it actually was successful, so we
        # cannot actually use the exit code. The PHP code appears to use
        # it, but the exit code it examines is not the exit code of
        # intelmqctl but of a little shell script that basically ends up
        # ignoring intelmqctl's exit code.
        if not result.stdout or result.stderr:
            message = str(result.stderr, errors="replace")

            if not message:
                message = "Failed to execute intelmqctl."

            for msg_fragment, tip in failure_tips:
                if msg_fragment in message:
                    break
            else:
                tip = ""

            raise IntelMQCtlError({"tip": tip,
                                   "message": message,
                                   "command": shell_command_for_errors(command),
                                   })
        return result

    def _run_json(self, args: Args) -> JSONFile:
        completed = self._run_intelmq_ctl(["--type", "json"] + args)
        return completed.stdout

    def _run_str(self, args: Args) -> str:
        completed = self._run_intelmq_ctl(args)
        return str(completed.stdout, "ascii")

    def botnet(self, action: str, group: Optional[str]) -> JSONFile:
        args = [action]
        if group is not None and group != "botnet":
            args.extend(["--group", group])
        return self._run_json(args)

    def bot(self, action: str, bot_id: str) -> JSONFile:
        return self._run_json([action, bot_id])

    def log(self, bot_id: str, lines: int, level: str) -> JSONFile:
        if level == "ALL":
            level = "DEBUG"
        return self._run_json(["log", bot_id, str(lines), level])

    def list(self, kind: str) -> JSONFile:
        return self._run_json(["list", kind])

    def version(self) -> Dict[str, str]:
        intelmq_version = self._run_str(["--version"]).strip()
        return {"intelmq": intelmq_version,
                "intelmq-api": __version__,
                }

    def check(self) -> JSONFile:
        return self._run_json(["check"])

    def clear(self, queue_name: str) -> JSONFile:
        return self._run_json(["clear", queue_name])

    def run(self, bot_id: str, cmd: str, show: bool, dry: bool,
            msg: str) -> str:
        args = ["run", bot_id]
        if cmd == "get":
            args.extend(["message", "get"])
        elif cmd == "pop":
            args.extend(["message", "pop"])
        elif cmd == "send":
            args.extend(["message", "send", msg])
        elif cmd == "process":
            args.append("process")
            if show:
                args.append("--show-sent")
            if dry:
                args.append("--dry")
            args.extend(["--msg", msg])
        return self._run_str(args)

    def debug(self, get_paths: bool = False) -> JSONFile:
        args = ["debug"]
        if get_paths:
            args.append("--get-paths")
        return self._run_json(args)

    def get_paths(self) -> Dict[str, str]:
        return dict(json.load(io.BytesIO(self.debug(get_paths=True)))["paths"])
