"""Configuration for IntelMQ Manager

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Herzog <bernhard.herzog@intevation.de>
"""

from typing import List, Optional
import json
from pathlib import Path


class Config:

    """Configuration settings for IntelMQ Manager"""

    intelmq_ctl_cmd: List[str] = ["sudo", "-u", "intelmq",
                                  "/usr/local/bin/intelmqctl"]

    allowed_path: Path = Path("/opt/intelmq/var/lib/bots/")

    session_store: Optional[Path] = None

    session_duration: int = 24 * 3600

    allow_origins: List[str] = ['*']

    def __init__(self, filename: Optional[str]):
        """Load configuration from JSON file"""
        raw = {}
        config = False

        configfiles = [
            Path('/etc/intelmq/api-config.json'),
            Path(__file__).parent.parent / 'etc/intelmq/api-config.json'
        ]

        if filename:
            configfiles.insert(0, Path(filename).resolve())

        for path in configfiles:
            if path.exists() and path.is_file():
                print(f"Loading config from {path}")
                config = True
                with path.open() as f:
                    try:
                        raw = json.load(f)
                    except json.decoder.JSONDecodeError:
                        print(f"{path} did not contain valid JSON. Using default values.")
                break
        if not config:
            print("Was not able to load a configfile. Using default values.")

        if "intelmq_ctl_cmd" in raw:
            self.intelmq_ctl_cmd = raw["intelmq_ctl_cmd"]

        if "allowed_path" in raw:
            self.allowed_path = Path(raw["allowed_path"])

        if "session_store" in raw:
            self.session_store = Path(raw["session_store"])

        if "session_duration" in raw:
            self.session_duration = int(raw["session_duration"])

        if "allow_origins" in raw:
            self.allow_origins = raw['allow_origins']
