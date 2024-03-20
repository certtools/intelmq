"""Configuration for IntelMQ server application

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>, 2023 Filip Pokorný
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Herzog <bernhard.herzog@intevation.de>
"""

from typing import List, Optional, Union
from pathlib import Path
from intelmq.lib import utils

from intelmq import VAR_STATE_PATH, DEFAULT_LOGGING_PATH


class Config:

    """Configuration settings for IntelMQ Manager"""

    intelmq_ctl_cmd: List[str] = ["intelmqctl"]

    allowed_path: Path = Path(VAR_STATE_PATH)

    session_store: Optional[Path] = None

    access_log: Optional[Union[Path,str]] = Path(DEFAULT_LOGGING_PATH) / "access.log"

    session_duration: int = 24 * 3600

    allow_origins: List[str] = ['*']

    enable_webgui: bool = True

    workers: int = 2

    host: str = "0.0.0.0"

    port: int = 8080

    debug: bool = False

    def __init__(self):
        server_settings = utils.get_server_settings()

        if "intelmq_ctl_cmd" in server_settings:
            self.intelmq_ctl_cmd = server_settings["intelmq_ctl_cmd"]

        if "allowed_path" in server_settings:
            self.allowed_path = Path(server_settings["allowed_path"])

        if "session_store" in server_settings:
            self.session_store = Path(server_settings["session_store"])

        if "access_log" in server_settings:
            if server_settings["access_log"] == "-":
                self.access_log = server_settings["access_log"]
            else:
                self.access_log = Path(server_settings["access_log"])

        if "session_duration" in server_settings:
            self.session_duration = int(server_settings["session_duration"])

        if "allow_origins" in server_settings:
            self.allow_origins = server_settings['allow_origins']

        if "enable_webgui" in server_settings:
            self.enable_webgui = server_settings["enable_webgui"]

        if "workers" in server_settings:
            self.workers = server_settings["workers"]

        if "host" in server_settings:
            self.host = server_settings["host"]

        if "port" in server_settings:
            self.port = server_settings["port"]

        if "debug" in server_settings:
            self.debug = server_settings["debug"]
