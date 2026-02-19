from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Annotated, Literal, Optional, TypeVar

from mininterface.cli import Positional
from tyro.conf import (DisallowNone, FlagCreatePairsOff,
                       OmitSubcommandPrefixes, arg)

from intelmq import STATE_FILE_PATH
from intelmq.lib.datatypes import LogLevel

if TYPE_CHECKING:
    from ..bin.intelmqctl import IntelMQController

from typing import Any, Callable, Type

from .datatypes import ReturnType

if TYPE_CHECKING:
    BotId = str
    GroupType = str
    UpgradeType = str


# Instead of refactoring IntelMQController code (for backwards compatibility for the case someone uses it as a library),
# we need this handler to control IntelMQController methods.

T = TypeVar("T", bound=Type)
_registry: dict[Type, Callable] = {}


def with_handler(handler: Callable):
    """Decorator to register a callback to a dataclass."""

    def wrapper(cls: T) -> T:
        _registry[cls] = handler
        return cls

    return wrapper


def run_handler(obj: Any):
    """Run callback registered with `with_handler`."""
    cls = type(obj)
    if cls not in _registry:
        raise ValueError(f"No handler registered for {cls}")
    return _registry[cls](**asdict(obj))


# Args arguments

def get_parser(ic: "IntelMQController", bot_ids, group_keys, upgrades):

    if not TYPE_CHECKING:
        BotId = Literal[tuple(bot_ids)]
        GroupType = Literal[tuple(group_keys)]
        UpgradeType = Literal[tuple(upgrades)]

    # Helper dataclasses

    @dataclass
    class Botted:
        bot_id: BotId

    @dataclass
    class Grouped(Botted):
        bot_id: Positional[Optional[BotId]] = None
        group: Optional[GroupType] = None
        "group of bots"

    # Subcommands

    @dataclass
    @with_handler(ic.list)
    class List:
        "Listing bots or queues"

        kind: Literal["bots", "queues", "queues-and-status"]
        non_zero: Annotated[bool, arg(aliases=["-q", "--quiet"])] = False
        "Only list non-empty queues or the IDs of enabled bots."
        count: Annotated[bool, arg(aliases=["-s", "--sum"])] = False
        "Only show the total number of messages in queues. Only valid for listing queues."
        configured: Annotated[bool, arg(aliases=["-c"])] = False
        "Only show configured bots"

    @dataclass
    @with_handler(ic.clear_queue)
    class Clear:
        "Clear a queue"

        queue: str
        "queue name"

    @dataclass
    @with_handler(ic.read_bot_log)
    class Log:
        "Get last log lines of a bot"

        bot_id: BotId
        number_of_lines: int = 10
        "number of lines"
        log_level: Annotated[LogLevel, arg(aliases=["-l"])] = LogLevel.INFO

    @dataclass
    class Console:
        "Get a ipdb live console."

        console_type: Optional[str] = None
        """You may specify which console should be run. Default is ipdb (if installed)
         or pudb (if installed) or pdb but you may want to use another one."""

    @dataclass
    class Message:
        """Debug bot's pipelines. Get the message in the
         input pipeline, pop it (cut it) and display it, or
         send the message directly to bot's output pipeline(s)."""

        message_action_kind: Literal["get", "pop", "send"]
        """get: show the next message in the source pipeline.
        pop: show and delete the next message in the source pipeline
        send: Send the given message to the destination pipeline(s)."""

        msg: Optional[str] = None
        "If send was chosen, put here the message in JSON."

    @dataclass
    class Process:
        """Single run of bot's process() method."""

        show_sent: Annotated[bool, arg(aliases=["-s"])] = False
        "If message is sent through, displays it."
        dryrun: Annotated[bool, arg(aliases=["-d"])] = False
        """Never really pop the message from the input pipeline
        nor send to output pipeline."""
        msg: Annotated[Optional[str], arg(aliases=["-m"])] = None
        """Trick the bot to process this JSON
        instead of the Message in its pipeline."""

    @dataclass
    @with_handler(ic.bot_run)
    class Run:
        """Run a bot interactively"""

        subcommand: Console | Message | Process

        bot_id: BotId
        loglevel: LogLevel | None = None

    @dataclass
    @with_handler(ic.check)
    class Check:
        "Check installation and configuration"

        quiet: Annotated[bool, arg(aliases=["-q"])] = False
        "Only print warnings and errors."
        no_connections: Annotated[bool, arg(aliases=["-C"])] = False
        "Do not test the connections to services like redis."

    @dataclass
    @with_handler(ic.bot_start)
    class Start(Grouped):
        "Start a bot or a botnet"

        pass

    @dataclass
    @with_handler(ic.bot_stop)
    class Stop(Grouped):
        "Stop a bot or a botnet"

        pass

    @dataclass
    @with_handler(ic.bot_restart)
    class Restart(Grouped):
        "Restart a bot or a botnet"

        pass

    @dataclass
    @with_handler(ic.bot_reload)
    class Reload(Grouped):
        "Reload a bot or a botnet"

        pass

    @dataclass
    @with_handler(ic.bot_status)
    class Status(Grouped):
        "Get status of a bot or a botnet"

        pass

    @dataclass
    @with_handler(ic.bot_enable)
    class Enable(Botted):
        "Enable a bot"

        pass

    @dataclass
    @with_handler(ic.bot_disable)
    class Disable(Botted):
        "Disable a bot"

        pass

    @dataclass
    @with_handler(ic.upgrade_conf)
    class UpgradeConfig:
        "Upgrade IntelMQ configuration to a newer version."

        previous: Annotated[Optional[str], arg(aliases=["-p"])] = None
        "Use this version as the previous one."
        dry_run: Annotated[bool, arg(aliases=["-d"])] = False
        "Do not write any files."
        function: Annotated[Optional[UpgradeType], arg(aliases=["-u"])] = None
        "Run this upgrade function."
        force: Annotated[bool, arg(aliases=["-f", "--force"])] = False
        "Force running the upgrade procedure."
        state_file: str = STATE_FILE_PATH
        "The state file location to use."
        no_backup: bool = False
        "Do not create backups of state and configuration files."

    # Just a helper function to adapt to `ic.debug`. I recommend refactor `ic.debug` to get rid of this.
    def debug_adapt(get_paths, get_environment_variables):
        sections = [
            name
            for cond, name in (
                (get_paths, "paths"),
                (get_environment_variables, "environment_variables"),
            )
            if cond
        ]
        if not sections:
            sections = None
        return ic.debug(sections)

    @dataclass
    @with_handler(debug_adapt)
    class Debug:
        "Get debugging output."

        get_paths: bool = False
        "Give all paths."

        get_environment_variables: bool = False
        "Give environment variables."

    # Top-level subcommands
    @dataclass
    class Env:
        command: Annotated[
            List
            | Clear
            | Log
            | Run
            | Check
            | Start
            | Stop
            | Restart
            | Reload
            | Status
            | Enable
            | Disable
            | UpgradeConfig
            | Debug,
            FlagCreatePairsOff,
            OmitSubcommandPrefixes,
            DisallowNone,
        ]

        type: ReturnType = ReturnType.TEXT
        """choose if it should return regular text or other machine-readable"""
        quiet: Annotated[bool, arg(aliases=["-q"])] = False
        """Quiet mode, useful for reloads initiated scripts like logrotate"""

    return Env
