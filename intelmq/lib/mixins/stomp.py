""" StompMixin for IntelMQ

SPDX-FileCopyrightText: 2017 Sebastian Wagner, 2023 NASK
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import enum
import os
import ssl
import sys
from typing import (
    Any,
    Callable,
    List,
    NoReturn,
    Tuple,
    Union,
)

try:
    import stomp
except ImportError:
    stomp = None
else:
    import stomp.transport

from intelmq.lib.exceptions import MissingDependencyError


class StompMixin:

    """A mixin that provides certain common methods for STOMP bots."""

    #
    # STOMP bot attributes relevant to this mixin

    server: str
    port: int
    heartbeat: int

    # Note: the `ssl_ca_certificate` configuration parameter must be set:
    # * *either* to the server's CA certificate(s) file path,
    # * *or* to an empty string -- dictating that the SSL tools employed
    #   by the `stomp.py`'s machinery will attempt to load the system’s
    #   default CA certificates.
    # The latter, if applicable, is more convenient -- by avoiding the
    # need to manually update the CA certificate(s) file.
    ssl_ca_certificate: str
    # (^ TODO: could also be pathlib.Path)

    auth_by_ssl_client_certificate: bool

    # Used if `auth_by_ssl_client_certificate` is true (otherwise ignored):
    ssl_client_certificate: str       # (cert file path)
    ssl_client_certificate_key: str   # (cert's key file path)
    # (^ TODO: could also be pathlib.Path)

    # Used if `auth_by_ssl_client_certificate` is false (otherwise ignored):
    username: str   # (STOMP auth *login*)
    password: str   # (STOMP auth *passcode*)

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
        _StompPyDedicatedSSLProxy.patch_stomp_transport_ssl()
        ssl_kwargs, connect_kwargs = self.__get_ssl_and_connect_kwargs()
        # Note: here we coerce `port` to int just to be on the safe
        # side, as some historical versions of `etc/feeds.yaml` used
        # to set it to a string.
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
        if stomp.__version__ < (4, 1, 12):
            raise MissingDependencyError('stomp', version="4.1.12",
                                         installed=stomp.__version__,
                                         additional_text=cls._DEPENDENCY_NAME_REMARK)

    @classmethod
    def __verify_parameters(cls,
                            get_param: Callable[[str], Any],
                            on_error: Callable[[str], None]) -> None:
        file_param_names = []
        if get_param('ssl_ca_certificate'):
            file_param_names.append('ssl_ca_certificate')
        if cls.__should_cert_auth_params_be_verified(get_param, on_error):
            file_param_names.extend([
                'ssl_client_certificate',
                'ssl_client_certificate_key',
            ])
        for param_name in file_param_names:
            cls.__verify_file_param(param_name, get_param, on_error)

    @classmethod
    def __should_cert_auth_params_be_verified(cls,
                                              get_param: Callable[[str], Any],
                                              on_error: Callable[[str], None]) -> bool:
        flag = get_param('auth_by_ssl_client_certificate')
        if not isinstance(flag, bool):
            # Let us better be strict here -- explicitly rejecting any
            # non-`bool` values as potentially misleading (e.g., consider
            # a string like "false", which would be interpreted as True).
            on_error(f"Parameter 'auth_by_ssl_client_certificate' "
                     f"is not set to a bool value (got: {flag!r}).")
            flag = False
        return flag

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
        # Note: a *non-empty* and *non-None* `ca_certs` argument must
        # always be passed to `set_ssl()`; otherwise the `stomp.py`'s
        # machinery would *not* enable any certificate verification!
        ssl_kwargs = dict(ca_certs=(
            self.ssl_ca_certificate if self.ssl_ca_certificate
            else _SYSTEM_DEFAULT_CA_MARKER))
        connect_kwargs = dict(wait=True)
        if self.auth_by_ssl_client_certificate:
            ssl_kwargs.update(
                cert_file=self.ssl_client_certificate,
                key_file=self.ssl_client_certificate_key,
            )
        else:
            connect_kwargs.update(
                username=self.username,
                passcode=self.password,
            )
        return ssl_kwargs, connect_kwargs


# Note: internally, we need to use a non-empty marker string because the
# logic of the `stomp.py`'s machinery does not make it possible to use
# None or an empty string as a request to load the system's default CA
# certificates.  Also, note that the string is intentionally an absolute
# filesystem path which *obviously does not point to an existing file*
# -- in case the value was used, by accident, as a CA certificate file
# path (as it is better to crash than to allow for silent misbehavior).
_SYSTEM_DEFAULT_CA_MARKER = '/SYSTEM-DEFAULT-CA-SPECIAL-INTELMQ-MARKER/'


class _StompPyDedicatedSSLProxy:

    """
    A kind of proxy to wrap the `stomp.transport` module's `ssl` member
    (originally being an object representing the standard `ssl` module),
    replacing some `ssl`-provided tools with their patched variants.

    We need it to fix the following two problems:

    * (1) Certain versions of `stomp.py` we need to be compatible with
      use the `ssl` module's tools in such ways that suffer from certain
      *security weaknesses*.  (In particular, `stomp.py >=8.0, <8.1`
      creates an `SSLContext` instance with the `check_hostname` flag
      unset -- an important negative effect is that the hostname of the
      STOMP server is *not* checked during the TLS handshake! See also
      code comments...)

    * (2) No version of `stomp.py` (at least as of this writing, i.e., up
      to and including `8.1.0`) makes it possible to load the *system's
      default CA certificates* -- condemning us to bother with manual
      updates of the CA certificate(s) file, even if the certificate of
      the STOMP server we connect to could be verified using some of the
      publicly available CA certificates which are part of nearly all
      mainstream operating system distributions (this is the case with
      the new *n6* Stream API server's certificate).

    Note that the `ssl` module itself and all its members (as seen from
    anywhere else than the `stomp.transport` module) are left untouched.
    Just the `ssl` member of the `stomp.transport` module is replaced
    with an instance of this class (it is done by invoking the class
    method `_StompPyDedicatedSSLProxy.patch_stomp_transport_ssl()`).

    ***

    The implementation of this class assumes that:

    * the Python version is `>= 3.7` (guaranteed thanks to the IntelMQ's
      project/setup declarations);
    * the `stomp.py` dependency is installed and its version is always
      `>= 4.1.12` (guaranteed thanks to STOMP bots' `REQUIREMENTS.txt`;
      see also: the `StompMixin.__verify_dependency()` method invoked in
      the `StompMixin.stomp_bot_runtime_initial_check()` method);
    * the `stomp` importable module has the `transport` submodule (see
      the `import stomp.transport` near the beginning of the source code
      of the module in which `_StompPyDedicatedSSLProxy` is defined).
    """

    #
    # Checking and replacing `stomp.transport` module's `ssl` member

    @classmethod
    def patch_stomp_transport_ssl(cls) -> None:
        if getattr(stomp.transport, 'DEFAULT_SSL_VERSION', None) is None:
            raise NotImplementedError('stomp.transport.DEFAULT_SSL_VERSION'
                                      'not found or None')
        found_ssl = getattr(stomp.transport, 'ssl', None)
        if found_ssl is ssl:
            # (patch only if not already patched!)
            stomp.transport.ssl = cls()
        elif not isinstance(found_ssl, cls):
            raise NotImplementedError(f'unexpectedly, stomp.transport.ssl '
                                      f'is neither {ssl!r} nor an instance '
                                      f'of {cls!r} (found: {found_ssl!r})')

    #
    # Proxying/substituting `ssl` tools for `stomp.transport` module

    def __dir__(self) -> List[str]:
        return dir(ssl)

    def __getattribute__(self, name: str) -> Any:
        # Selected `ssl` module's members are replaced with their patched
        # variants (see their definitions below...).
        if name in {'SSLContext', 'create_default_context'}:
            return super().__getattribute__(name)

        # The rest of the `ssl` module's members are just retrieved from
        # that module:
        return getattr(ssl, name)

    def __setattr__(self, name: str, value: Any) -> None:
        raise NotImplementedError('setting attributes on stomp.'
                                  'transport.ssl is not supported')

    def __delattr__(self, name: str) -> None:
        raise NotImplementedError('deleting attributes from stomp.'
                                  'transport.ssl is not supported')

    class SSLContext(ssl.SSLContext):

        """
        Note: `ssl.SSLContext` is invoked directly by `stomp.py >= 8.0.0`.
        Here we subclass it to handle our `_SYSTEM_DEFAULT_CA_MARKER` as
        well as to ensure that certain important security-related stuff is
        in accordance with the Python core developers' recommendations (see:
        https://docs.python.org/library/ssl.html#security-considerations)
        and that the TLS version we use is not too old...
        """

        def __new__(cls,
                    protocol: Union[int, enum.Enum, None] = None,
                    *args,
                    **kwargs) -> '_StompPyDedicatedSSLProxy.SSLContext':
            # Note: the `stomp.py`'s machinery *ignores* `ssl_version`
            # got by `stomp.Connection.set_ssl()`, and passes to the
            # `ssl.SSLContext` constructor the value of the constant
            # `stomp.transport.DEFAULT_SSL_VERSION`.  However, because
            # `PROTOCOL_TLS_CLIENT` is a good modern setting, we use it
            # instead of `stomp.transport.DEFAULT_SSL_VERSION` (which,
            # if not already set to `PROTOCOL_TLS_CLIENT`, must have
            # been set to some older setting -- depending on the version
            # of `stomp.py`...).
            ssl_context = super().__new__(
                cls,
                ssl.PROTOCOL_TLS_CLIENT,
                *args,
                **kwargs)
            # The versions of Python older than 3.10 seem to refrain
            # from blocking the use of the TLS versions 1.0 and 1.1
            # which nowadays are considered insecure.  Let's fix that:
            ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
            return ssl_context

        def load_verify_locations(self,
                                  cafile: Union[str, None] = None,
                                  capath: Union[str, None] = None,
                                  cadata: Union[str, bytes, None] = None) -> None:
            if cafile == _SYSTEM_DEFAULT_CA_MARKER and not (capath or cadata):
                self.load_default_certs(ssl.Purpose.SERVER_AUTH)
            else:
                super().load_verify_locations(cafile, capath, cadata)

        def wrap_socket(self,
                        *args,
                        **kwargs) -> ssl.SSLSocket:
            # Let's be sure that nothing spoiled these two SSL context's
            # settings, as they are crucial for certificate verification!
            if self.verify_mode != ssl.CERT_REQUIRED:
                raise ValueError(f"value of SSL context's `verify_mode` "
                                 f"setting ({self.verify_mode!r}) is, "
                                 f"unexpectedly, different from "
                                 f"{ssl.CERT_REQUIRED!r}")
            if not self.check_hostname:
                raise ValueError(f"value of SSL context's `check_hostname` "
                                 f"setting ({self.check_hostname!r}) is, "
                                 f"unexpectedly, not true")
            return super().wrap_socket(*args, **kwargs)

    @classmethod
    def create_default_context(cls,
                               purpose: ssl.Purpose = ssl.Purpose.SERVER_AUTH,
                               *,
                               cafile: Union[str, None] = None,
                               capath: Union[str, None] = None,
                               cadata: Union[str, bytes, None] = None) -> ssl.SSLContext:

        """
        Note: the `ssl.create_default_context()` helper is used by
        `stomp.py >= 4.1.12, < 8.0.0`.  That is OK, except that we
        also want to handle our `_SYSTEM_DEFAULT_CA_MARKER` as well
        as to provide some additional security-related tweaks and
        checks -- provided by our custom subclass of `SSLContext`.
        """

        if purpose == ssl.Purpose.SERVER_AUTH:
            ssl_context = cls.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            if not (cafile or capath or cadata):
                cafile = _SYSTEM_DEFAULT_CA_MARKER
            ssl_context.load_verify_locations(cafile, capath, cadata)

            if sys.version_info[:2] >= (3, 8):
                # Support for OpenSSL 1.1.1 keylog (copied from `Py>=3.8`):
                if hasattr(ssl_context, 'keylog_filename'):
                    keylogfile = os.environ.get('SSLKEYLOGFILE')
                    if keylogfile and not sys.flags.ignore_environment:
                        ssl_context.keylog_filename = keylogfile

        else:
            ssl_context = ssl.create_default_context(
                purpose,
                cafile=cafile,
                capath=capath,
                cadata=cadata)

        return ssl_context
