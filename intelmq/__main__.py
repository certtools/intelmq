# SPDX-FileCopyrightText: 2023 Filip Pokorný
# SPDX-License-Identifier: AGPL-3.0-or-later

import argparse
import getpass
import sys

from intelmq import __version__
from intelmq.app.api.session import SessionStore
from intelmq.app.server import run
from intelmq.bin.intelmqctl import IntelMQController, ReturnType
from intelmq.app.config import Config

ARGPARSER_EPILOG = """\
Run 'intelmq COMMAND --help' for more information on a command.

For more help on how to use IntelMQ, head to https://docs.intelmq.org/
"""


def print_version(*args, **kwargs):
    print(__version__)


def server_start(host: str = None, port: int = None, debug: bool = None, no_check: bool = False, *args, **kwargs):

    if not no_check and IntelMQController(no_file_logging=True).check()[0]:
        return 1

    return run(
        host=host,
        port=port,
        debug=debug
    )


def server_adduser(username: str, password: str = None, *args, **kwargs):
    config = Config()

    if config.session_store is None:
        sys.exit("Could not add user - no session store configured in configuration!")

    session_store = SessionStore(str(config.session_store), config.session_duration)
    password = getpass.getpass() if password is None else password
    session_store.add_user(username, password)
    print(f"Added user {username} to intelmq session file.")


def intelmq_api_adduser():
    """
    Backwards compatibility for 'intelmq-api-adduser' script.
    """
    if sys.argv[0].endswith("intelmq-api-adduser"):
        sys.argv[0] = "intelmq"
        sys.argv.insert(1, "server")
        sys.argv.insert(2, "adduser")
        main()


def main():
    parser = argparse.ArgumentParser(prog="intelmq", usage="intelmq [OPTIONS] COMMAND", epilog=ARGPARSER_EPILOG,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.set_defaults(func=(lambda *_, **__: parser.print_help()))  # wrapper to accept args and kwargs
    parser._optionals.title = "Options"
    parser.add_argument("-v", "--version", action="store_true", help="print version and exit", default=None)
    commands = parser.add_subparsers(metavar="", title="Commands")

    # intelmq server
    srv_parser = commands.add_parser("server", help="control IntelMQ server", usage="intelmq server [COMMAND]")
    srv_parser.set_defaults(func=(lambda *_, **__: srv_parser.print_help()))  # wrapper to accept args and kwargs
    srv_parser._optionals.title = "Options"
    srv_subcommands = srv_parser.add_subparsers(metavar="", title="Commands")

    # intelmq server start
    srv_start = srv_subcommands.add_parser("start", help="start the server", usage="intelmq server start [OPTIONS]")
    srv_start.set_defaults(func=server_start)
    srv_start._optionals.title = "Options"
    srv_start.add_argument("--debug", action="store_true", dest="debug", default=None)
    srv_start.add_argument("--host", type=str, dest="host")
    srv_start.add_argument("--port", type=int, dest="port")
    srv_start.add_argument("--no-check", action="store_true")

    # intelmq server adduser
    srv_adduser = srv_subcommands.add_parser("adduser", help="adds new user", usage="intelmq server adduser [OPTIONS]")
    srv_adduser.set_defaults(func=server_adduser)
    srv_adduser._optionals.title = "Options"
    srv_adduser.add_argument('--username', required=True, help='the username of the account', type=str)
    srv_adduser.add_argument('--password', required=False, help='the password of the account', type=str)

    args = parser.parse_args()
    args.func = print_version if args.version else args.func
    return args.func(**vars(args))


if __name__ == "__main__":
    main()
