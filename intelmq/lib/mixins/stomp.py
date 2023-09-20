""" StompMixin for IntelMQ

SPDX-FileCopyrightText: 2017 Sebastian Wagner, 2023 NASK
SPDX-License-Identifier: AGPL-3.0-or-later
"""

from typing import (
    Any,
    Callable,
    List,
    NoReturn,
    Tuple,
)

try:
    import stomp
except ImportError:
    stomp = None

from intelmq.lib.exceptions import MissingDependencyError


class StompMixin:

    """A mixin that provides certain common methods for STOMP bots."""

    #
    # STOMP bot attributes relevant to this mixin

    server: str
    port: int
    heartbeat: int

    ssl_ca_certificate: str  # TODO: could be pathlib.Path
    ssl_client_certificate: str  # TODO: could be pathlib.Path
    ssl_client_certificate_key: str  # TODO: could be patlib.Path

    #
    # Helper methods intended to be used in subclasses

    @classmethod
    def stomp_bot_parameters_check(cls, parameters: dict) -> List[List[str]]:
        """Intended to be used in bots' `check()` static/class method."""
        logs = []
        cls.__verify_parameters(
            get_param=parameters.get,
            on_error=lambda msg: logs.append(['error', msg]),
        )
        return logs

    def stomp_bot_runtime_initial_check(self) -> None:
        """Intended to be used in bots' `init()` instance method."""
        self.__verify_dependency()
        self.__verify_parameters(
            get_param=self.__get_own_attribute,
            on_error=self.__raise_value_error,
        )

    def prepare_stomp_connection(self) -> Tuple['stomp.Connection', dict]:
        """
        Get a `(<STOMP connection>, <STOMP connect arguments>)` pair.

        * `<STOMP connection>` is a new instance of `stomp.Connection`,
           with the SSL stuff *already configured*, but *without* any
           invocations of `connect()` made yet;

        * `<STOMP connect arguments>` is a dict of arguments -- ready
          to be passed to the `connect()` method of the aforementioned
          `<STOMP connection>` object.
        """
        ssl_kwargs, connect_kwargs = self.__get_ssl_and_connect_kwargs()
        host_and_ports = [(self.server, int(self.port))]
        stomp_connection = stomp.Connection(host_and_ports=host_and_ports,
                                            heartbeats=(self.heartbeat,
                                                        self.heartbeat))
        stomp_connection.set_ssl(host_and_ports, **ssl_kwargs)
        return stomp_connection, connect_kwargs

    #
    # Implementation details

    _DEPENDENCY_NAME_REMARK = (
        "Note that the actual name of the pip-installable "
        "distribution package is 'stomp.py', not 'stomp'.")

    @classmethod
    def __verify_dependency(cls) -> None:
        # Note: the pip-installable package's name is 'stomp.py', but
        # e.g. the apt-installable package's name is 'python3-stomp' (or
        # similar) -- that's why we pass to the `MissingDependencyError`
        # constructor the name 'stomp', but also pass the value of the
        # `_DEPENDENCY_NAME_REMARK` constant as `additional_text`...
        if stomp is None:
            raise MissingDependencyError('stomp',
                                         additional_text=cls._DEPENDENCY_NAME_REMARK)
        if stomp.__version__ < (4, 1, 8):
            raise MissingDependencyError('stomp', version="4.1.8",
                                         installed=stomp.__version__,
                                         additional_text=cls._DEPENDENCY_NAME_REMARK)

    @classmethod
    def __verify_parameters(cls,
                            get_param: Callable[[str], Any],
                            on_error: Callable[[str], None]) -> None:
        for param_name in [
            'ssl_ca_certificate',
            'ssl_client_certificate',
            'ssl_client_certificate_key',
        ]:
            cls.__verify_file_param(param_name, get_param, on_error)

    @classmethod
    def __verify_file_param(cls,
                            param_name: str,
                            get_param: Callable[[str], Any],
                            on_error: Callable[[str], None]) -> None:
        path = get_param(param_name)
        if path is None:
            on_error(f"Parameter {param_name!r} is not given "
                     f"(or is set to None).")
            return
        try:
            open(path, 'rb').close()
        except OSError as exc:
            # (note: the filename is mentioned in the included exc message)
            on_error(f"Cannot open file specified as parameter "
                     f"{param_name!r} ({str(exc)!r}).")

    def __get_own_attribute(self, param_name: str) -> Any:
        return getattr(self, param_name, None)

    def __raise_value_error(self, msg: str) -> NoReturn:
        raise ValueError(msg)

    def __get_ssl_and_connect_kwargs(self) -> Tuple[dict, dict]:
        # Note: the `ca_certs` argument to `set_ssl()` must always be
        # provided, otherwise the `stomp.py`'s machinery would *not*
        # perform any certificate verification!
        ssl_kwargs = dict(
            ca_certs=self.ssl_ca_certificate,
            cert_file=self.ssl_client_certificate,
            key_file=self.ssl_client_certificate_key,
        )
        connect_kwargs = dict(wait=True)
        return ssl_kwargs, connect_kwargs
