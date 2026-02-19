from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from intelmq import STATE_FILE_PATH

@dataclass
class SetupConfig:
    "Set's up directories and example configurations for IntelMQ."

    skip_ownership: bool = False
    "Skip setting file ownership."

    state_file: Path = Path(STATE_FILE_PATH)
    "The state file location to use."

    webserver_user: Optional[str] = None
    "The webserver to use instead of auto-detection."

    webserver_configuration_directory: Optional[str] = None
    "The webserver configuration directory to use instead of auto-detection."

    skip_api: bool = False
    "Skip set-up of intelmq-api."

    skip_webserver: bool = False
    "Skip all operations on the webserver configuration, affects the API and Manager."

    skip_manager: bool = False
    "Skip set-up of intelmq-manager."
